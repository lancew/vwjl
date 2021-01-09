package VWJL::Infrastructure::Database;
use Moo::Role;

use DBI;

has 'dbh' => (
    is      => 'lazy',
    builder => sub {
      DBI->connect(
        $ENV{DB_SOURCE},
        $ENV{DB_USERNAME},
        $ENV{DB_PASSWORD},
        {
            AutoCommit => 1,
            RaiseError => $ENV{DB_RAISEERROR},
        }
      );  
      #  DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
      #      'postgres', 'somePassword', { AutoCommit => 1, RaiseError => 1 } );
    },
);

sub is_username_in_db {
    my ( $self, $user ) = @_;

    my $user_data
        = $self->dbh->selectrow_hashref(
        'SELECT username FROM accounts WHERE username = ?',
        undef, $user );

    return undef unless $user_data;
}

sub get_users {
    my $self = shift;

    my $users = $self->dbh->selectall_arrayref( 'SELECT * FROM accounts',
        { Slice => {} } );

    return $users;
}

sub get_athletes {
    my $self = shift;

    my $athletes = $self->dbh->selectall_arrayref( 'SELECT * FROM athletes',
        { Slice => {} } );

    return $athletes;
}

sub get_competitions {
    my $self = shift;

    my $competitions = $self->dbh->selectall_arrayref( 'SELECT * FROM competitions',
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
        my $athlete = $athletes->{$entry_id};
        $competition_data->{'entries'}{ $athlete->{id} } = $athlete;
    }

    return $competition_data;
}

sub get_user_data {
    my ( $self, $user ) = @_;

    my $user_data
        = $self->dbh->selectrow_hashref(
        'SELECT * FROM accounts WHERE username = ?',
        undef, $user );

    return $user_data;
}

sub add_user {
    my ( $self, %args ) = @_;

    $self->dbh->do( "
      INSERT INTO accounts
      (username,passphrase,created_on)
      VALUES
      ( ?, ?, localtimestamp)
    ", undef, $args{username}, $args{passphrase} );

    $self->dbh->do( "
      INSERT INTO athletes
      (username)
      VALUES
      (?)
    ", undef, $args{username} );
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

sub add_user_to_competition {
    my ( $self, %args ) = @_;

    $self->dbh->do( "
        INSERT INTO competitions_athletes
                    (athlete_id, competition_id,added_on)
             VALUES (?,?, localtimestamp)
    ", undef, $args{athlete_id}, $args{competition_id} );
}

1;

