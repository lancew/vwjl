#!/usr/bin/env perl

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use vwjl_redirect;
use Plack::Builder;

builder {
    mount '/' => vwjl_redirect->to_app;
}

