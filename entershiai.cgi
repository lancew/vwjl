#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;

print header(); 
print start_html("e-Judo Test Area");
print h1("Enter Shiai"); 

if ( param("judoka_id") ) { 
    if ( param("shiai") ) { 
        my $shiai       = param("shiai");
        my $judoka      = param("judoka_id");
        my $judoka_name = param("judoka_name");

        my @data_to_pass = ( $shiai, $judoka, $judoka_name );
        enter_judoka_in_ladder(@data_to_pass);
    }
    else {    
        my $judoka       = param("judoka_id");
        my $judoka_name  = param("judoka_name");
        my @data_to_pass = ( $judoka, $judoka_name );
        list_shiai(@data_to_pass);
    }    
}
else { 
    print p("Problem!");
    print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
}


sub list_shiai {
    my @passed_info = @_; 
    my $judoka_id   = $passed_info[0];
    my $judoka_name = $passed_info[1];

    my @shiai_found;
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' );

    my $sql = "SELECT shiai_id,name FROM shiai_db";

    my $sth = $dbh->prepare($sql);
    $sth->execute();              

    print h2("SHIAI LIST");
    while ( my @sql_returned = $sth->fetchrow_array ) {
        my $shiai_id = $sql_returned[0];
        my $shiai_name = $sql_returned[1];
        print p(
            "<a href=entershiai.cgi?judoka_id=$judoka_id&shiai=$shiai_id&judoka_name=$judoka_name>$shiai_name</a>"
        );
    }

    $dbh->disconnect();
}

sub enter_judoka_in_ladder {
    my @passed_info = @_;
    my $shiai_id    = $passed_info[0];
    my $judoka_id   = $passed_info[1];
    my $judoka_name = $passed_info[2];
    
    my $ladder_table
        = "data/shiai_data/"
        . $shiai_id
        . "_ldr";
        
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog' );

    my $sql = "SELECT id FROM ladder_db WHERE id = ?";
    my $params = ($judoka_id);

    my $sth = $dbh->prepare($sql);    
    $sth->execute($params);           
    
    my @result = $sth->fetchrow_array;
    $dbh->disconnect();

    if (@result) {
        print h2("this Judoka is already entered!");
    }
    else {
        my $player_name     = $judoka_name;
        my $ID              = $judoka_id;
        my $position        = 0;
        my $fights          = 0;
        my $wins            = 0;
        my $joined_date     = gmtime();
        my $date_last_fight = "no Fights";

        my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
        $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog' );

        my $sql = "INSERT INTO ladder_db VALUES ( ?,?,?,?,?,?,? )";

        my @ladder_params = (
            $player_name, $ID, $position, $fights, $wins, $joined_date,
            $date_last_fight
            )
            ;

        my $sth = $dbh->prepare($sql);
        $sth->execute(@ladder_params);
        
        $dbh->disconnect();

        my @data_to_pass = ( $shiai_id, $judoka_id, $judoka_name );
        enter_judoka_in_history(@data_to_pass);

        print p("Player Entered");
    }
}

sub enter_judoka_in_history {
    my @passed_info = @_;
    my $shiai_id    = $passed_info[0];
    my $judoka_id   = $passed_info[1];
    my $judoka_name = $passed_info[2];
    
    my $history_table
        = "data/shiai_data/"
        . $shiai_id
        . "_hst";
        
    my $date_time   = gmtime();
    my $activity    = "Entry";
    my $description = "$judoka_name entered this shiai";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog' );

    my $sql = "INSERT INTO history_db VALUES ( ?,?,? )";
    my @history_params = ( $date_time, $activity, $description );

    my $sth = $dbh->prepare($sql);     
    $sth->execute(@history_params);    
    
    $dbh->disconnect();
}


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