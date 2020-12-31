package VWJL::Athlete;

use VWJL::Infrastructure::Database;

sub get {
    my %args = @_;

    my $athlete = VWJL::Infrastructure::Database::get_athlete(
        user => $args{'user'} );

    return $athlete;
}

true;

