package VWJL::Simulator;

use Moo;

use VWJL::Infrastructure;
use Time::Piece;
use Time::Seconds;

sub simulate {
    my ( $self, %args ) = @_;

    my $inf = VWJL::Infrastructure->new;

    my @athletes = ( $args{athlete_white}, $args{athlete_blue} );
    my $first    = int( rand(2) );
    my $winner   = 0;
    my ( $won, $lost );
    my $winning_waza = "shido";

    $athletes[0] = $inf->get_athlete_data( user => $args{athlete_white}, );

    $athletes[1] = $inf->get_athlete_data( user => $args{athlete_blue}, );

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
        $inf->update_athlete(
            field => 'wins',
            user  => $won,
            value => $athletes[1]->{'wins'} + 1,
        );

        $inf->update_athlete(
            field => 'losses',
            user  => $lost,
            value => $athletes[0]->{'losses'} + 1,
        );
    }
    elsif ( $winner == 0 ) {
        $won  = $athletes[0]->{'username'};
        $lost = $athletes[1]->{'username'};
        $inf->update_athlete(
            field => 'wins',
            user  => $won,
            value => $athletes[0]->{'wins'} + 1,
        );

        $inf->update_athlete(
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

1;
