#!/usr/bin/perl -w
use strict;
use warnings;

use CGI;
$CGI::DISABLE_UPLOADS = 1;         # Disable uploads
$CGI::POST_MAX        = 51_200;    # Maximum number of bytes per post

use lib './MyLib';
use DBI;

my $query = CGI->new();            # Start a new cgi object

my $judoka_id;
my $judoka_name;

print $query->header();
print $query->start_html( -title => 'Simulate Fights' );
print $query->h1("E-Judo Test Area - Simulate");
print $query->h1("SIMULATE");

find_challenge($query);
print $query->end_html;

# ---------------------------------------------------

sub find_challenge {
    my $query    = shift;
    my $shiai_id = "lancewlw1";    # Hard coding for now.
    my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog' );

    my $sql = "SELECT * FROM challenge_db";
    my $sth = $dbh->prepare($sql);
    $sth->execute();

    while ( my @sql_returned = $sth->fetchrow_array ) {
        if ( $sql_returned[2] eq "Yes" ) {
            my @player1 = get_player_data( $sql_returned[0] );
            my @player2 = get_player_data( $sql_returned[1] );

            my $result = fight( $query, @player1, @player2 );
        }
    }

    $dbh->disconnect();
}

sub read_judoka_data {
    my @passed_info = @_;
    my $judoka_id   = $passed_info[0];

    my @judoka_data;
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' );

    my $sql_query  = "SELECT * FROM judoka WHERE judoka_id = ?";
    my $sql_params = ($judoka_id);

    my $sth = $dbh->prepare($sql_query);
    $sth->execute($sql_params);

    my @result = $sth->fetchrow_array;
    $dbh->disconnect();

    return @result;
}

sub get_player_data {
    my @internal_data = @_;
    my @player        = read_judoka_data( $internal_data[0] );
    return @player;
}

sub fight {
    my $query           = shift;
    my @passed_info     = @_;
    my $length_of_array = @passed_info / 2;

    print $query->h3( $passed_info[2], " Vs. ", $passed_info[125] );

    my $count;

    my $player1_total_stats = 0;
    my $player2_total_stats = 0;

    for ( $count = 14; $count < 123; $count++ ) {
        $player1_total_stats += $passed_info[$count];
    }

    for ( $count = 137; $count < 246; $count++ ) {
        $player2_total_stats += $passed_info[$count];
    }

    srand(time);
    my $rnd_fighter1 = int( rand( $player1_total_stats + 20 ) );
    my $rnd_fighter2 = int( rand( $player2_total_stats + 20 ) );

    my $result;
    if ( $rnd_fighter1 > $rnd_fighter2 ) {
        print $query->p("Player1 WINS ");
        $result = "Player1 WINS ";
        update_stats( $passed_info[1], $passed_info[124] );
        remove_challenge(@passed_info);
    }

    if ( $rnd_fighter1 < $rnd_fighter2 ) {
        print $query->p("Player2 WINS ");
        $result = "Player2 WINS ";
        update_stats( $passed_info[124], $passed_info[1] );
        remove_challenge(@passed_info);
    }

    if ( $rnd_fighter1 == $rnd_fighter2 ) {
        # draw
        print $query->p("A Draw!");
        $result = "Its a Draw";
    }
    return $result;
}

sub update_stats {
    my @internal_data = @_;

    my $winner = $internal_data[0];
    my $loser  = $internal_data[1];

    my @judoka_data;

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' );

    my $sql_query  = "SELECT * FROM judoka WHERE judoka_id = ?";
    my $sql_params = ($winner);

    my $sth = $dbh->prepare($sql_query);
    $sth->execute($sql_params);

    my @winner_data = $sth->fetchrow_array;

    my $wins              = $winner_data[10] + 1;
    my $sql_insert        = "UPDATE judoka SET wins = ? WHERE judoka_id = ?";
    my @sql_insert_params = ( $wins, $winner );

    $sth = $dbh->prepare($sql_insert);
    $sth->execute(@sql_insert_params);

    # Grab the winners strength data and update by say 10?
    my $strength = $winner_data[14] + 10;

    my $sql_strength = "UPDATE judoka SET strength = ? WHERE judoka_id = ?";
    my @sql_strength_params = ( $strength, $winner );

    $sth = $dbh->prepare($sql_strength);
    $sth->execute(@sql_strength_params);

    # okay give the loser some stats
    $sql_query  = "SELECT * FROM judoka WHERE judoka_id = ?";
    $sql_params = ($loser);

    $sth = $dbh->prepare($sql_query);
    $sth->execute($sql_params);
    my @loser_data = $sth->fetchrow_array;

    my $losses = $loser_data[11] + 1;
    $sql_insert = "UPDATE judoka SET losses = ? WHERE judoka_id = ?";
    @sql_insert_params = ( $losses, $loser );

    $sth = $dbh->prepare($sql_insert);
    $sth->execute(@sql_insert_params);
    $strength = $loser_data[14] + 5;

    $sql_strength = "UPDATE judoka SET strength = ? WHERE judoka_id = ?";
    @sql_strength_params = ( $strength, $loser );
    $sth                 = $dbh->prepare($sql_strength);
    $sth->execute(@sql_strength_params);

    $dbh->disconnect();

    enter_history( $winner_data[2], $loser_data[2] );
}

sub remove_challenge {
    my @info = @_;

    #TODO: ShiaiID is hadcoded, fix this.
    my $shiai_id        = 'lancewlw1';
    my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog' );

    my $sql = "DELETE FROM challenge_db WHERE challenger = ? ";

    my @challenge_params = ( $info[1] );

    my $sth = $dbh->prepare($sql);
    $sth->execute(@challenge_params);

    $dbh->disconnect();
}

sub enter_history {
    # TODO: Don't hard code the shiai id
    my $shiai_id = 'lancewlw1';

    my $history_table = "data/shiai_data/" . $shiai_id . "_hst";

    my @info        = @_;
    my $date_time   = gmtime();
    my $activity    = "Fight";
    my $description = "$info[0] beat $info[1]";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog' );

    my $sql = "INSERT INTO history_db VALUES ( ?,?,? )";

    my @history_params = ( $date_time, $activity, $description );

    my $sth = $dbh->prepare($sql);
    $sth->execute(@history_params);

    $dbh->disconnect();
}

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
