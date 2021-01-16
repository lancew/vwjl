package VWJL::Infrastructure::Database;
use Moo::Role;

use DBI;
use FindBin;

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

sub get_migration_files {
    my $dir = "$FindBin::Bin/../db";
    opendir my $dh, $dir or die "Could not open '$dir' for reading '$!'\n";
    my @migration_files = readdir $dh;
    closedir $dh;

    my @files;
    for my $file ( sort @migration_files ) {
        push @files, $file if $file =~ /\d{3}/;
    }

    return @files;
}

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

1;

