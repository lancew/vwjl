package vwjl_training;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use waza;

our $VERSION = '0.1';

use VWJL::Athlete;

get '/' => sub {
    redirect '/' unless session('user');

    template 'training/index' => {};
};

get '/uchi_komi' => sub {
    redirect '/' unless session('user');

    my $waza = waza::all();

    my $athlete_srv = VWJL::Athlete->new;
    my $athlete      = $athlete_srv->get( user => session('user') );

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

    redirect '/training/uchi_komi';
};

1;

