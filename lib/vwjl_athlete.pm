package vwjl_athlete;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

use VWJL::Athlete;
use VWJL::Waza;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('user');
    my $athlete_srv = VWJL::Athlete->new;
    my $waza_module = VWJL::Waza->new;
    my $inf         = VWJL::Infrastructure->new;

    my $athlete      = $athlete_srv->get( user => session('user') );
    my $waza         = $waza_module->all_names;
    my $competitions = $inf->get_competitions;

    my $comps;
    for my $comp (@$competitions) {
        $comps->{ $comp->{id} } = $comp->{name};
    }

    template 'athlete/index' => {
        'title'        => 'VWJL Athlete',
        'athlete'      => $athlete,
        'waza'         => $waza,
        'competitions' => $comps,
    };
};

1;

