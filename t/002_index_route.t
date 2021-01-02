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
my $res  = $test->request( GET '/' );

ok( $res->is_success, '[GET /] successful' );

like $res->content,   qr{href="/register"}, 'Has "Register" link';
like $res->content,   qr{href="/login"},    'Has "Login" link';
unlike $res->content, qr{href="/logout"},
    'Does not have "Logout" link (not yet logged in)';

done_testing;
