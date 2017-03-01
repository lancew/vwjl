#!/usr/bin/perl -w
use strict;
use warnings;

our $DEBUG = 1;    #  If this is set to 1 then we see the debug messages.

use CGI qw(:standard);
use lib './MyLib';
use DBI;


# main code block
# ---------------

print header(), start_html("e-Judo Test Area"),
    h1("CREATE NEW USER");    # This line uses CGI.PM to to create the webpage

print p("Start main block") if $DEBUG;
print p( "parameters: ", param() ) if $DEBUG;
#   print p("no parameters so print the form") if !(param());
if ( param() )
{ # If there is a parameter(or parameters) then validate, else show the login screen.
        # the following lines are excecuted if paramaters HAVE been entered

    print p("collect user data ...") if $DEBUG;
    my @temp_variable = collect_user_input();
    print p("... gave us: ") if $DEBUG;

    print p("going to validate user input") if $DEBUG;
    my @temp_variable2 = validate_user_input(@temp_variable);
    print p("VALIDATED") if $DEBUG;
    # print p("validate user data gave us: @temp_variable2") if $DEBUG;

    print p("going to Add user data to DB") if $DEBUG;
    my @temp_variable3 = add_user_input_to_db(@temp_variable2);
    print p("added") if $DEBUG;
    # print p("add user data to db gave us: @temp_variable3") if $DEBUG;

}
else
{   # if there are no parameters (the form has not yet been filled in then....
    print_user_data_form();
}

print end_html;    # this closes the web page properly
print p("End of main block") if $DEBUG;

sub collect_user_input {
# This routine collects the data entered by the user from the form and adds the initial values and returns the @user_data array
# ---------------------------------------------------------------------
    print p("Start of collect_user_input") if $DEBUG;

    my @user_data
        ; # initialise the array we will use to store all these pieces of data
    $user_data[0] = param("id")
        ; # the next few lines alocate the info from the completed form to variables.
    print p("$user_data[0]") if $DEBUG;
    $user_data[1] = param("first_name");
    $user_data[2] = param("surname");
    $user_data[3] = param("date_of_birth");
    $user_data[4] = param("email");
    $user_data[5] = param("ejudopass");
    # now give values to the other user data field variables
    $user_data[6] = "NO"
        ; # ($active) the user is not immediately active, we will email them first.
    $user_data[7] = gmtime();    # ($last_login)set the last login time to now
    $user_data[8] = gmtime()
        ;    #($create_data) set the date we created this user to now as well
    $user_data[9] = 0
        ;   # ($earnings) They have not earned any thing yet so set it to Zero
    $user_data[10] = 50
        ; # ($cash) This is their cash on hand, lets give them 50 credits by default
    $user_data[11] = 99
        ; # ($judoka_limit) They can create 1 Judoka  ** Temporarily set to 99
    $user_data[12] = 99;  # ($sensei_limit) They can NOT create a sensei (YET)
    $user_data[13] = 0;   # ($dojo_limit) They can not create a Dojo
    $user_data[14] = 0;   # ($team_limit)They can not create a team
    $user_data[15] = "Novice";  # ($rank) They are a novice user to start with
    return @user_data;
    print p("END of collect_user_input") if $DEBUG;
}    # end of subroutine collect_user_data

sub validate_user_input {
# This sub routine receives the @user_data array from collect_user_input sub-routine, it validates it to make sure it is safe for the database, then return the @user_data array
# ----------------------------------------------------------------------------------
    print p("Start of validate_user_input") if $DEBUG;
    my @internal_user_data = @_;

    # add some data validation of user input here

    return @internal_user_data;
    print p("END of validate_user_input") if $DEBUG;

}    # end of sub routine validate_user_input

sub add_user_input_to_db {
# This routine receives @user_data from validate_user_input and then adds it to the Database using SQL
# ----------------------------------------------------------------------------------------------------
# Next connect to the database and check if they exist already.
    print p("Start of add_user_input_to_db") if $DEBUG;

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
    my $sql = "SELECT id FROM users WHERE id = ?"
        ;    # this is the SQL command we want to execute
    my @params = ($entered_id)
        ;    # Theese are the parameteres we will use in the SQL command above
    print "$sql\n[@params]\n"
        if $DEBUG;    # if we are in debug mode print the SQL statement

    my $sth = $dbh->prepare($sql);    # prepare the SQL command
    $sth->execute(@params);           # excecute the SQL using our parameters

    my @result = $sth->fetchrow_array
        ; # this line takes the results of the select and puts it in the array called RESULTS
    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

    print p("result = @result")
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.

    if (@result)
    {  #if the result array is in existence (ie we found the username) then...
        print p("Sorry this ID is in use already");

    }
    else {

        print p("about to insert the new record") if $DEBUG;
        # if the user does not exist then add them!
        # so connect to the database
        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
            ;    # tell DBI we want to use the Anydata module in ./MyLibs
        $dbh->func( 'users', 'CSV', 'data/users_csv', 'ad_catalog' )
            ;    # Connect to the users_csv data file

        # add the data into a new record
        my $sql
            = "INSERT INTO users VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )"
            ;    # this is the SQL command we want to execute
        my @params = (@internal_user_data)
            ; # Make the parameters those passed to us from the previous routine (and originally from the user)
#                        print "$sql\n[@params]\n" if $DEBUG;                 # if we are in debug mode print the SQL statement

        my $sth = $dbh->prepare($sql); # prepare the SQL command
        $sth->execute(@params);        # excecute the SQL using our parameters

        print p("User Created");       # just a reference in debug mode
        print p(
            "-> <a href='e-judo.cgi'>Click HERE to continue</a>"
        );
    }
    print p("END of add_user_input_to_db") if $DEBUG;
}    # end of sub routine add_user_input_to_db

sub print_user_data_form {
# This subroutine create the user data web page which is filled in, the data is then used by other routines.
    print p("START of print_user_data_form") if $DEBUG;
    print hr, start_form;    # create a form using CGI.PM
    print p( "User ID: ", textfield("id"),
        " - This is the ID you will use to login to the system" )
        ;                    # what username do they want.
    print p( "First Name: ", textfield("first_name"),
        " - This is your REAL name" );    # what is their real name
    print p( "Surname: ", textfield("surname"),
        " - This is your REAL last name" );    # what is their real name
    print p(
        "Date of Birth: ",
        textfield("date_of_birth"),
        " - (DD/MM/YYYY) This is your date of birth, used if you ever need to prove who you are"
    );
    print p( "Email address: ",
        textfield("email"), " - the email address you would like to use." );
    print p(
        "Password: ",
        password_field("ejudopass"),
        " - Choose a password to use on the system"
    );
    print submit( -name => 'submit button' );
    print end_form, hr;    # end the form
    print p("END of print_user_data_form") if $DEBUG;
}    # end of print_user_data_form

# end of subroutines
# -------------------






# ---------------------------------------------
# create-user.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script adds a new user to the users database
#
# History:
# ========
# 20 December 2003, Lance Wicks - Created initial file.
# 23 December 2003, Lance Wicks - On the suggestion of Jeff Zucker, am re-writing this code to use more sub-routines and some other good suggestions.
# 02 January 2004, Lance Wicks - Finally finished this module, is now working, still need to add input validation and user notification etc.
# 01 March 2016, Lance Wicks - Restarting the project
