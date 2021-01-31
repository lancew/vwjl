use Test2::V0 -target => VWJL::Athlete;

use Data::Dumper;
$Data::Dumper::Sortkeys = 1;

my $a = $CLASS->new;

is $a->win_percentage, 0, 'win_percentage calculated correctly when no wins or losses';

$a->wins(1);
is $a->win_percentage, 100, 'win_percentage calculated correctly when 1 win and 0 losses';

$a->losses(1);
is $a->win_percentage, 50, 'win_percentage calculated correctly when 1 win and 1 loss';



is $a->ashi_garami,
{ attack =>1, defense =>1},
'Waza correctly added';

$a->ashi_garami->attack(5);
is $a->ashi_garami,
{ attack =>5, defense =>1},
'Waza correctly updated';


note Dumper $a;
done_testing;
