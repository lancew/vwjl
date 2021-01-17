use strict;
use warnings;

use Test::More;
use Test::MockModule;
use Test::Deep;

use VWJL::Simulator;

use Data::Dumper;

{
    my $inf = Test::MockModule->new('VWJL::Infrastructure');
    $inf->mock( 'dbh'            => sub {return} );
    $inf->mock( 'update_athlete' => sub {return} );
    $inf->mock(
        'get_athlete_data' => sub {
            my ( $self, %args ) = @_;

            if ( $args{user} eq 'WHITE' ) {
                return {
                    username    => $args{user},
                    wins        => 10,
                    losses      => 20,
                    waza_levels => {
                        ippon_seoi_nage => {
                            attack  => 100,
                            defence => 100,
                        },
                        uchi_mata => {
                            attack  => 100,
                            defence => 100,
                        },
                    }
                };
            }
            else {
                return {
                    username    => $args{user},
                    wins        => 0,
                    losses      => 0,
                    waza_levels => {
                        ippon_seoi_nage => {
                            attack  => 1,
                            defence => 1,
                        },
                    }
                };
            }
        }
    );

    my $sim = VWJL::Simulator->new;

    my $result = $sim->simulate(
        athlete_blue   => 'BLUE',
        athlete_white  => 'WHITE',
        competition_id => 123,
        round          => 1,
    );

    cmp_deeply $result,
        {
        'commentary' => ignore(),
        'round'      => 1,
        'scoreboard' => {
            'clock' => {
                'seconds'               => any( 0 .. 59 ),
                'minutes'               => any( 0, 1, 2, 3, 4 ),
                'total_elapsed_seconds' => 240
            },
            'blue' => {
                'wazari'  => any( 1, 0 ),
                'shido'   => any( 0, 1, 2, 3 ),
                'athlete' => 'BLUE',
                'ippon'   => any( 1, 0 ),
            },
            'white' => {
                'ippon'   => any( 1, 0 ),
                'wazari'  => any( 0, 1 ),
                'athlete' => 'WHITE',
                'shido'   => any( 0, 1, 2, 3 )
            }
        },
        'loser'  => any( 'WHITE', 'BLUE' ),
        'winner' => any( 'WHITE', 'BLUE' ),
        },
        'simulate returns expected output';

    isnt $result->{'winner'}, $result->{'loser'},
        'Winner and Loser can not be the same';

    if ( $result->{'scoreboard'}{'blue'}{'ippon'} == 1 ) {
        is $result->{'winner'}, 'BLUE',
            'BLUE has Ippon: winner should be BLUE';
        is $result->{'loser'}, 'WHITE',
            'BLUE has Ippon: loser should be WHITE';
    }
    else {
        is $result->{'winner'}, 'WHITE',
            'WHITE has Ippon: winner should be WHITE';
        is $result->{'loser'}, 'BLUE',
            'WHITE has Ippon: loser should be BLUE';

    }

}

done_testing;
