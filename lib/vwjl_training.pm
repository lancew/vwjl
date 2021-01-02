package vwjl_training;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('user');

    template 'training/index' => {};
};

get '/uchi_komi' => sub {
    redirect '/' unless session('user');

    template 'training/uchi_komi';
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

true;

