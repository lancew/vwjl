package vwjl_ranking;

use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

use VWJL::Ranking;

get '/' => sub {
    redirect '/' unless session('user');

    my $rank     = VWJL::Ranking->new;
    my $rankings = $rank->get_all_rankings;

    template 'ranking/index' => { 'rankings' => $rankings, };
};
1;
