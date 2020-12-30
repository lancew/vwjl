package vwjl;
use Dancer2;
use Dancer2::Plugin::Auth::Tiny;

our $VERSION = '0.1';

get '/' => sub {
    # Temp add user and admin session
    session 'user'  => 'lancew';
    session 'admin' => true;

    template 'index' => { 'title' => 'vwjl' };
};

get '/login' => sub {
    # put 'return_url' in a hidden form field
    template 'login' => { return_url => params->{return_url} };
};

get '/logout' => sub {
    app->destroy_session;
    redirect '/';
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

sub _is_valid {
    my ( $user, $password ) = @_;

    if ( $user eq 'lancew' && $password eq '' ) {
        return true;
    }
    else {
        return false;
    }
}

true;
