#!/usr/bin/env perl

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use vwjl;
use vwjl_admin;
use vwjl_athlete;
use vwjl_training;

use Plack::Builder;

builder {
    mount '/'        => vwjl->to_app;
    mount '/admin'   => vwjl_admin->to_app;
    mount '/athlete' => vwjl_athlete->to_app;
    mount '/training' => vwjl_training->to_app;
}


