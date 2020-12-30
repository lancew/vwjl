package vwjl_training;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('user');

    template 'training/index' => {};
};

true;

