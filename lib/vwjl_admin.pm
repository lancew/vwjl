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

    my $users = [ 'Lance Wicks', 'Joe Bloggs', 'Jane Doe', ];

    my $total_users = 0 + @{$users};

    template 'admin/users' => {
        'title'     => 'VWJL Admin',
        users       => $users,
        total_users => $total_users
    };
};

get '/database' => sub {
    # redirect '/' unless session('admin');

    my $output;

    my $dbh = DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
        'postgres', 'somePassword', { AutoCommit => 1 } );

    my $rv = $dbh->do( '
   CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP); 
    ' );

    $rv = $dbh->do( "
      INSERT INTO accounts
      (username,password,email,created_on)
      VALUES
      ( 'lancew', 'lancew', 'lw\@judocoach.com', localtimestamp)
    
    " );

    my $users = $dbh->selectall_arrayref( 'SELECT username from accounts',
        { 'Slice' => {} } );

    use Data::Dumper;
    warn Dumper $users;

    $dbh->disconnect;

    template 'admin/database' => {
        users  => $users,
        output => $output,
    };
};

true;
