use strict;
use warnings;

use Test::More;

use_ok 'VWJL::Infrastructure';

my $inf = VWJL::Infrastructure->new;

can_ok( $inf, 'get_athlete'); 

done_testing;
