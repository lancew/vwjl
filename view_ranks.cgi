#!/usr/bin/perl -w

# ---------------------------------------------
# view_ranks.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script allows you to view the Shiai on the system
#
# How does it work?
# =================
#
#
# History:
# ========
# 21 September 2004, Lance Wicks - File created

my $DEBUG = 0;    #  If this is set to 1 then we see the debug messages.

# The following 4 lines set strict PERL coding then load the CGI DBI and DBD::Anydata modules.
# ---------------------------------------------------------------------------------------------
use strict;               # force strict programming controls
use CGI qw(:standard);    # use the CGI.PM module
use lib './MyLib'
    ; # use the modules in MyLib, this is the DBD::Anydata used for database activities
use DBI
    ; # This calls the DBI module, which along with the line above allows us to do database activities

# Sub routines
# --------------

sub show_ranks {
# This subroutine prints a list of players associated with this shiai
# ----------------------------------------------------------------------------------

    print p("Start show history") if $DEBUG;

    # create the scalers we need to use in the sql
    # ----------------------------------------------
    # Takes the values passed to us and assign them to a scaler

    my $judoka_table = "data/judoka_csv"
        ;    # eg: data/shiai_data/userTest.ldr the ladder itself
    print p( "Judoka_Table: ", $judoka_table ) if $DEBUG;

    # next we need to make a connection to the ladder_table CSV file
    # ---------------------------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'judoka_db', 'CSV', $judoka_table, 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT * FROM judoka_db"
        ;    # this is the SQL command we want to execute
    print "$sql\n\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute();                  # excecute the SQL using our parameters

    my @sql_returned;
    my %ranking;

    while ( @sql_returned = $sth->fetchrow_array )
    {    # This while loop continues till there is no more reults
        print p( "Results = ", @sql_returned ) if $DEBUG;

# print ("<TR><TD>$sql_returned[2]</TD><TD>$sql_returned[10]</TD><TD>$sql_returned[11]</TD></TR>");
        $ranking{ $sql_returned[2] } = $sql_returned[10];

    }

    print h2("JUDOKA - Ranked by number of Wins");
    print("<table width=85% border=1>");
    print("<TR><TD>Name</TD><TD>Wins</TD></TR>");

    for my $key ( sort { $ranking{$b} <=> $ranking{$a} } ( keys %ranking ) ) {
        print p("<TR><TD> $key </TD><TD>$ranking{$key}</TD></TR>");
    }
    print("</table>");

    # ----------------------

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)
#
#             print p("result = ", @result)if $DEBUG;                # Prints the result of our SQL command if we are in debug mode.
#
#
#
#

    print p("End show_ranks") if $DEBUG;
}

# ------------------
# End of Subroutines

# Main Code Block
# ----------------

print header(), start_html("e-Judo View Ranks"),
    h1("VIEW Ranks");    # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p( "parameters: ", param() )     if $DEBUG;
print p( "values: ",     param("id") ) if $DEBUG;

# the ID parameter should be present when they first arrive and not when the form is filled in, so if it does exist we need to do the lines below

show_ranks();

# End of the if statement related to the Judoka parameter

print p("END main block") if $DEBUG;

# --------------------
# End of Main Block

