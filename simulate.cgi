#!/usr/bin/perl -w

# ---------------------------------------------
# simulate.cgi   - Create by Lance Wicks
#
# (C) 2004, Lance Wicks. All Rights Reserved
#
# Description:
#
# History:
# ========
# 17 August 2004, Lance Wicks - Initial File created as prototype
#
#
# Steps
# --------
#
#
#

# Scripts header    -   Standard settings for all scripts
# ---------------------------------------------------------------
    my $DEBUG = 0;                                  #  If this is set to 1 then we see the debug messages.

       my $shiai_id = "lw1";    # Hard coding for now.

    my $max_post = 51_200;			    #  To have messages appear use the following example in the code: print p("message in debug only") if $DEBUG;
    use strict; # force strict programming controls
    use CGI; # use the CGI.PM module

    $CGI::DISABLE_UPLOADS = 1;                          # Disable uploads
    $CGI::POST_MAX        = $max_post;                  # Maximum number of bytes per post


    use lib './MyLib';                                  # use the modules in MyLib, this is the DBD::Anydata used for database activities
    use DBI;                                            # This calls the DBI module, which along with the line above allows us to do database activities

    use Benchmark;

    my $query = CGI->new();          # Start a new cgi object

# Initialise variables for this scripts
# --------------------------------------------

my $judoka_id;
my $judoka_name;


# -------------------------------------------


# ---------------------------------------------------
# Sub-routines
# ---------------------------------------------------


sub find_challenge {

   my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";
   print $query->p("challenge_Table: ", $challenge_table) if $DEBUG;

   # next we need to make a connection to the challenge_table CSV file
   # ---------------------------------------------------------------

     print $query->p("Accessing the challenge_DB")if $DEBUG;


     # attached to the ladder table and enter the Judoka
     # -------------------------------------------------
     my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
     $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog'); # Connect to the judoka_csv data file

     my $sql = "SELECT * FROM challenge_db";       # this is the SQL command we want to execute.
     
     my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
     $sth->execute();                            # excecute the SQL using our parameters
     my @sql_returned;
     while (@sql_returned=$sth->fetchrow_array) {
           print $query->p("Challenge_Found: ",@sql_returned) if $DEBUG;
           if ($sql_returned[2] eq "Yes") {
              print $query->p("go go simulation engine!!") if $DEBUG;
              my @player1 = get_player_data($sql_returned[0]);
              print $query->p("Player1 Data = ",@player1) if $DEBUG;
              my @player2 = get_player_data($sql_returned[1]);
              print $query->p("Player2 Data = ",@player2) if $DEBUG;

              my $result = fight(@player1, @player2);
              print $query->h2($result) if $DEBUG;


           }else{
                  	print $query->p("THIS CHALLENGE HAS NOT BEEN ACCEPTED") if $DEBUG;
           }

      }



     $dbh->disconnect();










}

sub read_judoka_data {
# This sub reads in all the data from the database.
# --------------------------------------------------
print $query->p("Start read_judoka_data") if $DEBUG;


my @passed_info = @_;                                                              # Takes the values passed to us and assign them to a scaler
my $judoka_id = $passed_info[0];                                                     # this is the users id passed to us, we create this scaler just to make the script easier to understand
print $query->p("judoka_id = ", $judoka_id) if $DEBUG;
my @judoka_data;
print $query->p("passed info: ", @passed_info) if $DEBUG;

             # Use DBI to connect to the judoka_csv datafile
             #-----------------------------------------------
             my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog'); # Connect to the users_csv data file

             # select from the datafile the id for the user ID from the array paased from the previous sub routine
             my $sql_query = "SELECT * FROM judoka WHERE judoka_id = ?";       # this is the SQL command we want to execute
             my $sql_params = ($judoka_id);                          # Theese are the parameteres we will use in the SQL command above
             print $query->p("$sql_query\n[$sql_params]\n") if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth = $dbh->prepare( $sql_query );                     # prepare the SQL command
             $sth->execute( $sql_params );                            # excecute the SQL using our parameters

             my @result = $sth->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS
             $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

             print $query->p("result = ", @result)if $DEBUG;                # Prints the result of our SQL command if we are in debug mode.



             print $query->p("Judoka data = ", @result) if $DEBUG;


             return(@result);



print $query->p("End read_judoka_data") if $DEBUG;
}



sub get_player_data {
    my @internal_data = @_;
    print $query->p("data passed to GET_PLAYER_DATA = ",@internal_data) if $DEBUG;
    my @player = read_judoka_data($internal_data[0]);
    print $query->p("Player Data  = ",@player) if $DEBUG;
    return (@player);
}

sub fight {
   my @passed_info = @_;                                                              # Takes the values passed to us and assign them to a scaler
   print $query->h4("fight data passed = ",@passed_info) if $DEBUG;
   my $length_of_array = @passed_info / 2;
   print $query->h4("Number of variables = ",$length_of_array) if $DEBUG;
   print $query->h3($passed_info[2]," Vs. ",$passed_info[125]);

   my $count;

   my $player1_total_stats= 0;
   my $player2_total_stats= 0;

   for ($count=14; $count<123; $count++) {
        #       print $query->p("Stat -> ",$count," <-> ",$passed_info[$count]);
               $player1_total_stats += $passed_info[$count];
        }
    print $query->p("Player1 Total Stats -> ",$player1_total_stats) if $DEBUG;

    for ($count=137; $count<246; $count++) {
        #       print $query->p("Stat -> ",$count," <-> ",$passed_info[$count]);
               $player2_total_stats += $passed_info[$count];
        }
    print $query->p("Player2 Total Stats -> ",$player2_total_stats)if $DEBUG;


   srand(time);
   my $rnd_fighter1 = int(rand($player1_total_stats+20));
   my $rnd_fighter2 = int(rand($player2_total_stats+20));
   print $query->p("Player1 random -> ",$rnd_fighter1," vs. ",$rnd_fighter2," <- Player2 random") if $DEBUG;
   my $result;
   if ( $rnd_fighter1 > $rnd_fighter2 ) {
                                        	# player1 wins
                                        	    print $query->p("Player1 WINS ");
                                        	    $result = "Player1 WINS ";
                                                    update_stats($passed_info[1],$passed_info[124]);
                                                    remove_challenge(@passed_info);
   }

   if ( $rnd_fighter1 < $rnd_fighter2 ) {
                                        	# player2 wins
                                        	print $query->p("Player2 WINS ");
                                        	$result = "Player2 WINS ";
                                        	update_stats($passed_info[124],$passed_info[1]);
                                        	remove_challenge(@passed_info);
   }

   if ( $rnd_fighter1 == $rnd_fighter2 ) {
                                        	# draw
                                        	print $query->p("A Draw!");
                                        	$result = "Its a Draw";
   }

 #  remove_challenge(@passed_info);



   return($result);
}

sub update_stats {
  # $internal_user_data[10] = wins
  # $internal_user_data[11] = losses
  # $internal_user_data[14] = strength
  my @internal_data = @_;
  print $query->p("Data Passed to update_stats = ",@internal_data) if $DEBUG;

  my $winner = $internal_data[0];
  my $loser = $internal_data[1];


my @judoka_data;

             # Use DBI to connect to the judoka_csv datafile
             #-----------------------------------------------
             my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog'); # Connect to the users_csv data file

             # select from the datafile the id for the user ID from the array paased from the previous sub routine
             my $sql_query = "SELECT * FROM judoka WHERE judoka_id = ?";       # this is the SQL command we want to execute
             my $sql_params = ($winner);                          # Theese are the parameteres we will use in the SQL command above
             print $query->p("$sql_query\n[$sql_params]\n") if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth = $dbh->prepare( $sql_query );                     # prepare the SQL command
             $sth->execute( $sql_params );                            # excecute the SQL using our parameters

             my @winner_data = $sth->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS

             print $query->p("result = ", @winner_data)if $DEBUG;                # Prints the result of our SQL command if we are in debug mode.

             # grab the number of wins and then add one to it and insert back into the DB
             my $wins = $winner_data[10] + 1;
             print $query->p("winner =",$winner," and Wins = ", $wins)if $DEBUG;
             my $sql_insert ="UPDATE judoka SET wins = ? WHERE judoka_id = ?";
             my @sql_insert_params = ($wins,$winner);
             print $query->p("$sql_insert\n[@sql_insert_params]\n") if $DEBUG;                 # if we are in debug mode print the SQL statement
             $sth = $dbh->prepare( $sql_insert );                     # prepare the SQL command
             $sth->execute( @sql_insert_params );                            # excecute the SQL using our parameters

             # Grab the winners strength data and update by say 10?
             my $strength = $winner_data[14] +10;
             print $query->p("winner =",$winner," and strength = ", $strength)if $DEBUG;
             my $sql_strength ="UPDATE judoka SET strength = ? WHERE judoka_id = ?";
             my @sql_strength_params = ($strength,$winner);
             print $query->p("$sql_strength\n[@sql_strength_params]\n") if $DEBUG;
             $sth = $dbh->prepare( $sql_strength );
             $sth->execute( @sql_strength_params );




             # okay give the loser some stats
             $sql_query = "SELECT * FROM judoka WHERE judoka_id = ?";
             $sql_params = ($loser);
             print $query->p("$sql_query\n[$sql_params]\n") if $DEBUG;
             $sth = $dbh->prepare( $sql_query );
             $sth->execute( $sql_params );
             my @loser_data = $sth->fetchrow_array;
             print $query->p("result = ", @loser_data)if $DEBUG;
             my $losses = $loser_data[11] + 1;
             print $query->p("Loser =",$loser," and Losses = ", $losses)if $DEBUG;
             $sql_insert ="UPDATE judoka SET losses = ? WHERE judoka_id = ?";
             @sql_insert_params = ($losses,$loser);
             print $query->p("$sql_insert\n[@sql_insert_params]\n") if $DEBUG;
             $sth = $dbh->prepare( $sql_insert );
             $sth->execute( @sql_insert_params );
             $strength = $loser_data[14] +5;
             print $query->p("Loser =",$loser," and strength = ", $strength)if $DEBUG;
             $sql_strength ="UPDATE judoka SET strength = ? WHERE judoka_id = ?";
             @sql_strength_params = ($strength,$loser);
             print $query->p("$sql_strength\n[@sql_strength_params]\n") if $DEBUG;
             $sth = $dbh->prepare( $sql_strength );
             $sth->execute( @sql_strength_params );


             $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

             
             enter_history($winner_data[2], $loser_data[2]);






}


sub remove_challenge {
   my @info = @_;
   my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";
   print $query->p("challenge_Table: ", $challenge_table) if $DEBUG;

      # next we need to make a connection to the challenge_table CSV file
      # ---------------------------------------------------------------



                        print $query->p("about to remove the challenge")if $DEBUG;


                        # attached to the ladder table and enter the Judoka
                        # -------------------------------------------------
                        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
                        $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog'); # Connect to the judoka_csv data file

                        # add the data into a new record
                        my $sql = "DELETE FROM challenge_db WHERE challenger = ? ";       # this is the SQL command we want to execute, there SHOULD be 18 question marks

                        my @challenge_params = ($info[1]);                  # Make the parameters those passed to us from the previous routine (and originally from the user)
                        print $query->p("$sql\n[@challenge_params]\n") if $DEBUG;                 # if we are in debug mode print the SQL statement


                        my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
                        $sth->execute( @challenge_params );                            # excecute the SQL using our parameters

                        $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

                        print $query->p("Challenge removed") if $DEBUG;                 # just a reference in debug mode


}

sub enter_history {
# This subroutine enters the Judoka ID into the shiai
# ----------------------------------------------------------------------------------
#print p("Start enter_result_in_history") if $DEBUG;

      # create the scalers we need to use in the sql
      # ----------------------------------------------

      my $history_table = "data/shiai_data/" . $shiai_id . "_hst";     # eg: data/shiai_data/userTest_hst the ladder itself
#      print p("history_Table: ", $history_table) if $DEBUG;

      # next we need to make a connection to the history_table CSV file
      # ---------------------------------------------------------------

                        my @info = @_;

#                        print p("about to enter history")if $DEBUG;

                        # Okay we need to add the following fields into the table:
                        # ----------------------------------------------------------
                        # date_time - right now
                        # activity - short description
                        # description - long description

                        # first lets setup those scalers.
                        # --------------------------------------

                        my $date_time = gmtime();
                        my $activity = "Fight";
                        my $description = "$info[0] beat $info[1]";

                        # attached to the ladder table and enter the Judoka
                        # -------------------------------------------------
                        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
                        $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog'); # Connect to the judoka_csv data file

                        # add the data into a new record
                        my $sql = "INSERT INTO history_db VALUES ( ?,?,? )";       # this is the SQL command we want to execute, there SHOULD be 18 question marks

                        my @history_params = ($date_time, $activity, $description);                  # Make the parameters those passed to us from the previous routine (and originally from the user)
 #                       print "$sql\n[@history_params]\n" if $DEBUG;                 # if we are in debug mode print the SQL statement


                        my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
                        $sth->execute( @history_params );                            # excecute the SQL using our parameters

                        $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)

 #                       print p("History Created") if $DEBUG;                 # just a reference in debug mode






# print p("End enter_judoka_in_history") if $DEBUG;
}






 # ------




# ---------------------------------------------------
# Main Block
# ---------------------------------------------------

# Open a HTML page by printing headers using cgi.pm
# --------------------------------------------------
print $query->header( ),
      $query->start_html(-title=>'Simulate Fights'),
      $query->h1( "E-Judo Test Area - Simulate" );



                                  print $query->h1("SIMULATE");
                                  find_challenge();












# close the HTML page
# -----------------------
print $query->end_html;

# ------------------------------------------------
#  End of Main Block
# ------------------------------------------------
# EOF


