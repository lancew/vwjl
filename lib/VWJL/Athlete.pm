package VWJL::Athlete;

use Moo;
use VWJL::Infrastructure;
use waza;

has 'inf' => (
    is      => 'lazy',
    builder => sub {
        VWJL::Infrastructure->new;
    },
);

sub get {
    my ( $self, %args ) = @_;

    my $athlete = $self->inf->get_athlete_data( user => $args{'user'} );

    if ($athlete->{wins} && $athlete->{losses} ) {
        $athlete->{win_percentage} = int(100 * ($athlete->{wins} / ($athlete->{wins} + $athlete->{losses})));
    } 

    return $athlete;
}

sub uchi_komi {
    my ( $self, %args ) = @_;

    my $athlete = $self->inf->get_athlete_data( user => $args{'user'} );

    $self->inf->update_athlete_waza(
        athlete_id    => $athlete->{'id'},
        waza          => $args{'waza'},
        attack_delta  => 1,
        defence_delta => 0,
    );

    $self->inf->update_athlete(
        user  => $args{'user'},
        field => 'physical_fatigue',
        value => $athlete->{'physical_fatigue'} + 1,
    );
}

1;

