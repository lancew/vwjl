package VWJL::Admin;

use Moo;
use VWJL::Infrastructure;

sub get_migration_data {
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

sub run_migrations {
    my $inf = VWJL::Infrastructure->new;

    my $db_migration_level = -1;
    eval {
        $db_migration_level
            = $inf->dbh->selectrow_array(
            'SELECT db_migration_level FROM system');
    };

    my @migration_files = $inf->get_migration_files;
    my $dir             = "$FindBin::Bin/../db";

    for my $file ( sort @migration_files ) {
        my $migration;

        $file =~ /(\d{3})/;
        if ($1) {
            $migration = $1;
        }

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
}



1;
