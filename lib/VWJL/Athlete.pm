package VWJL::Athlete;

use VWJL::Infrastructure;

sub get {
    my %args = @_;

    my $inf = VWJL::Infrastructure->new;

    my $athlete = $inf->get_athlete( user => $args{'user'} );

    return $athlete;
}

true;

