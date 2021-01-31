use Test2::V0 -target => VWJL::Contest;

use VWJL::Athlete;

use Data::Dumper;
$Data::Dumper::Sortkeys = 1;



my $a1 = VWJL::Athlete->new(
    name => 'a1',
);
my $a2 = VWJL::Athlete->new(
    name => 'a2',
);




my $contest = VWJL::Contest->new(
    duration => 240,
    athletes => [
        $a1,$a2
    ],
);


note Dumper $contest;



ok 1;
done_testing;
