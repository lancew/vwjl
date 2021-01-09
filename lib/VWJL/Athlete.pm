package VWJL::Athlete;

use Moo;
use VWJL::Infrastructure;

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

    return if $athlete->{'physical_fatigue'} >= 5;

    my $key   = 'waza_' . $args{waza} . '_attack';
    my $value = $athlete->{$key} + 1;

    $self->inf->update_athlete(
        user  => $args{'user'},
        field => $key,
        value => $value,
    );
    $self->inf->update_athlete(
        user  => $args{'user'},
        field => 'physical_fatigue',
        value => $athlete->{'physical_fatigue'} + 1,
    );
}

1;

