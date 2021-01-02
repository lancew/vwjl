package vwjl;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use Dancer2::Plugin::Passphrase;
use DBI;

our $VERSION = '0.1';

get '/' => sub {
    template 'index' => { 'title' => 'vwjl' };
};

get '/login' => sub {
    # put 'return_url' in a hidden form field
    template 'login' => { return_url => params->{return_url} };
};

post '/login' => sub {
    if ( _is_valid( params->{user}, params->{password} ) ) {
        warn "Logging in " . params->{user};
        session 'user' => params->{user};
        
        if ( params->{user} eq 'lancew' ) {
            session 'admin' => true;
        }

        return redirect params->{return_url} || '/';
    }
    else {
        template 'login' => { error => "invalid username or password" };
    }
};

get '/logout' => sub {
    app->destroy_session;
    redirect '/';
};

get '/register' => sub {
    template 'register';
};

post '/register' => sub {
    my $phrase = passphrase( params->{'password'} )->generate;
   
    unless (
        params->{user} && params->{password} && params->{password2}
    ) {
        warn 'Missing Fields';
        return template 'register' => { error => "All fields must be filled"};
    }

    unless (params->{password} eq params->{password2}) {
        warn 'Passwords must match';
        return template 'register' => { error => "Passwords must match"};
    }

    if (_is_username_in_db( params->{user} )) {
        warn 'Username already exists';
        return template 'register' => { error => "This user name already exists in the system"};
    }


    warn '----------------------+++++++++++', $phrase->rfc2307;

    my $dbh = DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
        'postgres', 'somePassword', { AutoCommit => 1 } );
    
    $dbh->do( "
      INSERT INTO accounts
      (username,email,passphrase,created_on)
      VALUES
      ( ?, ?,? , localtimestamp)
    ",undef, params->{user}, '-',$phrase->rfc2307 );

    $dbh->disconnect;

    redirect '/login';
};



sub _is_valid {
    my ( $user, $password ) = @_;

    my $dbh = DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
        'postgres', 'somePassword', { AutoCommit => 1 } );
    my $user_data = $dbh->selectrow_hashref( 'SELECT * FROM accounts WHERE username = ?',
        undef, $user );
    $dbh->disconnect;



    return false unless $user_data;
    


    if ( passphrase($password)->matches($user_data->{passphrase}) ) {
        return true;
    }
    else {
        return false;
    }
}

sub _is_username_in_db {
    my $user = shift;

    my $dbh = DBI->connect( "dbi:Pg:dbname=postgres;host=localhost",
        'postgres', 'somePassword', { AutoCommit => 1 } );
    my $user_data = $dbh->selectrow_hashref( 'SELECT username FROM accounts WHERE username = ?',
        undef, $user );
    $dbh->disconnect;

    return false unless $user_data;
}





true;
