package VWJL::Infrastructure::Database;

sub get_athlete {
    my %args = @_;

    my %fake_data = (
        'lancew' => {
            name      => 'Hifumi Maruyama',
            weight    => '65.2',
            dojo      => 'Kodokan',
            country   => 'Japan',
            sensei    => 'Inoue Kosei',
            wins      => 0,
            losses    => 0,
            biography =>
                'Just a Judoka trying to make his way in the universe',
            physical => {
                fitness  => 10,
                form     => 11,
                fatigue  => 12,
                left_arm => {
                    strength => 50,
                    fatigue  => 50,
                    injury   => 50,
                },
                right_arm => {
                    fatigue  => 51,
                    injury   => 51,
                    strength => 51,
                },
                left_leg => {
                    fatigue  => 52,
                    injury   => 52,
                    strength => 52,
                },
                right_leg => {
                    strength => 53,
                    fatigue  => 53,
                    injury   => 53,
                },
            },
            waza => {
                ippon_seoi_nage => {
                    attack  => 80,
                    defense => 81,
                },
                uchi_mata => {
                    attack  => 90,
                    defense => 91,
                },
            },
        }
    );

    my $athlete = $fake_data{ $args{'user'} };

    return $athlete;
}

true;

