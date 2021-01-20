package VWJL::Infrastructure::DatabaseCompetition;

use strict;
use warnings;

use DBI;
use Moo::Role;

has 'dbh' => (
    is      => 'lazy',
    builder => sub {
        DBI->connect(
            $ENV{DB_SOURCE},
            $ENV{DB_USERNAME},
            $ENV{DB_PASSWORD},
            {   AutoCommit => 1,
                RaiseError => $ENV{DB_RAISEERROR},
            }
        );
    },
);

sub get_competitions {
    my $self = shift;

    my $competitions
        = $self->dbh->selectall_arrayref(
        'SELECT * FROM competitions ORDER BY id',
        { Slice => {} } );

    return $competitions;
}

sub get_competition {
    my ( $self, %args ) = @_;

    my $competition_data
        = $self->dbh->selectrow_hashref(
        'SELECT * FROM competitions WHERE id = ?',
        undef, $args{competition_id} );

    my $entries = $self->dbh->selectall_arrayref(
        'SELECT athlete_id from competitions_athletes WHERE competition_id = ?',
        { Slice => {} },
        $args{competition_id}
    );

    my $athletes
        = $self->dbh->selectall_hashref( 'SELECT * FROM athletes', 'id' );

    for my $entry (@$entries) {
        my $entry_id = $entry->{'athlete_id'};
        my $athlete  = $athletes->{$entry_id};
        $competition_data->{'entries'}{ $athlete->{id} } = $athlete;
    }

    return $competition_data;
}

sub get_competition_results {
    my ( $self, %args ) = @_;

    my $results = $self->dbh->selectall_arrayref(
        'SELECT results.*, scoreboard.* 
           FROM results
           JOIN scoreboard ON (results.id = scoreboard.result_id)
          WHERE competition = ?',
        { Slice => {} },
        $args{competition_id}
    );

    return $results;
}

sub add_competition {
    my ( $self, %args ) = @_;

    my $rv = $self->dbh->do(
        "INSERT INTO competitions
        ( name, description, owner_username, entry_fee, created_on )
        VALUES
        (?, ?, ?, ?, localtimestamp )",
        undef,
        $args{name},
        $args{description},
        $args{username},
        $args{entry_fee}
    );

    return 1;
}

sub add_user_to_competition {
    my ( $self, %args ) = @_;

    $self->dbh->do( "
        INSERT INTO competitions_athletes
                    (athlete_id, competition_id,added_on)
             VALUES (?,?, localtimestamp)
    ", undef, $args{athlete_id}, $args{competition_id} );

    return 1;
}

sub store_result {
    my ( $self, %args ) = @_;

    $self->dbh->do( '
            INSERT INTO scoreboard
            (
                clock_minutes,
                clock_seconds,
                white_athlete,
                white_ippon,
                white_wazari,
                white_shido,
                blue_athlete,
                blue_ippon,
                blue_wazari,
                blue_shido
            )
            VALUES
            (?,?,?,?,?,?,?,?,?,?)
            RETURNING id;
        ',
        undef,
        $args{clock_minutes},
        $args{clock_seconds},
        $args{white_athlete},
        $args{white_ippon},
        $args{white_wazari},
        $args{white_shido},
        $args{blue_athlete},
        $args{blue_ippon},
        $args{blue_wazari},
        $args{blue_shido},
    );

    my $scoreboard_id
        = $self->dbh->last_insert_id( undef, undef, 'scoreboard' );

    $self->dbh->do( '
            INSERT INTO results
            (
                competition,
                round,
                winner,
                loser,
                scoreboard_id,
                commentary
            )
            VALUES
            ( ?, ?, ?, ?, ?, ? )
            RETURNING id;
        ',
        undef,
        $args{competition_id},
        $args{round},
        $args{winner},
        $args{loser},
        $scoreboard_id,
        $args{commentary},
    );

    my $result_id = $self->dbh->last_insert_id( undef, undef, 'results' );

    $self->dbh->do( '
            UPDATE scoreboard
               SET result_id = ?
             WHERE id = ?  
        ',
        undef,
        $result_id,
        $scoreboard_id,
    );

    $self->dbh->do( '
            UPDATE results
               SET scoreboard_id = ?
             WHERE id = ?  
        ',
        undef,
        $scoreboard_id,
        $result_id,
    );

    $self->dbh->do( "
            UPDATE competitions
               SET status = 'Complete'
             WHERE id = ? 
        ",
        undef,
        $args{competition_id},

    );

    return 1;
}

1;
