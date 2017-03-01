#!/usr/bin/perl -w
use strict;
use warnings;

# ---------------------------------------------
# entershiai.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script allows you to enter shiai
#
# How does it work?
# =================
# Steps/Stages
# ------------
# 1) we know what judoka we are working with (passed to the script) - yes
# 2) Create a list of shiai to enter - yes
# 3) Let the user click on the one they wish to enter - yes
# 4) Enter the judoka_ID into the shiai data files - yes
# 5) Return to the main menu
#
# History:
# ========
# 23 March 2004, Lance Wicks - File created, based on the challenge.cgi script.
# 23 March 2004, Lance Wicks - Initial three stages complete, needs re-writing to handle different contest formats in next revision.

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

sub list_shiai {
# This subroutine opens the shiai database and finds all the shiai
# It then returns this list of names to the system, with a link to each.
# ----------------------------------------------------------------------------------
    print p("Start list_shiai") if $DEBUG;
    my @passed_info
        = @_;    # Takes the values passed to us and assign them to a scaler
    my $judoka_id   = $passed_info[0];
    my $judoka_name = $passed_info[1]
        ; # this is the judoka id passed to us, we create this scaler just to make the script easier to understand
    print p( "passed_info: ", @passed_info ) if $DEBUG;
    my @shiai_found
        ;  # initialise the array where we shall collect the shiai information
    # next we use DBI to connect to the shiai_csv datafile
    #-----------------------------------------------
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' )
        ;    # Connect to the shiai_csv data file

    # Next we collect all the shiai IDs and names from the db
    my $sql = "SELECT shiai_id,name FROM shiai_db"
        ;    # this is the SQL command we want to execute

    print "$sql\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute();                  # excecute the SQL using our parameters

    my @sql_returned;
    print h2("SHIAI LIST");
    while ( @sql_returned = $sth->fetchrow_array )
    {    # This while loop continues till there is no more reults
        print p( "Results = ", @sql_returned ) if $DEBUG;
        my $shiai_id = $sql_returned[0]
            ;    #create a scaler for tidiness which has the JudokaID
        my $shiai_name = $sql_returned[1]
            ;    #create a scaler for tidiness that is the name of the Judoka

# The following line prints out the shiai name with a link to enter this Judoka into the shiai
# ----------------------------------------------------------------------------------------------
        print p(
            "<a href=entershiai.cgi?judoka_id=$judoka_id&shiai=$shiai_id&judoka_name=$judoka_name>$shiai_name</a>"
        );

    }

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p("End list_shiai") if $DEBUG;
}

sub enter_judoka_in_ladder {
# This subroutine enters the Judoka ID into the shiai
# ----------------------------------------------------------------------------------
    print p("Start enter_judoka_in_ladder") if $DEBUG;

    # create the scalers we need to use in the sql
    # ----------------------------------------------
    my @passed_info
        = @_;    # Takes the values passed to us and assign them to a scaler
    my $shiai_id    = $passed_info[0];
    my $judoka_id   = $passed_info[1];
    my $judoka_name = $passed_info[2];
    print p( "passed_info: ", @passed_info ) if $DEBUG;
    my $ladder_table
        = "data/shiai_data/"
        . $shiai_id
        . "_ldr";    # eg: data/shiai_data/userTest.ldr the ladder itself
    print p( "ladder_Table: ", $ladder_table ) if $DEBUG;

    # next we need to make a connection to the ladder_table CSV file
    # ---------------------------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT id FROM ladder_db WHERE id = ?"
        ;    # this is the SQL command we want to execute
    my $params = ($judoka_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    print "$sql\n[$params]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement
    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute($params);           # excecute the SQL using our parameters

    my @result = $sth->fetchrow_array
        ; # this line takes the results of the select and puts it in the array called RESULTS
    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p( "result = ", @result )
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.

    if (@result)
    {  #if the result array is in existence (ie we found the username) then...
        print h2("this Judoka is already entered!");

    }
    else {

        print p("about to enter Judoka") if $DEBUG;

        # Okay we need to add the following fields into the table:
        # ----------------------------------------------------------
        # player_name - This is passed to us from previous script
        # ID - This is passed to us from previous script
        # position - This will be the number of rows in the table + 1
        # fights - will equal 0
        # wins  - will equal 0
        # joined_date - the date and time right now
        # date_last_fight - will be blank

        # first lets setup those scalers.
        # --------------------------------------
        my $player_name     = $judoka_name;
        my $ID              = $judoka_id;
        my $position        = 0;
        my $fights          = 0;
        my $wins            = 0;
        my $joined_date     = gmtime();
        my $date_last_fight = "no Fights";

        # attached to the ladder table and enter the Judoka
        # -------------------------------------------------
        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
            ;    # tell DBI we want to use the Anydata module in ./MyLibs
        $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog' )
            ;    # Connect to the judoka_csv data file

        # add the data into a new record
        my $sql = "INSERT INTO ladder_db VALUES ( ?,?,?,?,?,?,? )"
            ; # this is the SQL command we want to execute, there SHOULD be 18 question marks

        my @ladder_params = (
            $player_name, $ID, $position, $fights, $wins, $joined_date,
            $date_last_fight
            )
            ; # Make the parameters those passed to us from the previous routine (and originally from the user)
        print "$sql\n[@ladder_params]\n"
            if $DEBUG;    # if we are in debug mode print the SQL statement

        my $sth = $dbh->prepare($sql); # prepare the SQL command
        $sth->execute(@ladder_params); # excecute the SQL using our parameters

        $dbh->disconnect()
            ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

        my @data_to_pass = ( $shiai_id, $judoka_id, $judoka_name );
        enter_judoka_in_history(@data_to_pass);

        print p("Player Entered");
    }

    print p("End enter_judoka_in_ladder") if $DEBUG;
}

sub enter_judoka_in_history {
# This subroutine enters the Judoka ID into the shiai
# ----------------------------------------------------------------------------------
    print p("Start enter_judoka_in_history") if $DEBUG;

    # create the scalers we need to use in the sql
    # ----------------------------------------------
    my @passed_info
        = @_;    # Takes the values passed to us and assign them to a scaler
    my $shiai_id    = $passed_info[0];
    my $judoka_id   = $passed_info[1];
    my $judoka_name = $passed_info[2];
    print p( "passed_info: ", @passed_info ) if $DEBUG;
    my $history_table
        = "data/shiai_data/"
        . $shiai_id
        . "_hst";    # eg: data/shiai_data/userTest_hst the ladder itself
    print p( "history_Table: ", $history_table ) if $DEBUG;

    # next we need to make a connection to the history_table CSV file
    # ---------------------------------------------------------------

    print p("about to enter history") if $DEBUG;

    # Okay we need to add the following fields into the table:
    # ----------------------------------------------------------
    # date_time - right now
    # activity - short description
    # description - long description

    # first lets setup those scalers.
    # --------------------------------------

    my $date_time   = gmtime();
    my $activity    = "Entry";
    my $description = "$judoka_name entered this shiai";

    # attached to the ladder table and enter the Judoka
    # -------------------------------------------------
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog' )
        ;    # Connect to the judoka_csv data file

    # add the data into a new record
    my $sql = "INSERT INTO history_db VALUES ( ?,?,? )"
        ; # this is the SQL command we want to execute, there SHOULD be 18 question marks

    my @history_params = ( $date_time, $activity, $description )
        ; # Make the parameters those passed to us from the previous routine (and originally from the user)
    print "$sql\n[@history_params]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);     # prepare the SQL command
    $sth->execute(@history_params);    # excecute the SQL using our parameters

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p("History Created") if $DEBUG;    # just a reference in debug mode

    print p("End enter_judoka_in_history") if $DEBUG;
}

# ------------------
# End of Subroutines

# Main Code Block
# ----------------

print header(), start_html("e-Judo Test Area"),
    h1("Enter Shiai");    # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p( "parameters: ", param() ) if $DEBUG;
print p( "values: ", param("judoka_id"), param("judoka_name") ) if $DEBUG;

if ( param("judoka_id") )
{ # the judoka-Id is passed to us from the previous script, so should exist. If it does not something is wrong so exit
    if ( param("shiai") )
    { # if the Shiai parameter exists then the user has selected a shiai to enter
        my $shiai       = param("shiai");
        my $judoka      = param("judoka_id");
        my $judoka_name = param("judoka_name");
        print p( "Shiai parameter = ",       $shiai )       if $DEBUG;
        print p( "Judoka parameter = ",      $judoka )      if $DEBUG;
        print p( "Judoka_name parameter = ", $judoka_name ) if $DEBUG;

        my @data_to_pass = ( $shiai, $judoka, $judoka_name );
        enter_judoka_in_ladder(@data_to_pass);

        #
    }
    else {    # If the SHIAI param does not exist them list them
        my $judoka       = param("judoka_id");
        my $judoka_name  = param("judoka_name");
        my @data_to_pass = ( $judoka, $judoka_name );
        list_shiai(@data_to_pass)
            ; # This line calls the sub that lists the shiai, we pass the judoka ID so that we can add it to the HTTP link
    }    # End of the if statement related to the Judoka parameter
}
else
{ # If the judoka_id parameter does not exist they should not be here so display a link to the front page (e-judo.cgi)
    print p("Problem!");
    print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
}

print p("END main block") if $DEBUG;
print end_html;    # this closes the web page properly
# --------------------
# End of Main Block

