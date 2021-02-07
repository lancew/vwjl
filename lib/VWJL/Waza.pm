package VWJL::Waza;

use Moo;

extends 'waza';

use strict;
use warnings;

has name => ( is => 'ro', );

has [qw/attack defense/] => (
    is      => 'rw',
    default => 1,
);

sub all {
    my %new_waza = %waza::waza;

    return \%new_waza;
}

1;
