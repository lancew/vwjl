package vwjl;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;
use Dancer2::Plugin::Passphrase;
use DBI;

use VWJL::Infrastructure;

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
    my $inf = VWJL::Infrastructure->new;

    my $phrase = passphrase( params->{'password'} )->generate;

    unless ( params->{user} && params->{password} && params->{password2} ) {
        return template 'register' =>
            { error => "All fields must be filled" };
    }

    unless ( params->{password} eq params->{password2} ) {
        return template 'register' => { error => "Passwords must match" };
    }

    if ( $inf->is_username_in_db( params->{user} ) ) {
        return template 'register' =>
            { error => "This user name already exists in the system" };
    }

    $inf->add_user(
        username => params->{user}, 
        passphrase => $phrase->rfc2307
    );


    redirect '/login';
};

sub _is_valid {
    my ( $user, $password ) = @_;


    my $inf = VWJL::Infrastructure->new;
    my $user_data = $inf->get_user_data($user);


    return false unless $user_data;

    if ( passphrase($password)->matches( $user_data->{passphrase} ) ) {
        return true;
    }
    else {
        return false;
    }
}


true;
