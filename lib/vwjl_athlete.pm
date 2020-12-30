package vwjl_athlete;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

use VWJL::Athlete;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('user');

    my $athlete = VWJL::Athlete::get(user => session('user'));

    template 'athlete/index' => { 
        'title' => 'VWJL Athlete',
        'athlete' => $athlete,
    };
};

true;





