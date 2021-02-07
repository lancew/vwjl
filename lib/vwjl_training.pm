package vwjl_training;

use strict;
use warnings;

use Dancer2::Plugin::Auth::Tiny;
use Dancer2;
use VWJL::Athlete;
use waza;

get '/' => sub {
    redirect '/' unless session('user');

    template 'training/index' => {};
};

get '/uchi_komi' => sub {
    redirect '/' unless session('user');

    my $waza = waza::all();

    my $athlete_srv = VWJL::Athlete->new;
    my $athlete     = $athlete_srv->get( user => session('user') );

    template 'training/uchi_komi' => {
        athlete => $athlete,
        waza    => $waza,
    };
};

get '/uchi_komi/:waza' => sub {
    redirect '/' unless session('user');

    my $athlete_srv = VWJL::Athlete->new;

    $athlete_srv->uchi_komi(
        user => session('user'),
        waza => route_parameters->get('waza'),
    );

    warn '------------------';

    redirect '/uchi_komi';
};

get '/stretching' => sub {
    redirect '/' unless session('user');

    my $athlete_srv = VWJL::Athlete->new;
    my $athlete     = $athlete_srv->get( user => session('user') );

    template 'training/stretching' => { athlete => $athlete, };
};

post '/stretching' => sub {
    redirect '/' unless session('user');

    my $inf = VWJL::Infrastructure->new;

    my $athlete     = $inf->get_athlete_data( user => session('user') );
    my $competition = $inf->get_competition(
        competition_id => route_parameters->get('competition_id') );

    # Decrease by up to 5 points, if they have money and they are fatugued
    if ( $athlete->{credits} >= 1 && $athlete->{physical_fatigue} > 0 ) {
        $inf->update_athlete(
            field => 'credits',
            user  => session('user'),
            value => ( $athlete->{'credits'} - 1 ),
        );

        $inf->update_athlete(
            field => 'physical_fatigue',
            user  => session('user'),
            value => ( $athlete->{'physical_fatigue'} - 1 ),
        );
    }

    redirect '/stretching';
};

1;

