package VWJL::Infrastructure::DatabaseResults;
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

sub get_all_results {
    my $self = shift;

    my $results = $self->dbh->selectall_arrayref( 'SELECT * FROM results',
        { Slice => {}, } );

    return $results;
}

1;
