package VWJL;

use Moo;
use lib './MyLib';
use DBI;

use namespace::clean;

my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');

sub get_user {
    my ($user_id ) = @_;

    $dbh->func( 'users', 'CSV', './data/users_csv', 'ad_catalog' );
    $dbh->selectrow_hashref( 
        'SELECT * FROM users WHERE id = ?',
        { Slice => {} }, 
        $user_id 
    );
}


1;