package vwjl_redirect;
use Dancer2;

get '/' => sub {
    redirect 'https://www.vwjl.net';
};

1;

