package VWJL::Infrastructure::Database;
use Moo::Role;

use DBI;

has 'dbh' => (
    is      => 'lazy',
    builder => sub {
        DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
            'postgres', 'somePassword', { AutoCommit => 1 } );
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

sub get_competitions {
    my $self = shift;

    my $users = $self->dbh->selectall_arrayref( 'SELECT * FROM competitions',
        { Slice => {} } );

    return $users;
}

sub get_competition {
    my ( $self, %args ) = @_;

    my $user_data
        = $self->dbh->selectrow_hashref(
        'SELECT * FROM competitions WHERE id = ?',
        undef, $args{competition_id} );

    return $user_data;
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
        SELECT id FROM competitions_athletes WHERE athlete_id = ?
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

