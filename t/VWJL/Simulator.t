use strict;
use warnings;

use Test::More;
use Test::MockModule;
use Test::Deep;

use VWJL::Simulator;

use Data::Dumper;


subtest '_actions' => sub {
	my $sim = VWJL::Simulator->new;
    my (
            $scoreboard,
            $commentary,
        ) = $sim->_actions(
            scoreboard => {
              'clock' => {
                  'seconds'               => 0,
                  'minutes'               => 0,
                  'total_elapsed_seconds' => 0
              },
              'blue' => {
                  'wazari'  => 0,
                  'shido'   => 0,
                  'athlete' => 'Mr Blue',
                  'ippon'   => 0,
              },
              'white' => {
                  'ippon'   => 0,
                  'wazari'  => 0,
                  'athlete' => 'Mt White',
                  'shido'   => 0,
              }
            },
            commentary => 'Foo',
            white => {
                username    => 'Mr White',
                physical_fatigue => 10,
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

            },
            blue  => {
                username    => 'Mr Blue',
                physical_fatigue => 9,
                wins        => 1,
                losses      => 2,
                waza_levels => {
                    ippon_seoi_nage => {
                        attack  => 11,
                        defence => 12,
                    },
                    uchi_mata => {
                        attack  => 13,
                        defence => 14,
                    },
                }
            },
        );

	ok 1;
};


subtest '_who_goes_first' => sub {
    my $sim = VWJL::Simulator->new;

    my $result = $sim->_who_goes_first(
            {
                username    => 'Mr White',
                physical_fatigue => 3,
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

            },
            {
                username    => 'Mr Blue',
                physical_fatigue => 9,
                wins        => 1,
                losses      => 2,
                waza_levels => {
                    ippon_seoi_nage => {
                        attack  => 11,
                        defence => 12,
                    },
                    uchi_mata => {
                        attack  => 13,
                        defence => 14,
                    },
                }
            },

    );

    is $result, 'white', 'White should go first';
};


subtest '_make_attack' => sub{
	my $sim = VWJL::Simulator->new;

    my $result = $sim->_make_attack(
            {
                username    => 'Mr White',
                physical_fatigue => 3,
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

            },
            {
                username    => 'Mr Blue',
                physical_fatigue => 9,
                wins        => 1,
                losses      => 2,
                waza_levels => {
                    tai_otoshi => {
                        attack  => 11,
                        defence => 12,
                    },
                    uchi_mata => {
                        attack  => 13,
                        defence => 14,
                    },
                }
            },

    );

    ok 1;
};

subtest 'simulate' => sub {
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
        'commentary' => re('white attacks with ippon_seoi_nage'),
        'round'      => 1,
        'scoreboard' => {
            'clock' => {
                'seconds'               => any( 0 .. 59 ),
                'minutes'               => any( 0, 1, 2, 3, 4 ),
                'total_elapsed_seconds' => any( 1..240),
            },
            'blue' => {
                'wazari'  => any( 2, 1, 0 ),
                'shido'   => any( 0, 1, 2, 3 ),
                'athlete' => 'BLUE',
                'ippon'   => any( 1, 0 ),
            },
            'white' => {
                'ippon'   => any( 1, 0 ),
                'wazari'  => any( 0, 1, 2 ),
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
        is $result->{'winner'}, 'BLUE',  'BLUE has Ippon: winner should be BLUE';
        is $result->{'loser'},  'WHITE', 'BLUE has Ippon: loser should be WHITE';
    }
    else {
        is $result->{'winner'}, 'WHITE',
            'WHITE has Ippon: winner should be WHITE';
        is $result->{'loser'}, 'BLUE', 'WHITE has Ippon: loser should be BLUE';

    }
};

subtest '_has_winner' => sub {
    my $sim = VWJL::Simulator->new;
    my $scoreboard = {
            'clock' => {
                'seconds'               => 0,
                'minutes'               => 0,
                'total_elapsed_seconds' => 240
            },
            'blue' => {
                'wazari'  => 0,
                'shido'   => 0,
                'athlete' => 'BLUE',
                'ippon'   => 0,
            },
            'white' => {
                'ippon'   => 1,
                'wazari'  => 0,
                'athlete' => 'WHITE',
                'shido'   => 0
            }
        };

    is $sim->_has_winner($scoreboard), 1, '_has_winner White Ippon';

    $scoreboard->{white}{ippon} = 0;
    $scoreboard->{white}{shido} = 3;
    is $sim->_has_winner($scoreboard), 1, '_has_winner White 3 Shido';

    $scoreboard->{white}{shido} = 2;
    is $sim->_has_winner($scoreboard), 0, '_has_winner White 2 Shido, no winner';

    $scoreboard->{blue}{ippon} = 1;
    $scoreboard->{white}{shido} = 0;
    is $sim->_has_winner($scoreboard), 1, '_has_winner Blue Ippon';

    $scoreboard->{blue}{ippon} = 0;
    $scoreboard->{white}{wazari} = 1;
    is $sim->_has_winner($scoreboard), 0, '_has_winner White Wazari x1, no winner';

    $scoreboard->{white}{wazari} = 2;
    is $sim->_has_winner($scoreboard), 1, '_has_winner White Wazari x2';
};

subtest '_won_lost' => sub {
    my $sim = VWJL::Simulator->new;
    my $scoreboard = {
            'clock' => {
                'seconds'               => 0,
                'minutes'               => 0,
                'total_elapsed_seconds' => 240
            },
            'blue' => {
                'wazari'  => 0,
                'shido'   => 0,
                'athlete' => 'BLUE',
                'ippon'   => 0,
            },
            'white' => {
                'ippon'   => 1,
                'wazari'  => 0,
                'athlete' => 'WHITE',
                'shido'   => 0
            }
        };

    my $result = $sim->_won_lost($scoreboard);
    is $result->[0], "WHITE", '_won_lost, White won';
    is $result->[1], "BLUE", '_won_lost, Blue lost';


    $scoreboard->{white}{ippon} = 0;
    $scoreboard->{white}{shido} = 3;
    $result = $sim->_won_lost($scoreboard);
    is $result->[0], "BLUE", '_won_lost, Blue won';
    is $result->[1], "WHITE", '_won_lost, White lost';
};



done_testing;
