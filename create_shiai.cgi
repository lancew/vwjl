#!/usr/bin/perl -w
use strict;
use warnings;

# ---------------------------------------------
# create_shiai.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script adds a new Shiai to the database
#
# How does it work?
# =================
#
#
# History:
# ========
# 9 January 2004 - Lance Wicks - File created (based on create_judoka.cgi)
# 10 January 2004 - Lance Wicks - tested and is working OK
# 12 January 2004 - Lance Wicks - Fixed bug where this script was not adding the prize values to the DB.
# 28 January 2004 - Lance Wicks - Shout out to Roger on perlMonks.org for his help with the creating of tables in DBD::ANYDATA!
# 30 January 2004 - Lance WIcks - The script now successfully creates a shiai with 3 accompanying data tables

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

sub get_user_data {
    # This subroutine collects the users data from the user database

    print p("START of get_user_data") if $DEBUG;

    my @internal_user_data = @_
        ; # This line takes the user_data passed to us from the previous routine (@_) and allocates it to our internal user data array
    my $entered_id = $internal_user_data[0]
        ; # just so that it is clearer later we create a variable from the passed data

    # Use DBI to connect to the users_csv datafile
    #-----------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'users', 'CSV', 'data/users_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my @parameters = ($entered_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    my $sql = "SELECT * FROM users WHERE id = ?"
        ;    # this is the SQL command we want to execute
    print "$sql\n[@parameters]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute(@parameters);       # excecute the SQL using our parameters

    my @result = $sth->fetchrow_array
        ; # this line takes the results of the select and puts it in the array called RESULTS
    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p("result = @result")
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.
    return (@result);

    print p("END of get_user_data") if $DEBUG;
}

sub shiai_count {
# This sub rotine gets the Judoka the user has from judoka_csv file and returns the number
    print p("START of shiai_count") if $DEBUG;

    my @internal_shiai_data = @_
        ; # This line takes the user_data passed to us from the previous routine (@_) and allocates it to our internal user data array
    my $entered_id = $internal_shiai_data[0]
        ; # just so that it is clearer later we create a variable from the passed data

    # Use DBI to connect to the users_csv datafile
    #-----------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' )
        ;    # Connect to the _csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT * FROM shiai_db WHERE owner_id = ?"
        ;    # this is the SQL command we want to execute
    my @params = ($entered_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    print "$sql\n[@params]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute(@params);           # excecute the SQL using our parameters

    my $row_count = 0;
    my @results;                      # Initialise this variable
    while ( @results = $sth->fetchrow_array )
    {    # This while loop continues till there is no more reults
        print p( "ROW = ", @results ) if $DEBUG;
        $row_count++;
    }

    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)
    print p( "Number of Shiai for this user = ", $row_count ) if $DEBUG;
    return ($row_count);

    print p("END of shiai_count") if $DEBUG;

}

sub print_shiai_data_form {
# This subroutine create the user data web page which is filled in, the data is then used by other routines.
# Data fields:  owner_id,shiai_id,name,closedate,type,eventdate,admins_name,active,earnings,cash,entry_fee,createdate,first_prize,second_prize,third_prize,fourth_prize,fith_prize,description
#                   1         2     3       4      5      6          7         8      9      10       11       12          13           14          15          16          17          18
#                                   *       *      *      *                                           *                     *            *           *           *           *           *
# All the fields with "*" under them are  generated by the user
# The numbers indicate their position in the array(s)

    print p("START of print_shiai_data_form") if $DEBUG;
    my @internal_shiai_data = @_;
    my $user_id_passed      = $internal_shiai_data[0];
    print p( "user ID passed = ", $user_id_passed ) if $DEBUG;
    print hr, start_form;    # create a form using CGI.PM

    print p( "Shiai Name: ", textfield("shiai_name"),
        " - This is the name of the tournament" );
    print p( "Close Date: ", textfield("closedate"),
        " - This is date that entries close to the tournament" );
# The following entries are commented out for now till we come up with the later modules
#                         print p("Shiai Type: ", textfield("type"), " - This is which type of tournament format this tournament is");
    print p( "Shiai Date: ", textfield("eventdate"),
        " - the date this shiai will begin." );
    print p( "Entry Fee: ", textfield("entry_fee"),
        " - this is how much it will cost players to enter the event" );
    print p(
        "First Prize: ",
        textfield("first_prize"),
        " - This is how much the winner will receive"
    );
    print p(
        "Second Place Prize: ",
        textfield("second_prize"),
        " - This is how much the second place getter will receive"
    );
    print p(
        "Third Place Prize: ",
        textfield("third_prize"),
        " - This is how much the third place getter will receive"
    );
    print p(
        "Fourth Place Prize: ",
        textfield("fourth_prize"),
        " - This is how much the fourth place getter will receive"
    );
    print p(
        "Fifth Place Prize: ",
        textfield("fifth_prize"),
        " - This is how much the fifth place getter will receive"
    );
    print p( "Description: ",
        textfield("desc"), " - This is a short description of this event" );
    print hidden( -name => "user_id", -value => "$user_id_passed" );
    print submit( -name => 'submit button' );
    print end_form, hr;    # end the form
    print p("END of print_shiai_data_form") if $DEBUG;
}    # end of print_shiai_data_form

sub collect_shiai_data {
# This subroutine collects the user input from the form and returns it to the next form
    print p("Start of collect_shiai_data") if $DEBUG;
# Data fields:  owner_id,shiai_id,name,closedate,type,eventdate,admins_name,active,earnings,cash,entry_fee,createdate,first_prize,second_prize,third_prize,fourth_prize,fith_prize,description
#                   0         1    2     3        4      5          6         7      8      9       10       11          12           13          14          15          16          17
#                                  *     *        *      *                                           *                     *            *           *           *           *           *
    my @shiai_data;
    $shiai_data[0] = param("user_id");
    $shiai_data[1] = "BLANK_for_now"
        ; # Now take the parameters from the completed form and add them to the array
    $shiai_data[2]  = param("shiai_name");
    $shiai_data[3]  = param("closedate");
    $shiai_data[4]  = "ladder";
    $shiai_data[5]  = param("eventdate");
    $shiai_data[6]  = "BLANK";
    $shiai_data[7]  = "blank";
    $shiai_data[8]  = "blank";
    $shiai_data[9]  = "BLANK";
    $shiai_data[10] = param("entry_fee");
    $shiai_data[11] = "blank";

    $shiai_data[12] = param("first_prize");
    $shiai_data[13] = param("second_prize");
    $shiai_data[14] = param("third_prize");
    $shiai_data[15] = param("fourth_prize");
    $shiai_data[16] = param("fifth_prize");
    $shiai_data[17] = param("desc");
    print p( "Shiai_data array = ", @shiai_data ) if $DEBUG;
    return (@shiai_data);    # return the collected data
    print p("END of collect_shiai_data") if $DEBUG;
}

sub validate_shiai_data {
    # This sub routine validate the user input from collect_shiai_data
    print p("Start of validate_shiai_data") if $DEBUG;
    my @internal_data = @_
        ; # Take the array passed to this routine and assign it to an internal array

    print p( "validated data = ", @internal_data ) if $DEBUG;
    return (@internal_data);
    print p("END of validate_shiai_data") if $DEBUG;
}

sub generate_initial_values {
# This sub routinegenerates the variable data not inputed by the user (the initial variables)
# Data fields:  owner_id,shiai_id,name,closedate,type,eventdate,admins_name,active,earnings,cash,entry_fee,createdate,first_prize,second_prize,third_prize,fourth_prize,fith_prize,description
#                   0         1    2     3        4      5          6         7      8      9       10       11          12           13          14          15          16          17
#                                  *     *        *      *                                           *                     *            *           *           *           *           *
# All the fields with "*" under them are  generated by the user
# The numbers indicate their position in the array(s)
# user_id is already in the data array at this stage.
    print p("Start of generate_initial_values") if $DEBUG;
    my @internal_shiai_data = @_
        ; # Take the array passed to this routine and assign it to an internal array
    $internal_shiai_data[1] = $internal_shiai_data[0]
        . $internal_shiai_data[2]
        ; # Make the unique ID for this Judoka the users ID plus the Judoka name.
    $internal_shiai_data[6]
        = "for now just an abitrary data filed till I pass the users name OK!";
    $internal_shiai_data[7]  = "NO";
    $internal_shiai_data[8]  = 0;
    $internal_shiai_data[9]  = 0;
    $internal_shiai_data[11] = gmtime();

    print p( "Internal dta now equals = ", @internal_shiai_data ) if $DEBUG;

    print p( "Validated data + initial values = ", @internal_shiai_data )
        if $DEBUG;

    print p("END of generate_initial_values") if $DEBUG;
    return (@internal_shiai_data);
}

sub add_shiai_to_db {
    print p("Start of add_shiai_to_db subroutine") if $DEBUG;

    my @internal_shiai_data = @_
        ; # This line takes the user_data passed to us from the previous routine (@_) and allocates it to our internal user data array
    my $entered_shiai_id = $internal_shiai_data[1]
        ; # just so that it is clearer later we create a variable from the passed data

    # Use DBI to connect to the judoka_csv datafile
    #-----------------------------------------------
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT * FROM shiai_db WHERE shiai_id = ?"
        ;    # this is the SQL command we want to execute
    my $params = ($entered_shiai_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    print "$sql\n[$params]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute($params);           # excecute the SQL using our parameters

    my @result = $sth->fetchrow_array
        ; # this line takes the results of the select and puts it in the array called RESULTS
    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

#             print p("result = ", @result)if $DEBUG;                # Prints the result of our SQL command if we are in debug mode.

    if (@result)
    {  #if the result array is in existence (ie we found the username) then...
        print p("Sorry this shiai ID is in use already");

    }
    else {

        print p("about to insert the new record") if $DEBUG;
        # if the shiai_id does not exist then add the shiai!
        # so connect to the database
        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
            ;    # tell DBI we want to use the Anydata module in ./MyLibs
        $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' )
            ;    # Connect to the judoka_csv data file

        # add the data into a new record
        my $sql
            = "INSERT INTO shiai_db VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )"
            ; # this is the SQL command we want to execute, there SHOULD be 18 question marks
        my @shiai_params = (@internal_shiai_data)
            ; # Make the parameters those passed to us from the previous routine (and originally from the user)
        print "$sql\n[@shiai_params]\n"
            if $DEBUG;    # if we are in debug mode print the SQL statement

        my $sth = $dbh->prepare($sql); # prepare the SQL command
        $sth->execute(@shiai_params);  # excecute the SQL using our parameters

        print p("Shiai Created");      # just a reference in debug mode
         # print p("-> <a href=main_menu.cgi?id=$internal_shiai_data[0];>Click HERE to continue</a>");
    }

    print p( "Data added to the DB = ", @internal_shiai_data ) if $DEBUG;
    print p("END of add_shiai_to_db subroutine") if $DEBUG;
}

sub create_shiai_db_files {
# This sub looks at the type of the shiai and calls subs to create the data for it
# Basically it craetes database tables.
    print p("Start of create shiai db files") if $DEBUG;

# Collect the data from the passed array and then grap the variables we will need
# --------------------------------------------------------------------------------
    my @the_shiai_data = @_;    # This is the data transfered to us
    my $shiai_type = $the_shiai_data[4];  # Pull the shiai type from the array

    # Now depending on the type of Shiai create it.
    # ------------------------------------------------
    my $flag = "0";  # This flag is zero unless a valid module has been called
    if ( $shiai_type eq "ladder" && $flag eq "0" ) {
        create_ladder_data(@the_shiai_data);
        $flag = 1; # set the flag to yes to prevent other modules being called
    }
    # ** add other types here **

    if ( $flag eq "0" ) {
        print p(
            "Sorry, the shiai type was invalid and things went pear shaped!");
    }

    print p("END of create_shiai_DB_files") if $DEBUG;

}

sub create_ladder_data {
    # This sub creates the db datafiles for a ladder tournament
    # Basically it creates database tables.
    print p("Start of createladder_data") if $DEBUG;

# Collect the data from the passed array and then grap the variables we will need
# --------------------------------------------------------------------------------
    my @the_shiai_data = @_;               # This is the data transfered to us
    my $shiai_ID       = $the_shiai_data[1]
        ; # A scaler to carry the id of this new shiai, used for nameing that data tables.

    # create the scalers we need to use in the sql
    # ----------------------------------------------
    my $ladder_table
        = "data/shiai_data/"
        . $shiai_ID
        . "_ldr";    # eg: data/shiai_data/userTest.ldr the ladder itself
    my $history_table   = "data/shiai_data/" . $shiai_ID . "_hst";
    my $challenge_table = "data/shiai_data/" . $shiai_ID . "_chal";
    print p( " table name = ", $ladder_table ) if $DEBUG;
    # Okay now we must create the database files (three)
    # here is the DBI/SQL code
    # ----------------------------------------------------

# First create the array and hash to hold the table fields and data definitions
# ------------------------------------------------------------------------------
    my @ladder_fields
        = qw/ player_name ID position fights wins joined_date date_last_fight /;
    my %ladder_field_def = (
        player_name     => 'char(20)',
        ID              => 'char(20)',
        position        => 'char(20)',
        fights          => 'char(20)',
        wins            => 'char(20)',
        joined_date     => 'char(20)',
        date_last_fight => 'char(20)'
    );
    my @history_fields    = qw/ date_time activity description /;
    my %history_field_def = (
        date_time   => 'char(20)',
        activity    => 'char(20)',
        description => 'char(20)'
    );

    my @challenge_fields    = qw/ challenger opponent_id accepted /;
    my %challenge_field_def = (
        challenger  => 'char(20)',
        opponent_id => 'char(20)',
        accepted    => 'char(20)'
    );

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        or die "Can not create database connection";

    # build the LADDER table using SQL
    # ---------------------------------
    $dbh->do(
        "CREATE TABLE ladder ("
            . join( ',',
            map { $_ . ' ' . $ladder_field_def{$_} } @ladder_fields )
            . ")"
    ) or die "Can not create table";

    unlink $ladder_table;    # delete existing csv file if any
    $dbh->func( 'ladder', 'CSV', $ladder_table, 'ad_export' );

    print p("Ladder table created") if $DEBUG;

    # build the HISTORY table using SQL
    # ---------------------------------
    $dbh->do(
        "CREATE TABLE history ("
            . join( ',',
            map { $_ . ' ' . $history_field_def{$_} } @history_fields )
            . ")"
    ) or die "Can not create table";

    unlink $history_table;    # delete existing csv file if any
    $dbh->func( 'history', 'CSV', $history_table, 'ad_export' );

    print p("History table created") if $DEBUG;

    # build the CHALLENGE table using SQL
    # ---------------------------------
    $dbh->do(
        "CREATE TABLE challenge ("
            . join( ',',
            map { $_ . ' ' . $challenge_field_def{$_} } @challenge_fields )
            . ")"
    ) or die "Can not create table";

    unlink $challenge_table;    # delete existing csv file if any
    $dbh->func( 'challenge', 'CSV', $challenge_table, 'ad_export' );

    print p("Challenge table created") if $DEBUG;

    $dbh->disconnect();

    print p("END of create_ladder_data") if $DEBUG;

}

# end of subroutines
# -------------------

# main code block
# ---------------

print header(), start_html("e-Judo Test Area"),
    h1("CREATE NEW SHIAI");   # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p( "parameters: ", param() ) if $DEBUG;
#   print p("no parameters so print the form") if !(param());

#
if ( param("id") )
{ # the ID parameter should be present when they first arrive and not when the form is filled in, so if it does exist we need to do the lines below
    print p(
        "param:id exists, check the judoka limit against the number of judokas created for this user - START"
    ) if $DEBUG;

    my $user_id = param("id")
        ; # This line collects the user ID passed from the main menu identifying the user.
    my @user_data = get_user_data($user_id)
        ; # This line calls a sub routine which collects the user data from the user database
    print p("User Data = @user_data")
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.
    my $shiai_limit
        = $user_data[12];    # This collects the Judoka limit from the array
    print p("Shiai Limit = $shiai_limit")
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.
    my $shiai_count = shiai_count($user_id)
        ; # This line calls the subroutine that gets all the users Judoka Data

    if ( $shiai_count >= $shiai_limit )
    { # If they have already created all the Judoka they are allowed return to main menu
        print p("SORRY!!, Shiai Limit reached.");
        print p("You can create a new Shiai");
        print p(
            "-> <a href=main_menu.cgi?id=$user_id>Click HERE to continue</a>"
        );

    } # if the User has NOT entered any data then call the form and add user to the DB
    print p("yes, Shiai Count not reached, print the form") if $DEBUG;
    print_shiai_data_form($user_id)
        ; # Call the sub routine which shows the user form to create a new Judoka
}
else {
    my @temp_data  = collect_shiai_data();
    my @temp_data2 = validate_shiai_data(@temp_data)
        ;    # Call the subroutine to validate the users input
    my @temp_data3 = generate_initial_values(@temp_data2)
        ; # Create the initial values for the other fields not entered by users before adding to DB
    add_shiai_to_db(@temp_data3)
        ;    # Call the sub routine to add the Judo to the DB
    create_shiai_db_files(@temp_data3);

}

print end_html;    # this closes the web page properly
print p("End of main block") if $DEBUG;

