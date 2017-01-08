#!/usr/bin/perl -w

# ---------------------------------------------
# create_judoka.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script adds a new Judoka to the Judoka database
#
# How does it work?
# =================
# We get the user data, and then the users Judoka data, if there Judoka Limit (from user data) is bigger than the number of Judoka records
# Then they are allowed to create a new Judoka and we do this, else they are told they can't create a new Judoka.
#
# History:
# ========
# 03 January 2004, Lance Wicks - File created
# 05 January 2004, Lance Wicks - Finished initial work, can now add records to the database successfully

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

sub judoka_count {
# This sub rotine gets the Judoka the user has from judoka_csv file and returns the number
    print p("START of get_judoka_data") if $DEBUG;

    my @internal_user_data = @_
        ; # This line takes the user_data passed to us from the previous routine (@_) and allocates it to our internal user data array
    my $entered_id = $internal_user_data[0]
        ; # just so that it is clearer later we create a variable from the passed data

    # Use DBI to connect to the users_csv datafile
    #-----------------------------------------------

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT * FROM judoka WHERE user_id = ?"
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

#my @result = $sth->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS
    $dbh->disconnect()
        ; # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)
    print p( "Number of entries for this user = ", $row_count ) if $DEBUG;
    return ($row_count);

    print p("END of get_judoka_data") if $DEBUG;

}

sub print_judoka_data_form {
# This subroutine create the user data web page which is filled in, the data is then used by other routines.
# Data fields: user_id,judoka_id,name,start_date,dojo,country,date_of_birth,weight,active,sensei,wins,losses,bio,password,strength,fitness,speed,ki,injury_level,injury_desc,total_shiai,earnings,cash,grade,retired,activity_points,experience_points,strategy_1,strategy_2,strategy_3,strategy_4,strategy_5,strategy_6,strategy_7,strategy_8,strategy_9,strategy_10,strategy_11,strategy_12,strategy_13,strategy_14,strategy_15,jami_juji_jime,gyaku_juji_jime,kata_juji_jime,hadaka_jime,okuri_eri_jime,kata_ha_jime,katate_jime,ryote_jime,sode_guruma_jime,tsukkomi_jime,sankaku_jime,ude_garami,ude_hishigi_juji_gatame,ude_hishigi_ude_gatame,ude_hishigi_hiza_gatame,ude_hishigi_waki_gatame,ude_hishigi_hara_gatame,ude_hishigi_ashi_gatame,ude_hishigi_te_gatame,ude_hishigi_sankaku_gatame,hon_kesa_gatame,kuzure_kesa_gatame,kata_gatame,kami_shiho_gatame,kuzure_kami_shiho_gatame,yoko_shiho_gatame,tate_shiho_gatame,de_ashi_harai,hiza_guruma,sasae_tsurikomi_ashi,uki_goshi,osoto_gari,o_goshi,ouchi_gari,seoi_nage,kosoto_gari,kouchi_gari,koshi_guruma,tsurikomi_goshi,okuri_ashi_harai,tai_otoshi,harai_goshi,uchi_mata,kosoto_gake,tsuri_goshi,yoko_otoshi,ashi_guruma,hane_goshi,harai_tsurikomi_ashi,tomoe_nage,kata_guruma,sumi_gaeshi,tani_otoshi,hane_makikomi,sukui_nage,utsuri_goshi,o_guruma,soto_makikomi,uki_otoshi,osoto_guruma,uki_waza,yoko_wakare,yoko_guruma,ushiro_goshi,ura_nage,sumi_otoshi,yoko_gake,morote_gari,kuchiki_taoshi,kibisu_gaeshi,uchi_mata_sukashi,tsubame_gaeshi,osoto_gaeshi,ouchi_gaeshi,kouchi_gaeshi,hane_goshi_gaeshi,harai_goshi_gaeshi,uchi_mata_gaeshi,osoto_makikomi,uchi_mata_makikomi,harai_makikomi
#                          *       *               *     *          *         *             *                 *
#                  0        1      2        3      4     5          6         7       8     9     10     11   12    13        14 ...
# All the fields with "*" under them are  generated by the user
# The numbers indicate their position in the array(s)

    print p("START of print_judoka_data_form") if $DEBUG;
    my @internal_user_data = @_;
    my $user_id_passed     = $internal_user_data[0];
    print p( "user ID passed = ", $user_id_passed ) if $DEBUG;
    print hr, start_form;    # create a form using CGI.PM
      #     print p("Judoka ID: ", textfield("judoka_id"), " - This is the unique ID for this Judoka");
    print p(
        "Judoka Full Name: ",
        textfield("judoka_name"),
        " - This is your Judoka name (fullname)"
    );
    print p( "Judoka Dojo: ",
        textfield("dojo"),
        " - This is the Dojo that your Judoka will belong to" );
    print p( "Judoka Country: ",
        textfield("country"),
        " - This is which country your Judoka is from" );
    print p(
        "Judoka Date of Birth: ",
        textfield("date_of_birth"),
        " - the date of birth (Fictional) for this Judoka."
    );
    print p( "Judoka Weight: ",
        textfield("weight"), " - the weight of your Judoka in Kilograms" );
    print p( "Judoka Sensei: ",
        textfield("sensei"),
        " - the name of the Sensei (fictional) who teaches your Judoka" );
    print p( "Judoka Biography: ",
        textfield("bio"),
        " - a brief biography of your Judoka, some backgrond info" );
    print hidden( -name => "user_id", -value => "$user_id_passed" );
    print submit( -name => 'submit button' );
    print end_form, hr;    # end the form
    print p("END of print_judoka_data_form") if $DEBUG;
}    # end of print_user_data_form

sub collect_judoka_data {
# This subroutine collects the user input from the form and returns it to the next form
    print p("Start of collect_judoka_data") if $DEBUG;

    my @judoka_data;
    $judoka_data[0] = param("user_id");
#   $judoka_data[1] = param ("judoka_id");    # Now take the parameters from the completed form and add them to the array
    $judoka_data[1] = "BLANK"
        ; # Now take the parameters from the completed form and add them to the array
    $judoka_data[2]  = param("judoka_name");
    $judoka_data[3]  = "blank";
    $judoka_data[4]  = param("dojo");
    $judoka_data[5]  = param("country");
    $judoka_data[6]  = param("date_of_birth");
    $judoka_data[7]  = param("weight");
    $judoka_data[8]  = "blank";
    $judoka_data[9]  = param("sensei");
    $judoka_data[10] = "blank";
    $judoka_data[11] = "blank";
    $judoka_data[12] = param("bio");
    print p( "Judoka_data array = ", @judoka_data ) if $DEBUG;
    return (@judoka_data);    # return the collected data
    print p("END of collect_judoka_data") if $DEBUG;
}

sub validate_judoka_data {
    # This sub routine validate the user input from collect_judoka_data
    print p("Start of validate_judoka_data") if $DEBUG;
    my @internal_user_data = @_
        ; # Take the array passed to this routine and assign it to an internal array

    print p( "validated data = ", @internal_user_data ) if $DEBUG;
    return (@internal_user_data);
    print p("END of validate_judoka_data") if $DEBUG;
}

sub generate_initial_values {
# This sub routinegenerates the variable data not inputed by the user (the initial variables)
# Data fields: user_id,judoka_id,name,start_date,dojo,country,date_of_birth,weight,active,sensei,wins,losses,bio,password,strength,fitness,speed,ki,injury_level,injury_desc,total_shiai,earnings,cash,grade,retired,activity_points,experience_points,strategy_1,strategy_2,strategy_3,strategy_4,strategy_5,strategy_6,strategy_7,strategy_8,strategy_9,strategy_10,strategy_11,strategy_12,strategy_13,strategy_14,strategy_15,jami_juji_jime,gyaku_juji_jime,kata_juji_jime,hadaka_jime,okuri_eri_jime,kata_ha_jime,katate_jime,ryote_jime,sode_guruma_jime,tsukkomi_jime,sankaku_jime,ude_garami,ude_hishigi_juji_gatame,ude_hishigi_ude_gatame,ude_hishigi_hiza_gatame,ude_hishigi_waki_gatame,ude_hishigi_hara_gatame,ude_hishigi_ashi_gatame,ude_hishigi_te_gatame,ude_hishigi_sankaku_gatame,hon_kesa_gatame,kuzure_kesa_gatame,kata_gatame,kami_shiho_gatame,kuzure_kami_shiho_gatame,yoko_shiho_gatame,tate_shiho_gatame,de_ashi_harai,hiza_guruma,sasae_tsurikomi_ashi,uki_goshi,osoto_gari,o_goshi,ouchi_gari,seoi_nage,kosoto_gari,kouchi_gari,koshi_guruma,tsurikomi_goshi,okuri_ashi_harai,tai_otoshi,harai_goshi,uchi_mata,kosoto_gake,tsuri_goshi,yoko_otoshi,ashi_guruma,hane_goshi,harai_tsurikomi_ashi,tomoe_nage,kata_guruma,sumi_gaeshi,tani_otoshi,hane_makikomi,sukui_nage,utsuri_goshi,o_guruma,soto_makikomi,uki_otoshi,osoto_guruma,uki_waza,yoko_wakare,yoko_guruma,ushiro_goshi,ura_nage,sumi_otoshi,yoko_gake,morote_gari,kuchiki_taoshi,kibisu_gaeshi,uchi_mata_sukashi,tsubame_gaeshi,osoto_gaeshi,ouchi_gaeshi,kouchi_gaeshi,hane_goshi_gaeshi,harai_goshi_gaeshi,uchi_mata_gaeshi,osoto_makikomi,uchi_mata_makikomi,harai_makikomi
#                          *       *               *     *          *         *             *                 *
#                  0        1      2        3      4     5          6         7       8     9     10     11   12    13        14 ...
# All the fields with "*" under them are  generated by the user
# The numbers indicate their position in the array(s)
# user_id is already in the data array at this stage.
    print p("Start of generate_initial_values") if $DEBUG;
    my @internal_user_data = @_
        ; # Take the array passed to this routine and assign it to an internal array
    $internal_user_data[1] = $internal_user_data[0]
        . $internal_user_data[2]
        ; # Make the unique ID for this Judoka the users ID plus the Judoka name.
    $internal_user_data[3]  = gmtime();    # Set start date to now
    $internal_user_data[8]  = "NO";        # ACTIVE - Set to no initially
    $internal_user_data[10] = 0;           # WINS - set to zero initially
    $internal_user_data[11] = 0;           # LOSSES - set to zero
    $internal_user_data[13]
        = "default";  # PASSWORD - set this to default (well at least for now)
    $internal_user_data[14] = 0;    # STRENGTH - set this to zero for now
    my $loop;                       # Initialise a variable to use for a loop

    for ( $loop = 15; $loop < 124; $loop++ )
    {    # Loop from 15 to the last variable (there are 123)
        $internal_user_data[$loop] = 0
            ;   # This line sets all the remaining variables in the array to 0
    }

    print p( "Validated data + initial values = ", @internal_user_data )
        if $DEBUG;
    return (@internal_user_data);
    print p("END of generate_initial_values") if $DEBUG;
}

sub add_judoka_to_db {
    print p("Start of add_judoka_to_db subroutine") if $DEBUG;

    my @internal_user_data = @_
        ; # This line takes the user_data passed to us from the previous routine (@_) and allocates it to our internal user data array
    my $entered_judoka_id = $internal_user_data[1]
        ; # just so that it is clearer later we create a variable from the passed data

    # Use DBI to connect to the judoka_csv datafile
    #-----------------------------------------------
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        ;    # tell DBI we want to use the Anydata module in ./MyLibs
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' )
        ;    # Connect to the users_csv data file

# select from the datafile the id for the user ID from the array paased from the previous sub routine
    my $sql = "SELECT * FROM judoka WHERE judoka_id = ?"
        ;    # this is the SQL command we want to execute
    my @params = ($entered_judoka_id)
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
        # if the judoka_id does not exist then add them!
        # so connect to the database
        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
            ;    # tell DBI we want to use the Anydata module in ./MyLibs
        $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' )
            ;    # Connect to the judoka_csv data file

        # add the data into a new record
        my $sql
            = "INSERT INTO judoka VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )"
            ; # this is the SQL command we want to execute, there SHOULD be 123 question marks
        my @params = (@internal_user_data)
            ; # Make the parameters those passed to us from the previous routine (and originally from the user)
#                        print "$sql\n[@params]\n" if $DEBUG;                 # if we are in debug mode print the SQL statement

        my $sth = $dbh->prepare($sql); # prepare the SQL command
        $sth->execute(@params);        # excecute the SQL using our parameters

        print p("Judoka Created");     # just a reference in debug mode
        print p(
            "-> <a href=http://www.judocoach.com/e-judo/main_menu.cgi?id=$internal_user_data[0];>Click HERE to continue</a>"
        );
    }
    print p("END of add_user_input_to_db") if $DEBUG;

    print p( "Data added to the DB = ", @internal_user_data ) if $DEBUG;
    print p("END of add_judoka_to_db subroutine") if $DEBUG;
}

# end of subroutines
# -------------------

# main code block
# ---------------

print header(), start_html("e-Judo Test Area"),
    h1("CREATE NEW JUDOKA");  # This line uses CGI.PM to to create the webpage
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
    my $judoka_limit
        = $user_data[11];    # This collects the Judoka limit from the array
    print p("Judoka Limit = $judoka_limit")
        if $DEBUG
        ;    # Prints the result of our SQL command if we are in debug mode.
    my $judoka_count = judoka_count($user_id)
        ; # This line calls the subroutine that gets all the users Judoka Data

    if ( $judoka_count >= $judoka_limit )
    { # If they have already created all the Judoka they are allowed return to main menu
        print p("SORRY!!, Judoka Limit reached.");
        print p("You can create no more Judoka");
        print p(
            "-> <a href=http://www.judocoach.com/e-judo/main_menu.cgi?id=$user_id>Click HERE to continue</a>"
        );

    } # if the User has NOT entered any data then call the form and add user to the DB
    print p("yes, Judoka Count not reached, print the form") if $DEBUG;
    print_judoka_data_form($user_id)
        ; # Call the sub routine which shows the user form to create a new Judoka
}
else {
    my @temp_data  = collect_judoka_data();
    my @temp_data2 = validate_judoka_data(@temp_data)
        ;    # Call the subroutine to validate the users input
    my @temp_data3 = generate_initial_values(@temp_data2)
        ; # Create the initial values for the other fields not entered by users before adding to DB
    add_judoka_to_db(@temp_data3)
        ;    # Call the sub routine to add the Judo to the DB

}

print end_html;    # this closes the web page properly
print p("End of main block") if $DEBUG;

