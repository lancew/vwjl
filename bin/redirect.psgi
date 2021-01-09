#!/usr/bin/env perl

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use Plack::Builder;
use vwjl_redirect;

builder {
    mount '/' => vwjl_direct->to_app;
}

