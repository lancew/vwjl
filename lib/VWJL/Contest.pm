package VWJL::Contest;

use Moo;

has athletes => (
    is       => 'ro',
    required => 1,
);

has duration => (
    is       => 'ro',
    required => 1,
);

1;
