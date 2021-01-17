package VWJL::Ranking;

use Moo;
use VWJL::Infrastructure;
use Sort::Rank 'rank_sort';

has 'inf' => (
    is      => 'lazy',
    builder => sub {
        VWJL::Infrastructure->new;
    },
);

sub get_all_rankings {
    my $self = shift;

    my $results  = $self->inf->get_all_results;
    my $rankings = $self->calculate_ranking($results);

    return $rankings;
}

sub calculate_ranking {
    my ( $self, $results ) = @_;

    my %ranking;
    for my $r (@$results) {
        $ranking{ $r->{winner} }++;
        $ranking{ $r->{loser} } = 0 unless defined $ranking{ $r->{loser} };
    }

    my @scores;
    for my $r ( keys %ranking ) {
        push @scores,
            {
            name  => $r,
            score => $ranking{$r},
            };
    }

    my @ranks = rank_sort( \@scores );
    return \@ranks;
}

1;
