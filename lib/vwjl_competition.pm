package vwjl_competition;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

use VWJL::Infrastructure;

get '/' => sub {
    redirect '/' unless session('user');

    my $inf          = VWJL::Infrastructure->new;
    my $competitions = $inf->get_competitions;
    my $athlete = $inf->get_athlete_data( user => session('user') );

    my $comps_entered;
    for my $c ( @{$athlete->{competition_entries}}) {
        $comps_entered->{$c->{id}}++;
    }

    template 'competition/index' => { 
        competitions => $competitions, 
        athlete     => $athlete,
        comps_entered => $comps_entered,
    };
};

get '/:competition_id/register' => sub {
    redirect '/' unless session('user');

    my $inf         = VWJL::Infrastructure->new;
    my $competition = $inf->get_competition(
        competition_id => route_parameters->get('competition_id') );
    my $athlete = $inf->get_athlete_data( user => session('user') );

    template 'competition/register' => {
        competition => $competition,
        athlete     => $athlete,
        status      => 'view',
    };
};

post '/:competition_id/register' => sub {
    redirect '/' unless session('user');

    my $inf         = VWJL::Infrastructure->new;
    my $competition = $inf->get_competition(
        competition_id => route_parameters->get('competition_id') );
    my $athlete = $inf->get_athlete_data( user => session('user') );

    if ( $athlete->{credits} >= $competition->{entry_fee} ) {
        $inf->update_athlete(
            field => 'credits',
            user  => session('user'),
            value => ( $athlete->{'credits'} - $competition->{'entry_fee'} ),
        );

        $inf->add_user_to_competition(
            athlete_id     => $athlete->{id},
            competition_id => $competition->{id},
        );

        template 'competition/register' => {
            competition => $competition,
            athlete     => $athlete,
            status      => 'confirmed',
        };
    }
    else {
        template 'competition/register' => {
            competition => $competition,
            athlete     => $athlete,
            status      => 'view',
            error       => 'Sorry you do not have enough credits to register'
        };
    }
};

true;

