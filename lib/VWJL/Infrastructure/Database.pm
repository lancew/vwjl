package VWJL::Infrastructure::Database;
use Moo::Role;

use DBI;

has 'dbh' => (
    is => 'lazy',
    builder => sub {
        DBI->connect( "dbi:Pg:dbname=postgres;host=localhost", 'postgres', 'somePassword', { AutoCommit => 1 } );
    },
);


sub is_username_in_db {
    my ($self,$user) = @_;

    my $user_data
        = $self->dbh->selectrow_hashref(
        'SELECT username FROM accounts WHERE username = ?',
        undef, $user );

    return undef unless $user_data;
}

sub get_user_data {
    my ($self,$user) = @_;

    my $user_data
        = $self->dbh->selectrow_hashref(
        'SELECT * FROM accounts WHERE username = ?',
        undef, $user );

    return $user_data;    
}

sub add_user {
    my ($self, %args) = @_;

    $self->dbh->do( "
      INSERT INTO accounts
      (username,passphrase,created_on)
      VALUES
      ( ?, ?, localtimestamp)
    ", undef, $args{username}, $args{passphrase} );

}

sub get_athlete {
    my ( $self, %args ) = @_;

    my %fake_data = (
        'lancew' => {
            name      => 'Hifumi Maruyama',
            weight    => '65.2',
            dojo      => 'Kodokan',
            country   => 'Japan',
            sensei    => 'Inoue Kosei',
            wins      => 0,
            losses    => 0,
            biography =>
                'Just a Judoka trying to make his way in the universe',
            physical => {
                fitness  => 10,
                form     => 11,
                fatigue  => 12,
                left_arm => {
                    strength => 50,
                    fatigue  => 50,
                    injury   => 50,
                },
                right_arm => {
                    fatigue  => 51,
                    injury   => 51,
                    strength => 51,
                },
                left_leg => {
                    fatigue  => 52,
                    injury   => 52,
                    strength => 52,
                },
                right_leg => {
                    strength => 53,
                    fatigue  => 53,
                    injury   => 53,
                },
            },
            waza => {
                ippon_seoi_nage => {
                    attack  => 80,
                    defense => 81,
                },
                uchi_mata => {
                    attack  => 90,
                    defense => 91,
                },
            },
        }
    );

    my $athlete = $fake_data{ $args{'user'} };

    return $athlete;
}

1;

