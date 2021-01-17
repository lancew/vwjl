use strict;
use warnings;

use Test::More;
use Plack::Test;
use HTTP::Request::Common;
use Ref::Util qw<is_coderef>;

use vwjl_athlete;
my $app = vwjl_athlete->to_app;

ok( is_coderef($app), 'Got app' );

my $test = Plack::Test->create($app);
my $res  = $test->request( GET '/' );

is $res->code, 302, 'No session the /athlete route should redirect';







done_testing;
