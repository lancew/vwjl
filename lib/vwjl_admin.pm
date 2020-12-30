package vwjl_admin;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('admin');

    template 'admin/index' => { 'title' => 'VWJL Admin' };
};

get '/users' => sub {
    redirect '/' unless session('admin');

    my $users = [ 'Lance Wicks', 'Joe Bloggs', 'Jane Doe', ];

    my $total_users = 0 + @{$users};

    template 'admin/users' => {
        'title'     => 'VWJL Admin',
        users       => $users,
        total_users => $total_users
    };
};
true;
