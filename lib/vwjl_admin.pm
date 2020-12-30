package vwjl_admin;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

get '/' => sub {
	redirect '/' unless session('admin');

    template 'admin/index' => { 'title' => 'VWJL Admin' };
};

true;
