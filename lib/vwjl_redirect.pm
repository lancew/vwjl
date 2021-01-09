package vwjl_direct;
use Dancer2;

get '/' => sub {
    redirect 'https://www.vwjl.net';
};

1;

