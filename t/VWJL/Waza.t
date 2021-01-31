use Test2::V0 -target => VWJL::Waza;

ok 1;

use Data::Dumper;
$Data::Dumper::Sortkeys = 1;


my $w = $CLASS->new(
    name => 'ashi-Garami',
);

note Dumper $w;

done_testing;
