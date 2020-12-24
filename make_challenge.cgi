#!/usr/bin/perl -wT
use strict;
use warnings;

use CGI;
$CGI::DISABLE_UPLOADS = 1;         # Disable uploads
$CGI::POST_MAX        = 51_200;    # Maximum number of bytes per post

my $DEBUG = 0;    #  If this is set to 1 then we see the debug messages.

use lib './MyLib';
use DBI;

my $query = CGI->new();    # Start a new cgi object

my $judoka_id;
my $judoka_name;
my $shiai_id;

print $query->header();
print $query->start_html( -title => 'Make Challenge' ),
print $query->h1("E-Judo Test Area - Make Challenge");

if ( $query->param ) {
    $judoka_id   = $query->url_param('judoka_id');
    $judoka_name = $query->url_param('judoka_name');

    my $opponent_id = $query->param("challenge");

    #TODO: Hardcoded teh shiai ID, should be param
    $shiai_id = "lancewFoobar";

    if ( $query->param("challenge") ) {
        enter_in_database($judoka_id, $opponent_id);
    }
    else {
        my $available_judoka = identify_other_judoka( exclude => $judoka_id );
        display_list( $query, $available_judoka );
    }
}
else {
    print $query->h1("No Parameters passed so there was a problem");
    print $query->h1("CLICK YOUR BACK BUTTON");
}

print $query->end_html;

# ---------------------------------------------------
# Sub-routines
# ---------------------------------------------------

sub identify_other_judoka {
    my %args = @_;

    my $exclude_judoka_id = $args{exclude};

    my $shiai_id = 'lancewFoobar';
    my $the_ladder_table
        = "data/shiai_data/"
        . $shiai_id
        . "_ldr";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'ladder_db', 'CSV', $the_ladder_table, 'ad_catalog' );


    my $judoka_list = $dbh->selectall_arrayref(
        'SELECT * FROM ladder_db WHERE ID <> ?',
        {Slice=>{}},
        $exclude_judoka_id
    );


    $dbh->disconnect();

    return $judoka_list;
}


sub display_list {
    my ( $query, $judoka_list)   = @_;

    for my $judoka ( @$judoka_list ) {
        use Data::Dumper;
        warn Dumper $judoka;
        my $this_url = $query->self_url();
        my $link_url = $this_url . "&challenge=" . $judoka->{ID};
        print $query->p(
            $query->a( { -href => $link_url }, $judoka->{PLAYER_NAME} ) );
    }
}

sub enter_in_database {
    my ($challenger_id, $opponent_id) = @_;

    # Accepted database field = 0 for unaccepted.
    # 1 for accepted. (Default should be 0)
    my $accepted = "Yes";

    # TODO: hard coding shiai here.
    my $shiai_id        = 'lancewFoobar';
    my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog' );

    # add the data into a new record
    my $sql = "INSERT INTO challenge_db VALUES ( ?,?,? )";

    my @challenge_params = ( $challenger_id, $opponent_id, $accepted );

    my $sth = $dbh->prepare($sql);
    $sth->execute(@challenge_params);
    $dbh->disconnect();
}

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
