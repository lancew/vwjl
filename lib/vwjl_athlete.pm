package vwjl_athlete;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

use VWJL::Athlete;
use VWJL::Waza;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('user');

    my $athlete     = VWJL::Athlete::get( user => session('user') );
    my $waza_module = VWJL::Waza->new;
    my $waza        = $waza_module->all_names;

    template 'athlete/index' => {
        'title'   => 'VWJL Athlete',
        'athlete' => $athlete,
        'waza'    => $waza,
    };
};

1;

