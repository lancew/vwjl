package vwjl_admin;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use DBI;

our $VERSION = '0.1';

get '/' => sub {
    redirect '/' unless session('admin');

    template 'admin/index' => { 'title' => 'VWJL Admin' };
};

get '/users' => sub {
    redirect '/' unless session('admin');

    my $dbh = DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
        'postgres', 'somePassword', { AutoCommit => 1 } );
    my $users = $dbh->selectall_arrayref( 'SELECT username from accounts',
        { 'Slice' => {} } );
    $dbh->disconnect;

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

    my $rv = $dbh->do( '
   CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	passphrase VARCHAR ( 150 ) NOT NULL,
	created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP); 
    ' );

    $rv = $dbh->do( "
      INSERT INTO accounts
      (username,passphrase,created_on)
      VALUES
      ( 'lancew', '{CRYPT}\$2a\$04\$EB5QjLwL8N6.SOLRMqVVGe.r3ObhdFeWUwkM0XQl2nxOCISspH5I6', localtimestamp)
    
    " );

    my $users = $dbh->selectall_arrayref( 'SELECT * from accounts',
        { 'Slice' => {} } );

    $dbh->disconnect;

    template 'admin/database' => {
        users  => $users,
        output => $output,
    };
};

true;
