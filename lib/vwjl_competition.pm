package vwjl_competition;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('user');

    template 'competition/index' => {};
};

true;

