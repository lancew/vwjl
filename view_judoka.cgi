#!/usr/bin/perl -w

# ---------------------------------------------
# view_judoka.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script allows you to view your Judoka(s) and their statistics
#
# How does it work?
# =================
# Basically it uses your userID, accesses the Judoka database finds all your Judoka and lets you choose which one you want to look at
# Then it takes which ever one you clicked on and displays it
#
# History:
# ========
# 07 January 2004, Lance Wicks - File created

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
sub read_judoka_data {
    # This sub reads in all the data from the database.
    # --------------------------------------------------
    print p("Start read_judoka_data") if $DEBUG;

    my @passed_info
        = @_;    # Takes the values passed to us and assign them to a scaler
    my $judoka_id = $passed_info[0]
        ; # this is the users id passed to us, we create this scaler just to make the script easier to understand
    print p( "judoka_id = ", $judoka_id ) if $DEBUG;
    my @judoka_data;
    print p( "passed info: ", @passed_info ) if $DEBUG;

    # Use DBI to connect to the judoka_csv datafile
    #-----------------------------------------------
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql_query = "SELECT * FROM judoka WHERE judoka_id = ?"
        ;    # this is the SQL command we want to execute
    my $sql_params = ($judoka_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    print p("$sql_query\n[$sql_params]\n")
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql_query);    # prepare the SQL command
    $sth->execute($sql_params);    # excecute the SQL using our parameters

    my @result = $sth->fetchrow_array
        ; # this line takes the results of the select and puts it in the array called RESULTS
    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p( "result = ", @result )
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.

    print p( "Judoka data = ", @result ) if $DEBUG;

    return (@result);

    print p("End read_judoka_data") if $DEBUG;
}

sub display_judoka_data {
    print p("Start display_judoka_data") if $DEBUG;
    my @passed_info = @_;
    print h1( "Judoka: ", $passed_info[2] );
    my $number_of_items = @passed_info
        ; # This tells us how many items are in the passed info ie how many data fields
    print p( "Number of variables =", $number_of_items ) if $DEBUG;
    # we need to connect to the judoka DB...
    # ----------------------------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql_dataquery
        = "SELECT * FROM judoka"; # this is the SQL command we want to execute
    print p("$sql_dataquery\n")
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql_dataquery);    # prepare the SQL command
    $sth->execute();    # excecute the SQL using our parameters

    my @result = $sth->fetchrow_array
        ; # this line takes the results of the select and puts it in the array called RESULTS

    # ...and get the column headings
    # --------------------------------
    my @headings = @{ $sth->{NAME} };
    print p( "Column headings = ", @headings ) if $DEBUG;
    my $number_of_headings = @headings;
    print p( "Number of headings = ", $number_of_headings ) if $DEBUG;

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    # we now have to arrays @headings & @passed_info
    # we need to present these in a table.

    print("<table width=85% border=1>");    # create a table

    for ( my $loop = 2; $loop ne 123; $loop++ ) {
        print("<TR><TD>$headings[$loop]</TD><TD>$passed_info[$loop]</TD>");
        print("<TD>$loop</TD>") if $DEBUG;
        print("</TR>");
    }

    print("</table>");

    print p("End display_judoka_data") if $DEBUG;
}

sub list_users_judoka {
# This subroutine opens the judoka database and finds the Judoka names for the user
# It then returns this list of names to the system, with a link to each.
# ----------------------------------------------------------------------------------
    print p("Start list_users_judoka") if $DEBUG;
    my @passed_info
        = @_;    # Takes the values passed to us and assign them to a scaler
    my $user_id = $passed_info[0]
        ; # this is the users id passed to us, we create this scaler just to make the script easier to understand
    print p( "passed_id: ", @passed_info ) if $DEBUG;
    my @judoka_found
        ; # initialise the array where we shall collect the judoka information
    # next we use DBI to connect to the judoka_csv datafile
    #-----------------------------------------------
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the judoka_id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT judoka_id,name FROM judoka WHERE user_id = ?"
        ;    # this is the SQL command we want to execute
    my @params = ($user_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    print "$sql\n[@params]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute(@params);           # excecute the SQL using our parameters

    my @sql_returned;
    print h2("JUDOKA LIST");
    while ( @sql_returned = $sth->fetchrow_array )
    {    # This while loop continues till there is no more reults
        print p( "Results = ", @sql_returned ) if $DEBUG;
        my $judoka_id = $sql_returned[0]
            ;    #create a scaler for tidiness which has the JudokaID
        my $judoka_name = $sql_returned[1]
            ;    #create a scaler for tidiness that is the name of the Judoka
        print p(
            "<a href=view_judoka.cgi?id=$user_id&judoka=$judoka_id&name=$judoka_name>$judoka_name</a>"
        );

    }

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p("End list_users_judoka") if $DEBUG;
}

# ------------------
# End of Subroutines

# Main Code Block
# ----------------

print header(), start_html("e-Judo Test Area"),
    h1("VIEW JUDOKA");    # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p( "parameters: ", param() )     if $DEBUG;
print p( "values: ",     param("id") ) if $DEBUG;

if ( param("id") )
{ # the ID parameter should be present when they first arrive and not when the form is filled in, so if it does exist we need to do the lines below
    if ( param("judoka") )
    { # if the JUDOKA parameter exists then the user has selected a Judoka so show this judoka
        my $judoka      = param("judoka");
        my $judoka_name = param("name");
        print p( "Judoka_NAme: ", $judoka_name ) if $DEBUG;
        my @judoka_info = read_judoka_data($judoka)
            ; # Call the subroutine to collect the judoka data from the database and assign it to an array
        print( "The Judoka returned = ", @judoka_info ) if $DEBUG;
        print p(
            " <a href=entershiai.cgi?judoka_id=$judoka&judoka_name=$judoka_name>Enter a shiai</a>"
        );    # Print a link to enter a shiai.
        print p(
            " <a href=make_challenge.cgi?judoka_id=$judoka&judoka_name=$judoka_name>Make a challenge</a>"
        );    # Print a link to challenge another judoka
         #    print p(" <a href=accept_challenge.cgi?judoka_id=$judoka&judoka_name=$judoka_name>Accept a challenge</a>"); # Print a link to accept a challenge
         #    print p(" <a href=challenges.cgi?judoka_id=$judoka>Make/Accept Challenges</a>"); # Print a link to make challengesjust above the Judoka info.
        display_judoka_data(@judoka_info)
            ;    # Take the data collected and display it

    }
    else
    { # If the judoka parameter does not exist then we need to find all the users judoka and allow them to select one to view
        list_users_judoka( param("id") )
            ; # This line calls the sub that lists the users Judoka (with links to view the selected Judoka)
    }    # End of the if statement related to the Judoka parameter
}
else
{ # If the id parameter does not exist they should not be here so display a link to the front page (e-judo.cgi)
    print p("Problem!");
    print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
}

print p("END main block") if $DEBUG;

# --------------------
# End of Main Block

