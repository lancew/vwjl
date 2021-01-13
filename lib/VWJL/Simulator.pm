package VWJL::Simulator;

use Moo;

use VWJL::Infrastructure;
use Time::Piece;
use Time::Seconds;

has 'inf' => (
    is      => 'lazy',
    builder => sub {
        VWJL::Infrastructure->new;
    },
);

sub simulate {
    my ( $self, %args ) = @_;

    my @athletes = ( $args{athlete_white}, $args{athlete_blue} );
    my $first    = int( rand(2) );
    my $winner   = 0;
    my ( $won, $lost );
    my $winning_waza = "shido";

    $athletes[0]
        = $self->inf->get_athlete_data( user => $args{athlete_white}, );

    $athletes[1]
        = $self->inf->get_athlete_data( user => $args{athlete_blue}, );

    for my $waza ( keys %{ $athletes[$first]->{waza_levels} } ) {
        my $first = $athletes[$first]->{waza_levels}{$waza}{attack};
        my $second
            = (
            $athletes[ $first == 1 ? 0 : 1 ]->{waza_levels}{$waza}{defence} )
            || 0;

        if ( $first > $second ) {
            $winner = 1;
        }
        else {
            $winner = 0;
        }
        $winning_waza = $waza;
        last;
    }

    if ( $winner == 1 ) {
        $won  = $athletes[1]->{'username'};
        $lost = $athletes[0]->{'username'};
        $self->inf->update_athlete(
            field => 'wins',
            user  => $won,
            value => $athletes[1]->{'wins'} + 1,
        );

        $self->inf->update_athlete(
            field => 'losses',
            user  => $lost,
            value => $athletes[0]->{'losses'} + 1,
        );
    }
    elsif ( $winner == 0 ) {
        $won  = $athletes[0]->{'username'};
        $lost = $athletes[1]->{'username'};
        $self->inf->update_athlete(
            field => 'wins',
            user  => $won,
            value => $athletes[0]->{'wins'} + 1,
        );

        $self->inf->update_athlete(
            field => 'losses',
            user  => $lost,
            value => $athletes[1]->{'losses'} + 1,
        );
    }
    else {
        die 'SERIOUSLY WTF?? ', $winner;
    }

    my $result = {
        winner     => $won,
        loser      => $lost,
        round      => $args{'round'},
        scoreboard => {
            white => {
                athlete => $args{athlete_white},
                ippon   => 1,
                wazari  => 1,
                shido   => 0,
            },
            blue => {
                athlete => $args{athlete_blue},
                ippon   => 0,
                wazari  => 1,
                shido   => 2,
            },
            clock => {
                total_elapsed_seconds => 240,
                minutes               => 4,
                seconds               => 0,
            },
        },
        commentary => $winning_waza eq 'shido'
        ? "$lost lost to $won by $winning_waza"
        : "$won threw $lost with $winning_waza"
    };

    return $result;
}

sub store_results {
    my ( $self, %args ) = @_;

    my $comp    = $args{competition};
    my $results = $args{results};

    for my $result ( @{ $args{results} } ) {
        $self->inf->store_result(
            competition_id => $comp->{id},
            round          => $result->{round},
            winner         => $result->{winner},
            loser          => $result->{loser},
            commentary     => $result->{commentary},
            clock_minutes  => $result->{scoreboard}{clock}{minutes},
            clock_seconds  => $result->{scoreboard}{clock}{seconds},
            white_athlete  => $result->{scoreboard}{white}{athlete},
            white_ippon    => $result->{scoreboard}{white}{ippon},
            white_wazari   => $result->{scoreboard}{white}{wazari},
            white_shido    => $result->{scoreboard}{white}{shido},
            blue_athlete   => $result->{scoreboard}{blue}{athlete},
            blue_ippon     => $result->{scoreboard}{blue}{ippon},
            blue_wazari    => $result->{scoreboard}{blue}{wazari},
            blue_shido     => $result->{scoreboard}{blue}{shido},
        );
    }

}

1;
