#!/usr/bin/perl -w
use strict;
use warnings;

use CGI;
$CGI::DISABLE_UPLOADS = 1;         # Disable uploads
$CGI::POST_MAX        = 51_200;    # Maximum number of bytes per post

use lib './MyLib';
use DBI;
use VWJL;

my $query = CGI->new();            # Start a new cgi object

my $judoka_id;
my $judoka_name;

print $query->header();
print $query->start_html( -title => 'Simulate Fights' );
print $query->h1("E-Judo Test Area - Simulate");
print $query->h1("SIMULATE");

my $challenges = find_challenges();

for my $match (@$challenges) {
    print $query->p(simulate_match($match));
}

print $query->end_html;

# ---------------------------------------------------

sub find_challenges {
    my $query    = shift;
    my $shiai_id = "lancewFoobar";    # Hard coding for now.
    my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog' );

    $dbh->selectall_arrayref(
        'SELECT * FROM challenge_db WHERE ACCEPTED = ?',
        {Slice=>{}},
        'Yes'
    );
}

sub simulate_match {
    my $match = shift;

    my $challenger = VWJL::get_judoka( $match->{CHALLENGER} );
    my $opponent   = VWJL::get_judoka( $match->{OPPONENT_ID} );

    my $commentary = fight($challenger, $opponent);
    remove_challenge($match);

    return $commentary;
}

sub fight {
    my ($challenger, $opponent) = @_;
    my $commentary = '';

    $commentary .=  $challenger->{NAME} . ' Vs. ' . $opponent->{NAME};
    $commentary .= '. <br>';

    srand(time);
    my $challenger_attack = int( rand(100));
    my $opponent_attack = int( rand(100));

    my ($winner,$loser);
    if ( $challenger_attack >= $opponent_attack ) {
        $commentary .= $challenger->{NAME} . ' WINS';

        $winner = $challenger;
        $loser  = $opponent;
    }
    else {
        $commentary .= $opponent->{NAME} . ' WINS';

        $winner = $opponent;
        $loser  = $challenger;
    }

    update_stats($winner,$loser);
    enter_history( $winner->{NAME}, $loser->{NAME} );

    return $commentary;
}

sub update_stats {
    my ($winner, $loser) = @_;

    $winner->{WINS}++;
    $loser->{LOSSES}++;

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' );

    $dbh->do(
        'UPDATE judoka SET WINS = ? WHERE JUDOKA_ID = ?',
        undef,
        $winner->{WINS},
        $winner->{JUDOKA_ID}
    );
    $dbh->do(
        'UPDATE judoka SET LOSSES = ? WHERE JUDOKA_ID = ?',
        undef,
        $loser->{LOSSES},
        $loser->{JUDOKA_ID}
    );

    return;
}

sub remove_challenge {
    my $match = shift;

    #TODO: ShiaiID is hadcoded, fix this.
    my $shiai_id        = 'lancewFoobar';
    my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog' );

    $dbh->do(
        'DELETE FROM challenge_db WHERE challenger = ? AND opponent_id = ?',
        undef,
        $match->{CHALLENGER},
        $match->{OPPONENT_ID}
    );

    $dbh->disconnect();
}

sub enter_history {
    my ($winner,$loser) = @_;

    # TODO: Don't hard code the shiai id
    my $shiai_id = 'lancewFoobar';

    my $history_table = "data/shiai_data/" . $shiai_id . "_hst";

    my @info        = @_;
    my $date_time   = gmtime();
    my $activity    = "Fight";
    my $description = "$winner beat $loser";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog' );

    $dbh->do(
        'INSERT INTO history_db VALUES ( ?,?,? )',
        undef,
        $date_time,
        $activity,
        $description
    );

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
