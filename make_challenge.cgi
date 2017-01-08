#!/usr/bin/perl -wT

# ---------------------------------------------
# make_challenge.cgi   - Create by Lance Wicks
#
# (C) 2004, Lance Wicks. All Rights Reserved
#
# Description:
#
# History:
# ========
# 19 may 2004, Lance Wicks - Initial File created as prototype
# 21 May 2004, Lance Wicks - Started new file, shall add skeleton to help chris get started.
#
#
# Steps
# --------
#
# 1. identify the judoka
# 2. identify what shiai/competitions they are entered in
# 3. identify other judoka in the shiai
# 4. identify other judoka available to challenge
# 5. display this list
# 6. user selects a judoka to challenge
# 7. make entry in challenge table
# 8. email challenged player (?)
#
#

# Scripts header    -   Standard settings for all scripts
# ---------------------------------------------------------------
    my $DEBUGx = 1;
    my $DEBUG = 0;                                  #  If this is set to 1 then we see the debug messages.
    my $max_post = 51_200;			    #  To have messages appear use the following example in the code: print p("message in debug only") if $DEBUG;
    use strict; # force strict programming controls
    use CGI; # use the CGI.PM module

    $CGI::DISABLE_UPLOADS = 1;                          # Disable uploads
    $CGI::POST_MAX        = $max_post;                  # Maximum number of bytes per post


    use lib './MyLib';                                  # use the modules in MyLib, this is the DBD::Anydata used for database activities
    use DBI;                                            # This calls the DBI module, which along with the line above allows us to do database activities


    my $query = CGI->new();          # Start a new cgi object

# Initialise variables for this scripts
# --------------------------------------------

my $judoka_id;
my $judoka_name;
my $shiai_id;


# -------------------------------------------


# ---------------------------------------------------
# Sub-routines
# ---------------------------------------------------

sub identify_judoka {
 print $query->h4("This is the identify_judoka sub") if $DEBUG;
 # do we need this?


 }

 # ------

 sub identify_shiai {
 print $query->h4("This is the identify_shiai sub") if $DEBUG;



 # In this sub we are finding what shiai this player is entered in
 #  Hmmm..... maybe we are approaching this all wrong?
 #  Does the Judoka only enter one shiai?



      my $ladder_table = "data/shiai_data/" . $shiai_id . "_ldr";     # eg: data/shiai_data/userTest.ldr the ladder itself
      print $query->p("ladder_Table: ", $ladder_table) if $DEBUG;

      # next we need to make a connection to the ladder_table CSV file
      # ---------------------------------------------------------------

             my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog'); # Connect to the users_csv data file

             # select from the datafile the id for the user ID from the array paased from the previous sub routine
             my $sql = "SELECT * FROM ladder_db";       # this is the SQL command we want to execute

             print "$sql\n\n" if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
             $sth->execute();                            # excecute the SQL using our parameters

             my @sql_returned;
             print $query->h2("Judoka Entered LIST") if $DEBUG;
             my $judoka_found_flag = 0;

             while (@sql_returned=$sth->fetchrow_array) {                       # This while loop continues till there is no more reults
                                                               print $query->p("Results = ", @sql_returned) if $DEBUG;
                                                               my $found_id = $sql_returned[1];          #create a scaler for tidiness which has the JudokaID
                                                               print $query->br($found_id) if $DEBUG;
                                                               if ( $judoka_id eq $found_id ) {
                                                                                              	$judoka_found_flag = 1;
                                                               }


                        }


             print $query->br($judoka_found_flag," - ",$shiai_id) if $DEBUG;





             $dbh->disconnect(); # we are done with the database for now, so disconnect from it (MAY NOT BE NECESSARY)
   print $query->p("end of Sub") if $DEBUG;
   return $shiai_id;

 }

 # ------

 sub identify_other_judoka {
 print $query->h4("This is the identify_other_judoka sub") if $DEBUG;

    # find all the players enterd in the shiai from the DB
   my @passed_data = @_;
   print $query->p("Passed data =",@passed_data) if $DEBUG;

      my $the_ladder_table = "data/shiai_data/" . $passed_data[0] . "_ldr";     # eg: data/shiai_data/userTest.ldr the ladder itself
      print $query->p("ladder_Table: ", $the_ladder_table) if $DEBUG;

      # next we need to make a connection to the ladder_table CSV file
      # ---------------------------------------------------------------

             my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh->func( 'ladder_db', 'CSV', $the_ladder_table, 'ad_catalog'); # Connect to the users_csv data file

             # select from the datafile the id for the user ID from the array paased from the previous sub routine
             my $sql = "SELECT * FROM ladder_db";       # this is the SQL command we want to execute

             print "$sql\n\n" if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
             $sth->execute();                            # excecute the SQL using our parameters

             my @sql_returned;
             print $query->h4("Judoka Entered in Shiai ") if $DEBUG;

             my @judoka_list;
             my @judoka_names;
             my $counter = 0;
             while (@sql_returned=$sth->fetchrow_array) {                       # This while loop continues till there is no more reults
                                                               print $query->p("Results = ", @sql_returned) if $DEBUG;
                                                               my $found_id = $sql_returned[1];          #create a scaler for tidiness which has the JudokaID
                                                               my $found_name = $sql_returned[0];          #create a scaler for tidiness which has the JudokaID

                                                               if ($found_id ne $judoka_id) {
                                                                      	$judoka_list[$counter] = $found_id;
                                                                      	$judoka_names[$counter] = $found_name;
                                                                      	print $query->br($counter," - ",$judoka_list[$counter]) if $DEBUG;
                                                                      	print $query->br($found_name) if $DEBUG;
                                                                      	$counter = $counter + 1;
                                                               } else {
                                                                        print $query->br($found_name," (You)") if $DEBUG;
                                                               }


                        }


   print $query->br("Judoka list : ",@judoka_list) if $DEBUG;
   print $query->br("Judoka names list : ",@judoka_names) if $DEBUG;


             $dbh->disconnect(); # we are done with the database for now, so disconnect from it (MAY NOT BE NECESSARY)
   print $query->p("end of Sub") if $DEBUG;

   return @judoka_list,@judoka_names;




 }

 # ------

 sub identify_available_judoka {
 print $query->h4("This is the identify_available_judoka sub") if $DEBUG;
   # This sub is passed a list of all other Judoka in the shiai.
   # It returns a list of judoka you can challenge, based on what criteria?
   my @passed_list = @_;         # Accept the array/list of judoka passed to us.

   my $count = @passed_list;
   my $number_of_judoka = $count / 2;
   print $query->p("The number of entries in the passed list was :", $count) if $DEBUG;
   print $query->p("The number of JUDOKA in the passed list was :", $number_of_judoka) if $DEBUG;

   # The following are just for testing
   # -------------------------------------
   my @temp = @passed_list[$number_of_judoka..$count];
   print $query->p("The JUDOKA in the passed list are :", @temp) if $DEBUG;

   my @temp2 = @passed_list[0..$number_of_judoka-1];
   print $query->p("The JUDOKA_IDs in the passed list are :", @temp2) if $DEBUG;

   # --------------------------------------

   my @available_list = @passed_list;          #Just a cheat to make this work before the code goes in.




   return @available_list;       # Return the list of judoka available to challenge.
 }


 # ------

 sub display_list {
 print $query->h4("This is the display_list sub") if $DEBUG;
    # Print a list of the available players to challenge with links to challenge them (calling this script again but with an extra parameter)
    my @incoming_list = @_;
       print $query->br("Incoming List : ",@incoming_list) if $DEBUG;


       # take the list and work out how many entries there are.
       # The list is in fact two lists, names the IDs. So divide the total by two.
       my $item_count = @incoming_list;
       my $judoka_number = $item_count / 2;

        print $query->p("The number of entries in the passed list was :",$item_count) if $DEBUG;
        print $query->p("The number of JUDOKA in the passed list was :",$judoka_number) if $DEBUG;

        my @judoka_names = @incoming_list[$judoka_number..$item_count];
        print $query->p("The JUDOKA in the passed list are :", @judoka_names) if $DEBUG;

        my @judoka_ids = @incoming_list[0..$judoka_number-1];
        print $query->p("The JUDOKA_IDs in the passed list are :", @judoka_ids) if $DEBUG;

        my $loop=0;
        for ( $loop = 0; $loop ne $judoka_number; $loop++ ) {
             print $query->p($judoka_names[$loop]) if $DEBUG;
             my $this_url = $query->self_url();
             print $query->p($this_url) if $DEBUG;
             my $link_url = $this_url . "&challenge=" . $judoka_ids[$loop];
             print $query->p($link_url) if $DEBUG;
             print $query->p($query->a({-href=>$link_url},$judoka_names[$loop]));
        }

 }


 # ------

 sub enter_in_database {
 print $query->h4("This is the enter_in_database sub") if $DEBUG;
   # add entries in the challenge database and history database etc.


   my $opponent_id = $query->param("challenge");
   print $query->p("judoka you are challenging =",$opponent_id) if $DEBUG;

   # Challenge database fields = challenger opponent_id
   my $challenger = $judoka_id;

   # Accepted database field = 0 for unaccepted. 1 for accepted. (Default should be 0)
   my $accepted = "Yes";

   my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";
   print $query->p("challenge_Table: ", $challenge_table) if $DEBUG;

      # next we need to make a connection to the challenge_table CSV file
      # ---------------------------------------------------------------



                        print $query->p("about to enter the challenge")if $DEBUG;


                        # attached to the ladder table and enter the Judoka
                        # -------------------------------------------------
                        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
                        $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog'); # Connect to the judoka_csv data file

                        # add the data into a new record
                        my $sql = "INSERT INTO challenge_db VALUES ( ?,?,? )";       # this is the SQL command we want to execute, there SHOULD be 18 question marks

                        my @challenge_params = ($challenger, $opponent_id, $accepted);                  # Make the parameters those passed to us from the previous routine (and originally from the user)
                        print $query->p("$sql\n[@challenge_params]\n") if $DEBUG;                 # if we are in debug mode print the SQL statement


                        my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
                        $sth->execute( @challenge_params );                            # excecute the SQL using our parameters

                        $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

                        print $query->p("Challenge Entered");                 # just a reference in debug mode









 }

 # ------


 sub enter_chal_in_history {
 print $query->h4("This is the sub that enters the challenge into the history") if $DEBUG;

 }


 # ------



 # ------


 sub email_confirmation {
 print $query->h4("This is the email_confirmation sub") if $DEBUG;
 print $query->p("We are not presently emailing the users") if $DEBUG;
      # eventually, use this to sendmail the challenge to the user.
 }


 # ------




# ---------------------------------------------------
# Main Block
# ---------------------------------------------------

# Open a HTML page by printing headers using cgi.pm
# --------------------------------------------------
print $query->header( ),
      $query->start_html(-title=>'Make Challenge'),
      $query->h1( "E-Judo Test Area - Make Challenge" );


if ($query->param){  # If there is a parameter the user has already been to this page and enetered something so do something with their input
                                  print $query->h1("A parameter was passed so do Subs to do stuff") if $DEBUG;


                                  # call sub routines

                                      $judoka_id = $query->url_param('judoka_id');
                                      $judoka_name = $query->url_param('judoka_name');
                                      $shiai_id = "lw1";                           # Setting this manually for now, needs to be a loop to access all Shiai at a later date.

                                      print $query->p("The Judoka_id passed is:", $judoka_id) if $DEBUG;
                                      print $query->p("The Judoka_name passed is:", $judoka_name) if $DEBUG;
                                      print $query->p("The Shiai_ID passed is:", $shiai_id) if $DEBUG;


                                  if ( $query->param("challenge") ) {
                                          print $query->p("challenge parameter exists") if $DEBUG;

                                          enter_in_database();
                                          enter_chal_in_history();
                                          email_confirmation();

                                  } else {



                                  identify_judoka();
                                  my @temp = identify_shiai();
                                  print $query->p("returned data =",@temp) if $DEBUG;
                                  print $query->p("returned scaler =",$temp[0]) if $DEBUG;
                                  my @returned_judoka_list = identify_other_judoka($temp[0]);
                                  print $query->p("The judoka list returned = ",@returned_judoka_list) if $DEBUG;
                                  my @available_judoka = identify_available_judoka(@returned_judoka_list);
                                  print $query->p("The availablejudoka list returned = ",@available_judoka) if $DEBUG;
                                  display_list(@available_judoka);

                                  }

             } else {      # if there are no parameters then the user is here for the first time so show them the data entry form.
                                  print $query->h1("No Parameters passed so there was a problem");
                                  print $query->p("we pass the judoka_id & Judoka_name to this script") if $DEBUG;
                                  print $query->h1("CLICK YOUR BACK BUTTON");

}








# close the HTML page
# -----------------------
print $query->end_html;

# ------------------------------------------------
#  End of Main Block
# ------------------------------------------------
# EOF


