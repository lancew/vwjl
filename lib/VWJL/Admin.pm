package VWJL::Admin;

use Moo;
use VWJL::Infrastructure;

sub get_migration_data {
    my $self = shift;
    my $inf = VWJL::Infrastructure->new;

    my %data;

    eval {
        $data{'db_migration_level'}
            = $inf->dbh->selectrow_array(
            'SELECT db_migration_level FROM system');

        $data{'users'} = $inf->dbh->selectall_arrayref( 'SELECT * from accounts',
            { 'Slice' => {} } );

        $data{'competitions'}
            = $inf->dbh->selectall_arrayref( 'SELECT * from competitions',
            { 'Slice' => {} } );

    };

    my @file_list = $inf->get_migration_files;
    $file_list[-1] =~ /^(\d{3})/;

    if ($1) {
        $data{'file_migration_level'} = $1 if $1;
    }

    return %data;
}

1;
