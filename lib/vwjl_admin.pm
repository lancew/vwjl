package vwjl_admin;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use DBI;
use FindBin;

our $VERSION = '0.1';

use VWJL::Infrastructure;
use VWJL::Simulator;
use Games::Tournament::RoundRobin;
use Sort::Rank 'rank_sort';

get '/' => sub {
    redirect '/' unless session('admin');

    template 'admin/index' => { 'title' => 'VWJL Admin' };
};

get '/users' => sub {
    redirect '/' unless session('admin');

    my $inf = VWJL::Infrastructure->new;

    my $users = $inf->get_athletes;

    my $total_users = 0 + @{$users};

    template 'admin/users' => {
        'title'     => 'VWJL Admin',
        users       => $users,
        total_users => $total_users
    };
};

get '/competitions' => sub {
    redirect '/' unless session('admin');

    my $inf = VWJL::Infrastructure->new;

    my $competitions = $inf->get_competitions;

    template 'admin/competitions' => { competitions => $competitions, };
};

get '/competition/:competition_id' => sub {
    redirect '/' unless session('admin');
    my $inf = VWJL::Infrastructure->new;

    my $comp = $inf->get_competition(
        competition_id => route_parameters->get('competition_id'), );

    template 'admin/competition' => { competition => $comp, };
};

get '/competition/:competition_id/simulate' => sub {
    redirect '/' unless session('admin');
    my $inf = VWJL::Infrastructure->new;

    my $comp = $inf->get_competition(
        competition_id => route_parameters->get('competition_id'), );

    my @athletes;
    my $athletes = $comp->{entries};

    for my $key ( keys %$athletes ) {
        push @athletes, $athletes->{$key}{username};
    }

    my $schedule
        = Games::Tournament::RoundRobin->new( league => \@athletes, );

    session 'tournament' => $schedule;

    template 'admin/competition_sim' => {
        competition => $comp,
        schedule    => $schedule->wholeSchedule,
        tournament  => $schedule,
        status      => 'planning',
    };
};

post '/competition/:competition_id/simulate' => sub {
    redirect '/' unless session('admin');
    my $inf = VWJL::Infrastructure->new;

    use Data::Dumper;
    $Data::Dumper::Sortkeys = 1;

    my $comp = $inf->get_competition(
        competition_id => route_parameters->get('competition_id'), );

    my $tournament = session('tournament');
    my $simulator  = VWJL::Simulator->new;

    my @results;
    my $round_count = 0;
    for my $round ( @{ $tournament->byelessSchedule } ) {
        $round_count++;
        for my $contest (@$round) {
            push @results,
                $simulator->simulate(
                competition_id => route_parameters->get('competition_id'),
                athlete_white  => $contest->[0],
                athlete_blue   => $contest->[1],
                round          => $round_count,
                );
        }
    }

    $simulator->store_results(
        competition => $comp,
        results     => \@results,
    );

    my $ranks = $simulator->calculate_ranking( \@results );

    template 'admin/competition_sim' => {
        competition => $comp,
        schedule    => $tournament->wholeSchedule,
        tournament  => $tournament,
        status      => 'ran',
        results     => \@results,
        ranking     => $ranks,
    };
};

# -----------------------------------------------------
#  TODO: This needs doing properly
# -----------------------------------------------------

get '/database' => sub {
    #redirect '/' unless session('admin');

    my $inf = VWJL::Infrastructure->new;

    my ( $db_migration_level, $users, $competitions );

    eval {
        $db_migration_level
            = $inf->dbh->selectrow_array(
            'SELECT db_migration_level FROM system');

        $users = $inf->dbh->selectall_arrayref( 'SELECT * from accounts',
            { 'Slice' => {} } );

        $competitions
            = $inf->dbh->selectall_arrayref( 'SELECT * from competitions',
            { 'Slice' => {} } );

    };

    template 'admin/database' => {
        users              => $users,
        competitions       => $competitions,
        db_migration_level => $db_migration_level,
    };
};

post '/database' => sub {
    my $inf = VWJL::Infrastructure->new;

    my $db_migration_level = -1;
    eval {
        $db_migration_level
            = $inf->dbh->selectrow_array(
            'SELECT db_migration_level FROM system');
    };

    my $dir = "$FindBin::Bin/../db";
    opendir my $dh, $dir or die "Could not open '$dir' for reading '$!'\n";
    my @migration_files = readdir $dh;
    closedir $dh;

    for my $file ( sort @migration_files ) {

        next unless $file =~ /(\d{3})/;
        my $migration = $1;

        if ( $db_migration_level < $migration ) {

            my $filename = $dir . '/' . $file;
            $/ = undef;
            open( my $fh, '<:encoding(UTF-8)', $filename )
                or die "Could not open file '$filename' $!";
            my $sql = <$fh>;
            close $fh;

            $inf->dbh->do($sql);
            $inf->dbh->do( 'UPDATE system SET db_migration_level = ?',
                undef, $migration );
        }

    }

    redirect '/admin/database';
};

1;
