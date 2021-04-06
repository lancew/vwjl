package VWJL::Simulator;

use Moo;

use VWJL::Infrastructure;
use Sort::Rank 'rank_sort';

has 'inf' => (
    is      => 'lazy',
    builder => sub {
        VWJL::Infrastructure->new;
    },
);

sub simulate {
    my ( $self, %args ) = @_;

    my $duration = 240;

    my $scoreboard = {
        'clock' => {
            'seconds'               => 0,
            'minutes'               => 0,
            'total_elapsed_seconds' => 200,
        },
        'blue' => {
            'wazari'  => 0,
            'shido'   => 0,
            'athlete' => $args{athlete_blue},
            'ippon'   => 0,
        },
        'white' => {
            'ippon'   => 0,
            'wazari'  => 0,
            'athlete' => $args{athlete_white},
            'shido'   => 0,
        }
    };

    my $commentary;

    my @athletes = ( $args{athlete_white}, $args{athlete_blue} );

    while ( $scoreboard->{clock}{total_elapsed_seconds} < $duration ) {
        $athletes[0]
            = $self->inf->get_athlete_data( user => $args{athlete_white}, );

        $athletes[1]
            = $self->inf->get_athlete_data( user => $args{athlete_blue}, );

        ( $scoreboard, $commentary, ) = $self->_actions(
            scoreboard => $scoreboard,
            commentary => $commentary,
            white      => $athletes[0],
            blue       => $athletes[1],

        );

        last if $self->_has_winner($scoreboard);
    }

    my $won_lost = $self->_won_lost($scoreboard);

    my @time = gmtime( $scoreboard->{clock}{total_elapsed_seconds} );
    $scoreboard->{clock}{minutes} = $time[1];
    $scoreboard->{clock}{seconds} = $time[0];

    my $result = {
        winner     => $won_lost->[0],
        loser      => $won_lost->[1],
        round      => $args{'round'},
        scoreboard => $scoreboard,
        commentary => $commentary,
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

    return 1;
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
    # --------------------------
    return \@ranks;
}

sub _actions {
    my ( $self, %args ) = @_;

    use Data::Dumper;
    $Data::Dumper::Sortkeys = 1;
    #warn Dumper \%args;

    my $attacks = $self->_who_goes_first( $args{white}, $args{blue} );

    my $defends = $attacks eq 'white' ? 'blue' : 'white';

    my $attack = $self->_make_attack( $args{$attacks}, $args{$defends} );

    if ( $attack->{result} ) {
        # Attack succeeded
        my $roll  = int( rand(100) );
        my $score = "no score";

        if ( $roll > 10 ) {
            if ( $roll > 10 ) { $score = 'wazari' }
            if ( $roll > 90 ) { $score = 'ippon' }

            $args{commentary}
                .= "$attacks attacks with $attack->{waza}, scoring $score\n";
            $args{scoreboard}{$attacks}{$score}++;

        }
        else {
            $args{commentary}
                .= "$attacks attacks with $attack->{waza}, but it does not score\n";
        }

    }
    else {
        # Attack failed
        $args{commentary}
            .= "$attacks attacks with $attack->{waza}, but it fails\n";
    }

    $args{scoreboard}{clock}{total_elapsed_seconds}++;

    $self->inf->update_athlete(
        user  => $args{$attacks}->{username},
        field => 'physical_fatigue',
        value => ( $args{$attacks}->{'physical_fatigue'} || 0 ) + 1,
    );

    return ( $args{scoreboard}, $args{commentary}, );
}

sub _won_lost {
    my ( $self, $scoreboard ) = @_;

    if (   $scoreboard->{white}{ippon}
        || $scoreboard->{white}{wazari} == 2
        || $scoreboard->{blue}{shido} == 3 )
    {
        return [ $scoreboard->{white}{athlete},
            $scoreboard->{blue}{athlete} ];
    }
    else {
        return [ $scoreboard->{blue}{athlete},
            $scoreboard->{white}{athlete} ];
    }

}

sub _has_winner {
    my ( $self, $scoreboard ) = @_;

    if (   $scoreboard->{white}{ippon}
        || $scoreboard->{blue}{ippon}
        || $scoreboard->{white}{wazari} == 2
        || $scoreboard->{blue}{wazari} == 2
        || $scoreboard->{white}{shido} == 3
        || $scoreboard->{blue}{shido} == 3 )
    {
        return 1;
    }

    return 0;
}

sub _who_goes_first {
    my ( $self, $white, $blue ) = @_;

    if ( ( $white->{physical_fatigue} || 0 )
        > ( $blue->{physical_fatigue} || 0 ) )
    {
        return 'blue';
    }
    else {
        return 'white';
    }
}

sub _make_attack {
    my ( $self, $attacker, $defender ) = @_;

    my @waza_list = keys %{ $attacker->{waza_levels} };

    my $attack_waza = $waza_list[ int( rand(@waza_list) ) ];

    my $attacker_levels = $attacker->{waza_levels}{$attack_waza};
    my $defender_levels = $defender->{waza_levels}{$attack_waza};

    my $success = 0;
    if ( defined $defender_levels ) {
        my $attack_roll  = int( rand( $attacker_levels->{attack} ) );
        my $defence_roll = int( rand( $defender_levels->{defence} ) );

        if ( $attack_roll > $defence_roll ) {
            $success = 1;
        }

    }
    else {
        $success = 1;
    }

    return {
        waza   => $attack_waza,
        result => $success,
    };
}

1;
