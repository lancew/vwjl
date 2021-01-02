use strict;
use warnings;

use vwjl;
use Test::More;
use Plack::Test;
use HTTP::Request::Common;
use Ref::Util qw<is_coderef>;

my $app = vwjl->to_app;
ok( is_coderef($app), 'Got app' );

my $test = Plack::Test->create($app);
my $res  = $test->request( GET '/login' );

ok( $res->is_success, '[GET /login] successful' );

like $res->content, qr{name="user"},     'Has "user" field';
like $res->content, qr{name="password"}, 'Has "password" field';
like $res->content, qr{type="submit"},   'Has submit button';

done_testing;
