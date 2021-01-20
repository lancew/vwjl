package vwjl_ranking;

use strict;
use warnings;

use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use VWJL::Ranking;

get '/' => sub {
    redirect '/' unless session('user');

    my $rank     = VWJL::Ranking->new;
    my $rankings = $rank->get_all_rankings;

    template 'ranking/index' => { 'rankings' => $rankings, };
};
1;
