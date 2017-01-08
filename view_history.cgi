#!/usr/bin/perl -w

# ---------------------------------------------
# view_history.cgi   - Create by Lance Wicks
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
# 20 January 2004, Lance Wicks - File created

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

sub show_history {
# This subroutine prints a list of players associated with this shiai
# ----------------------------------------------------------------------------------

    print p("Start show history") if $DEBUG;

    # create the scalers we need to use in the sql
    # ----------------------------------------------
    # Takes the values passed to us and assign them to a scaler
    my @shiai = @_;
    print p( "passed_info: ", $shiai[0] ) if $DEBUG;
    my $history_table
        = "data/shiai_data/"
        . $shiai[0]
        . "_hst";    # eg: data/shiai_data/userTest.ldr the ladder itself
    print p( "ladder_Table: ", $history_table ) if $DEBUG;

    # next we need to make a connection to the ladder_table CSV file
    # ---------------------------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT * FROM history_db"
        ;    # this is the SQL command we want to execute
#             my $params = ($judoka_id);                          # Theese are the parameteres we will use in the SQL command above
    print "$sql\n\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute();                  # excecute the SQL using our parameters

#             my @result = $sth->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS

    my @sql_returned;
    print h2("History");
    print("<table width=85% border=1>");
    while ( @sql_returned = $sth->fetchrow_array )
    {    # This while loop continues till there is no more reults
        print p( "Results = ", @sql_returned ) if $DEBUG;
#                                                               my $name = $sql_returned[0];          #create a scaler for tidiness which has the JudokaID
        print(
            "<TR><TD>$sql_returned[0]</TD><TD>$sql_returned[1]</TD><TD>$sql_returned[2]</TD></TR>"
        );

    }
    print("</table>");

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)
#
#             print p("result = ", @result)if $DEBUG;                # Prints the result of our SQL command if we are in debug mode.
#
#
#
#

    print p("End show_history") if $DEBUG;
}

# ------------------
# End of Subroutines

# Main Code Block
# ----------------

print header(), start_html("e-Judo Test Area"),
    h1("VIEW SHIAI");    # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p( "parameters: ", param() )     if $DEBUG;
print p( "values: ",     param("id") ) if $DEBUG;

# the ID parameter should be present when they first arrive and not when the form is filled in, so if it does exist we need to do the lines below
my $shiai = param("shiai_id");
print p( "Shiai parameter = ", $shiai ) if $DEBUG;
show_history($shiai);

# End of the if statement related to the Judoka parameter

print p("END main block") if $DEBUG;

# --------------------
# End of Main Block

