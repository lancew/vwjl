package VWJL::Waza;

use Moo;

extends 'waza';

use strict;
use warnings;

sub all {
    my %new_waza = %waza::waza;

    return \%new_waza;
}

1;
