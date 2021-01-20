package vwjl_athlete;

use strict;
use warnings;

use Dancer2::Plugin::Auth::Tiny;
use Dancer2;
use VWJL::Athlete;
use VWJL::Infrastructure;
use VWJL::Waza;

get '/' => sub {
    redirect '/' unless session('user');

    my $athlete_srv = VWJL::Athlete->new;
    my $inf         = VWJL::Infrastructure->new;
    my $waza_module = VWJL::Waza->new;

    my $athlete      = $athlete_srv->get( user => session('user') );
    my $competitions = $inf->get_competitions;
    my $waza         = $waza_module->all_names;

    my $comps;
    for my $comp (@$competitions) {
        $comps->{ $comp->{id} } = $comp;
    }

    template 'athlete/index' => {
        'athlete'      => $athlete,
        'competitions' => $comps,
        'title'        => 'VWJL Athlete',
        'waza'         => $waza,
    };
};

1;

