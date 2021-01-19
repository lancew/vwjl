package VWJL::Admin;
require 5.00808;

use utf8;
use Carp qw/carp croak/;
use Moo;
use VWJL::Infrastructure;

sub get_migration_data {
    my $inf = VWJL::Infrastructure->new;

    my %migration_data;

    eval {
        $migration_data{'db_migration_level'}
            = $inf->dbh->selectrow_array(
            'SELECT db_migration_level FROM system');

        $migration_data{'users'}
            = $inf->dbh->selectall_arrayref( 'SELECT * from accounts',
            { 'Slice' => {} } );

        $migration_data{'competitions'}
            = $inf->dbh->selectall_arrayref( 'SELECT * from competitions',
            { 'Slice' => {} } );

    } or carp 'NO DATABASE APPEARS TO BE PRESENT';

    my @file_list = $inf->get_migration_files;
    $file_list[-1] =~ /^(\d{3})/x;

    if ($1) {
        $migration_data{'file_migration_level'} = $1 if $1;
    }

    return %migration_data;
}

sub run_migrations {
    my $inf = VWJL::Infrastructure->new;

    my $db_migration_level = -1;
    eval {
        $db_migration_level
            = $inf->dbh->selectrow_array(
            'SELECT db_migration_level FROM system');
    } or carp 'UNABLE TO FIND MIGRATION LEVEL IN DB';

    my @migration_files = $inf->get_migration_files;
    my $dir             = "$FindBin::Bin/../db";

    for my $file ( sort @migration_files ) {
        my $migration;

        $file =~ /(\d{3})/x;
        if ($1) {
            $migration = $1;
        }

        if ( $db_migration_level < $migration ) {

            my $filename = $dir . '/' . $file;
            local $/ = undef;
            open( my $fh, '<:encoding(UTF-8)', $filename )
                or croak "Could not open file '$filename' $!";
            my $sql = <$fh>;
            close $fh;

            $inf->dbh->do($sql);
            $inf->dbh->do( 'UPDATE system SET db_migration_level = ?',
                undef, $migration );
        }

    }
    return 1;
}

1;
