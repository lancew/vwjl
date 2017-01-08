#!/usr/bin/perl -w

# ---------------------------------------------
# view_shiai.cgi   - Create by Lance Wicks
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
# 10 January 2004, Lance Wicks - File created


    my $DEBUG = 0; #  If this is set to 1 then we see the debug messages.

# The following 4 lines set strict PERL coding then load the CGI DBI and DBD::Anydata modules.
# ---------------------------------------------------------------------------------------------
use strict; # force strict programming controls
use CGI qw(:standard); # use the CGI.PM module
use lib './MyLib'; # use the modules in MyLib, this is the DBD::Anydata used for database activities
use DBI; # This calls the DBI module, which along with the line above allows us to do database activities


# Sub routines
# --------------


sub read_shiai_data {
# This sub reads in all the data from the database.
# --------------------------------------------------
print p("Start read_shiai_data") if $DEBUG;


my @passed_info = @_;                                                              # Takes the values passed to us and assign them to a scaler
print p("passed info: ", @passed_info) if $DEBUG;

my $shiai_id = $passed_info[0];                                                     # this is the shiai passed to us, we create this scaler just to make the script easier to understand
print p("shiai_id = ", $shiai_id) if $DEBUG;
my @shiai_data;

             # Use DBI to connect to the shiai_csv datafile
             #-----------------------------------------------
             my $dbh1 = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh1->func( 'shiaidb', 'CSV', 'data/shiai_csv', 'ad_catalog'); # Connect to the users_csv data file

             # select from the datafile the full info for this shiai
             my $the_query = "SELECT * FROM shiaidb WHERE shiai_id = ?";       # this is the SQL command we want to execute
             my $the_params = ($shiai_id);                          # Theese are the parameteres we will use in the SQL command above
             print p("$the_query\n[$the_params]\n") if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth1 = $dbh1->prepare( $the_query );                     # prepare the SQL command
             $sth1->execute( $the_params );                            # excecute the SQL using our parameters

             my @query_result = $sth1->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS
             $dbh1->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)




            print p("Shiai data = ", @query_result) if $DEBUG;


             return(@query_result);



print p("End read_shiai_data") if $DEBUG;
}

sub display_shiai_data {
print p("Start display_shiai_data") if $DEBUG;
                         my @passed_info = @_;
                         print h1("Shiai: ",$passed_info[2]);
                         my $number_of_items = @passed_info;            # This tells us how many items are in the passed info ie how many data fields
                         print p("Number of variables =", $number_of_items) if $DEBUG;
                         # we need to connect to the shiai DB...
                         # ----------------------------------------------------------------

                         my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
                         $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog'); # Connect to the shiai_csv data file

                         # The following block gets the database headings...
                         # first make a simple query
                         my $sql_dataquery = "SELECT * FROM shiai_db";       # this is the SQL command we want to execute
                         print p("$sql_dataquery\n") if $DEBUG;                 # if we are in debug mode print the SQL statement

                         my $sth = $dbh->prepare( $sql_dataquery );                     # prepare the SQL command
                         $sth->execute();                            # excecute the SQL using our parameters

                         my @result = $sth->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS

                         # ...and then get the column headings
                         # --------------------------------
                         my @headings = @{$sth->{NAME}};
                         print p("Column headings = ", @headings) if $DEBUG;
                         my $number_of_headings = @headings;
                         print p("Number of headings = ", $number_of_headings) if $DEBUG;

                         $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)


                         # we now have to arrays @headings & @passed_info
                         # we need to present these in a table.


                         print ("<table width=85% border=1>");         # create a table

                         for (my $loop=2; $loop ne $number_of_headings; $loop++) {
                                                       print ("<TR><TD>$headings[$loop]</TD><TD>$passed_info[$loop]</TD>");
                                                       print ("<TD>$loop</TD>") if $DEBUG;
                                                       print ("</TR>");
                         }


                         print ("</table>");

print p("End display_shiai_data") if $DEBUG;
}


sub list_shiai {
# This subroutine opens the shiai database and finds all the shiai
# It then returns this list of names to the system, with a link to each.
# ----------------------------------------------------------------------------------
print p("Start list_shiai") if $DEBUG;
my @passed_info = @_;                                                              # Takes the values passed to us and assign them to a scaler
my $user_id = $passed_info[0];                                                     # this is the users id passed to us, we create this scaler just to make the script easier to understand
print p("passed_id: ", @passed_info) if $DEBUG;
my @shiai_found;                                                                # initialise the array where we shall collect the judoka information
# next we use DBI to connect to the judoka_csv datafile
#-----------------------------------------------
             my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog'); # Connect to the shiai_csv data file

# Next we collect all the shiai IDs and names from the db
             my $sql = "SELECT shiai_id,name FROM shiai_db";       # this is the SQL command we want to execute

             print "$sql\n" if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
             $sth->execute();                            # excecute the SQL using our parameters

             my @sql_returned;
             print h2("SHIAI LIST");
             while (@sql_returned=$sth->fetchrow_array) {                       # This while loop continues till there is no more reults
                                                               print p("Results = ", @sql_returned) if $DEBUG;
                                                               my $shiai_id = $sql_returned[0];          #create a scaler for tidiness which has the JudokaID
                                                               my $shiai_name = $sql_returned[1];        #create a scaler for tidiness that is the name of the Judoka
                                                               print p("<a href=view_shiai.cgi?id=$user_id&shiai=$shiai_id>$shiai_name</a>");


                        }

             $dbh->disconnect();                                # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)


print p("End list_shiai") if $DEBUG;
}

sub show_players {
# This subroutine prints a list of players associated with this shiai
# ----------------------------------------------------------------------------------
print p("Start show players") if $DEBUG;



      # create the scalers we need to use in the sql
      # ----------------------------------------------
      my @passed_info = @_;                                                              # Takes the values passed to us and assign them to a scaler
      my $shiai_id = $passed_info[0];
      print p("passed_info: ", @passed_info) if $DEBUG;
      my $ladder_table = "data/shiai_data/" . $shiai_id . "_ldr";     # eg: data/shiai_data/userTest.ldr the ladder itself
      print p("ladder_Table: ", $ladder_table) if $DEBUG;

      # next we need to make a connection to the ladder_table CSV file
      # ---------------------------------------------------------------

             my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):'); # tell DBI we want to use the Anydata module in ./MyLibs
             $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog'); # Connect to the users_csv data file

             # select from the datafile the id for the user ID from the array paased from the previous sub routine
             my $sql = "SELECT * FROM ladder_db";       # this is the SQL command we want to execute
#             my $params = ($judoka_id);                          # Theese are the parameteres we will use in the SQL command above
             print "$sql\n\n" if $DEBUG;                 # if we are in debug mode print the SQL statement

             my $sth = $dbh->prepare( $sql );                     # prepare the SQL command
             $sth->execute();                            # excecute the SQL using our parameters

#             my @result = $sth->fetchrow_array; # this line takes the results of the select and puts it in the array called RESULTS
 

              my @sql_returned;
             print h2("Judoka Entered LIST");
             while (@sql_returned=$sth->fetchrow_array) {                       # This while loop continues till there is no more reults
                                                               print p("Results = ", @sql_returned) if $DEBUG;
                                                               my $name = $sql_returned[0];          #create a scaler for tidiness which has the JudokaID
                                                               print br($name);


                        }







             $dbh->disconnect(); # we are done with the datbase for now, so disconnect from it (MAY NOT BE NECESSARY)
#
#             print p("result = ", @result)if $DEBUG;                # Prints the result of our SQL command if we are in debug mode.
#
#
#
#



print p("End show_players") if $DEBUG;
}





# ------------------
# End of Subroutines


# Main Code Block
# ----------------

print header(), start_html("e-Judo Test Area"), h1("VIEW SHIAI"); # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p("parameters: ", param()) if $DEBUG;
print p("values: ", param("id")) if $DEBUG;


if ( param("id") ) {                                                            # the ID parameter should be present when they first arrive and not when the form is filled in, so if it does exist we need to do the lines below
  if ( param("shiai") ) {                                                      # if the Shiai parameter exists then the user has selected a shiai to view
                        my $shiai = param("shiai");
                        print p("Shiai parameter = ", $shiai) if $DEBUG;
                        my @shiai_info = read_shiai_data($shiai);    # Call the subroutine to collect the judoka data from the database and assign it to an array
                        print ("The Shiai returned = ", @shiai_info) if $DEBUG;
                        display_shiai_data(@shiai_info);                      # Take the data collected and display it
                        show_players($shiai);
  } else {                                                                      # If the judoka parameter does not exist then we need to find all the users judoka and allow them to select one to view
                        list_shiai( param("id"));                                      # This line calls the sub that lists the users Judoka (with links to view the selected Judoka)
        }                                                                       # End of the if statement related to the Judoka parameter
} else {                                                                        # If the id parameter does not exist they should not be here so display a link to the front page (e-judo.cgi)
        print p("Problem!");
        print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
        }




print p("END main block") if $DEBUG;

# --------------------
# End of Main Block

