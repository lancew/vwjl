use strict;
use warnings;

use Test::More;
use Test::MockModule;
use Test::Deep;


use VWJL::Simulator;

use Data::Dumper;


{
    my $inf = Test::MockModule->new('VWJL::Infrastructure');
    $inf->mock(
        'dbh' => sub { return }
    );
    $inf->mock(
        'update_athlete' => sub { return }
    );
    $inf->mock(
        'get_athlete_data' => sub{
            my ($self, %args) = @_;

			if ($args{user} eq 'WHITE') {
              return {
                  username => $args{user},
                  wins     => 10,
                  losses   => 20,
				  waza_levels => {
                     ippon_seoi_nage => {
                        attack  => 100,
                        defence => 100,
                     },
                  }
              };
			} else {
              return {
                  username => $args{user},
                  wins     => 0,
                  losses   => 0,
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
        athlete_blue  => 'BLUE',
        athlete_white => 'WHITE',
        competition_id => 123,
        round          => 1,
    );

    cmp_deeply $result, {
          'commentary' => 'Some stuff happened',
          'round' => 1,
          'scoreboard' => {  
                            'clock' => {
                                         'seconds' => 0,
                                         'minutes' => 4,
                                         'total_elapsed_seconds' => 240
                                       },
                            'blue' => { 
                                        'wazari' => 1,
                                        'shido' => 2,
                                        'athlete' => 'BLUE',
                                        'ippon' => 0
                                      },
                            'white' => {
                                         'ippon' => 1,
                                         'wazari' => 1,
                                         'athlete' => 'WHITE',
                                         'shido' => 0
                                       }
                          },
          'loser' => ignore(),
          'winner' => ignore(), 
    }, 'simulate returns expected output';



}




done_testing;
