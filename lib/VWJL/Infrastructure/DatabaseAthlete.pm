package VWJL::Infrastructure::DatabaseAthlete;
use Moo::Role;

use DBI;

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

sub get_athletes {
    my $self = shift;

    my $athletes = $self->dbh->selectall_arrayref( 'SELECT * FROM athletes',
        { Slice => {} } );

    return $athletes;
}

sub get_athlete_data {
    my ( $self, %args ) = @_;

    my $athlete_data
        = $self->dbh->selectrow_hashref(
        'SELECT * FROM athletes WHERE username = ?',
        undef, $args{user} );

    my $entries = $self->dbh->selectall_arrayref( '
        SELECT competition_id FROM competitions_athletes WHERE athlete_id = ?
    ', { Slice => {} }, $athlete_data->{id} );

    $athlete_data->{competition_entries} = $entries;

    my $waza_levels
        = $self->dbh->selectall_hashref(
        'SELECT * FROM waza_level WHERE athlete_id = ?',
        'waza', undef, $athlete_data->{id}, );

    $athlete_data->{waza_levels} = $waza_levels;

    return $athlete_data;
}

sub update_athlete {
    my ( $self, %args ) = @_;

    my $rv = $self->dbh->do(
        "UPDATE athletes SET "
            . $args{'field'}
            . " = ? WHERE athletes.username = ?",
        undef, $args{'value'}, $args{'user'}
    );
}

sub update_athlete_waza {
    my ( $self, %args ) = @_;

    my $rv = $self->dbh->do(
        "UPDATE waza_level
            SET attack = attack + ?,
                defence = defence + ?
          WHERE athlete_id = ? AND waza = ?",
        undef,
        $args{attack_delta},
        $args{defence_delta},
        $args{athlete_id},
        $args{waza},
    );

    if ( $rv eq '0E0' ) {
        $self->dbh->do(
            'INSERT INTO waza_level
            (athlete_id,waza,attack,defence)
         VALUES
         (?,?,?,?)',
            undef,
            $args{athlete_id},
            $args{waza},
            $args{attack_delta},
            $args{defence_delta},
        );
    }
}

1;
