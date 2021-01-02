package vwjl_admin;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use DBI;

our $VERSION = '0.1';

use VWJL::Infrastructure;

get '/' => sub {
    redirect '/' unless session('admin');

    template 'admin/index' => { 'title' => 'VWJL Admin' };
};

get '/users' => sub {
    redirect '/' unless session('admin');

    my $inf = VWJL::Infrastructure->new;

    my $users = $inf->get_users;

    my $total_users = 0 + @{$users};

    template 'admin/users' => {
        'title'     => 'VWJL Admin',
        users       => $users,
        total_users => $total_users
    };
};

get '/database' => sub {
    #redirect '/' unless session('admin');

    my $output;

    my $dbh = DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
        'postgres', 'somePassword', { AutoCommit => 1 } );

    $dbh->do( '
   CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	passphrase VARCHAR ( 150 ) NOT NULL,
	created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP); 
    ' );

    $dbh->do( "
      INSERT INTO accounts
      (username,passphrase,created_on)
      VALUES
      ( 'lancew', '{CRYPT}\$2a\$04\$EB5QjLwL8N6.SOLRMqVVGe.r3ObhdFeWUwkM0XQl2nxOCISspH5I6', localtimestamp)
    
    " );

    $dbh->do( '
        CREATE TABLE athletes (
            athlete_id serial PRIMARY KEY,
            username varchar(50) UNIQUE NOT NULL,
            biography TEXT,
            country VARCHAR(100),
            credits INTEGER DEFAULT 0,
            dojo    VARCHAR(100),
            left_arm_fatigue   INTEGER DEFAULT 1,
            left_arm_injury    INTEGER DEFAULT 1, 
            left_arm_strength  INTEGER DEFAULT 1,
            left_leg_fatigue   INTEGER DEFAULT 1,
            left_leg_injury    INTEGER DEFAULT 1, 
            left_leg_strength  INTEGER DEFAULT 1,
            losses  INTEGER DEFAULT 0,
            name    VARCHAR(100),
            physical_fatigue   INTEGER DEFAULT 1,
            physical_fitness   INTEGER DEFAULT 1,
            physical_form      INTEGER DEFAULT 1,
            right_arm_fatigue  INTEGER DEFAULT 1,
            right_arm_injury   INTEGER DEFAULT 1,
            right_arm_strength INTEGER DEFAULT 1,
            right_leg_fatigue  INTEGER DEFAULT 1,
            right_leg_injury   INTEGER DEFAULT 1,
            right_leg_strength INTEGER DEFAULT 1,
            sensei  VARCHAR(100),
            waza_ippon_seoi_nage_attack  INTEGER DEFAULT 1,
            waza_ippon_seoi_nage_defense INTEGER DEFAULT 1,
            waza_uchi_mata_attack        INTEGER DEFAULT 1,
            waza_uchi_mata_defense       INTEGER DEFAULT 1,
            weight  DECIMAL,
            wins    INTEGER DEFAULT 0
        )
    ' );

    $dbh->do("INSERT INTO athletes (username) VALUES ('lancew')");

    my $users = $dbh->selectall_arrayref( 'SELECT * from accounts',
        { 'Slice' => {} } );

    my $athletes = $dbh->selectall_arrayref( 'SELECT * from athletes',
        { 'Slice' => {} } );

    $dbh->disconnect;

    template 'admin/database' => {
        users    => $users,
        athletes => $athletes,
        output   => $output,
    };
};

true;
