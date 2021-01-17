package VWJL::Infrastructure;

use strict;
use warnings;

use Moo;
with 'VWJL::Infrastructure::Database';
with 'VWJL::Infrastructure::DatabaseAthlete';
with 'VWJL::Infrastructure::DatabaseCompetition';
with 'VWJL::Infrastructure::DatabaseResults';

1;
