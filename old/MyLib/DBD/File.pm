# -*- perl -*-
#
#   DBD::File - A base class for implementing DBI drivers that
#               act on plain files
#
#  This module is currently maintained by
#
#      Jeff Zucker
#      <jeff@vpservices.com>
#
#  The original author is Jochen Wiedmann.
#
#  Copyright (C) 1998 by Jochen Wiedmann
#
#  All rights reserved.
#
#  You may distribute this module under the terms of either the GNU
#  General Public License or the Artistic License, as specified in
#  the Perl README file.
#

require 5.004;
use strict;


require DynaLoader;
require DBI;
require SQL::Statement;
require SQL::Eval;
my $haveFileSpec = eval { require File::Spec };

package DBD::File;

use vars qw(@ISA $VERSION $drh $err $errstr $sqlstate);

@ISA = qw(DynaLoader);

$VERSION = '0.22';      #

$err = 0;		# holds error code   for DBI::err
$errstr = "";		# holds error string for DBI::errstr
$sqlstate = "";         # holds error state  for DBI::state
$drh = undef;		# holds driver handle once initialised


sub driver ($;$) {
    my($class, $attr) = @_;
    my $drh = eval '$' . $class . "::drh";
    if (!$drh) {
	if (!$attr) { $attr = {} };
	if (!exists($attr->{Attribution})) {
	    $attr->{Attribution} = "$class by Jochen Wiedmann";
	}
	if (!exists($attr->{Version})) {
	    $attr->{Version} = eval '$' . $class . '::VERSION';
        }
        if (!exists($attr->{Err})) {
	    $attr->{Err} = eval '\$' . $class . '::err';
        }
        if (!exists($attr->{Errstr})) {
	    $attr->{Errstr} = eval '\$' . $class . '::errstr';
        }
        if (!exists($attr->{State})) {
	    $attr->{State} = eval '\$' . $class . '::state';
        }
        if (!exists($attr->{Name})) {
	    my $c = $class;
	    $c =~ s/^DBD\:\://;
	    $attr->{Name} = $c;
        }

        $drh = DBI::_new_drh($class . "::dr", $attr);
    }
    $drh;
}


package DBD::File::dr; # ====== DRIVER ======

$DBD::File::dr::imp_data_size = 0;

sub connect ($$;$$$) {
    my($drh, $dbname, $user, $auth, $attr)= @_;

    # create a 'blank' dbh
    my $this = DBI::_new_dbh($drh, {
	'Name' => $dbname,
	'USER' => $user, 
	'CURRENT_USER' => $user,
    });

    if ($this) {
	my($var, $val);
	$this->{f_dir} = $haveFileSpec ? File::Spec->curdir() : '.';
	while (length($dbname)) {
	    if ($dbname =~ s/^((?:[^\\;]|\\.)*?);//s) {
		$var = $1;
	    } else {
		$var = $dbname;
		$dbname = '';
	    }
	    if ($var =~ /^(.+?)=(.*)/s) {
		$var = $1;
		($val = $2) =~ s/\\(.)/$1/g;
		$this->{$var} = $val;
	    }
	}
    }

    $this;
}

sub data_sources ($;$) {
    my($drh, $attr) = @_;
    my($dir) = ($attr and exists($attr->{'f_dir'})) ?
	$attr->{'f_dir'} : $haveFileSpec ? File::Spec->curdir() : '.';
    my($dirh) = Symbol::gensym();
    if (!opendir($dirh, $dir)) {
        DBI::set_err($drh, 1, "Cannot open directory $dir");
	return undef;
    }
    my($file, @dsns, %names, $driver);
    if ($drh->{'ImplementorClass'} =~ /^dbd\:\:([^\:]+)\:\:/i) {
	$driver = $1;
    } else {
	$driver = 'File';
    }
    while (defined($file = readdir($dirh))) {
	my $d = $haveFileSpec ?
	    File::Spec->catdir($dir, $file) : "$dir/$file";
	if ($file ne ($haveFileSpec ? File::Spec->curdir() : '.')
	    and  $file ne ($haveFileSpec ? File::Spec->updir() : '..')
	    and  -d $d) {
	    push(@dsns, "DBI:$driver:f_dir=$d");
	}
    }
    @dsns;
}

sub disconnect_all {
}

sub DESTROY {
    undef;
}


package DBD::File::db; # ====== DATABASE ======

$DBD::File::db::imp_data_size = 0;


sub prepare ($$;@) {
    my($dbh, $statement, @attribs)= @_;

    # create a 'blank' dbh
    my $sth = DBI::_new_sth($dbh, {'Statement' => $statement});

    if ($sth) {
	$@ = '';
	my $class = $sth->FETCH('ImplementorClass');
	$class =~ s/::st$/::Statement/;
###jz
#         my($stmt) = eval { $class->new($statement) };
#
	my($stmt);
        my $sversion = $SQL::Statement::VERSION;
	if ($SQL::Statement::VERSION > 1) {
            my $parser = $dbh->{csv_sql_parser_object};
            eval { $parser ||= $dbh->func('csv_cache_sql_parser_object') };
            if ($@) {
                undef $@;
  	        $stmt = eval { $class->new($statement) };
	    }
            else {
  	        $stmt = eval { $class->new($statement,$parser) };
	    }
        }
        else {
	    $stmt = eval { $class->new($statement) };
	}
#
###jzend
	if ($@) {
	    DBI::set_err($dbh, 1, $@);
	    undef $sth;
	} else {
	    $sth->STORE('f_stmt', $stmt);
	    $sth->STORE('f_params', []);
	    $sth->STORE('NUM_OF_PARAMS', scalar($stmt->params()));
	}
    }

    $sth;
}

sub disconnect ($) {
    1;
}

sub FETCH ($$) {
    my ($dbh, $attrib) = @_;
    if ($attrib eq 'AutoCommit') {
	return 1;
    } elsif ($attrib eq (lc $attrib)) {
	# Driver private attributes are lower cased
	return $dbh->{$attrib};
    }
    # else pass up to DBI to handle
    return $dbh->DBD::_::db::FETCH($attrib);
}

sub STORE ($$$) {
    my ($dbh, $attrib, $value) = @_;
    if ($attrib eq 'AutoCommit') {
	return 1 if $value; # is already set
	die("Can't disable AutoCommit");
    } elsif ($attrib eq (lc $attrib)) {
	# Driver private attributes are lower cased
	$dbh->{$attrib} = $value;
	return 1;
    }
    return $dbh->DBD::_::db::STORE($attrib, $value);
}

sub DESTROY ($) {
    undef;
}

sub type_info_all ($) {
    [
     {   TYPE_NAME         => 0,
	 DATA_TYPE         => 1,
	 PRECISION         => 2,
	 LITERAL_PREFIX    => 3,
	 LITERAL_SUFFIX    => 4,
	 CREATE_PARAMS     => 5,
	 NULLABLE          => 6,
	 CASE_SENSITIVE    => 7,
	 SEARCHABLE        => 8,
	 UNSIGNED_ATTRIBUTE=> 9,
	 MONEY             => 10,
	 AUTO_INCREMENT    => 11,
	 LOCAL_TYPE_NAME   => 12,
	 MINIMUM_SCALE     => 13,
	 MAXIMUM_SCALE     => 14,
     },
     [ 'VARCHAR', DBI::SQL_VARCHAR(),
       undef, "'","'", undef,0, 1,1,0,0,0,undef,1,999999
       ],
     [ 'CHAR', DBI::SQL_CHAR(),
       undef, "'","'", undef,0, 1,1,0,0,0,undef,1,999999
       ],
     [ 'INTEGER', DBI::SQL_INTEGER(),
       undef,  "", "", undef,0, 0,1,0,0,0,undef,0,  0
       ],
     [ 'REAL', DBI::SQL_REAL(),
       undef,  "", "", undef,0, 0,1,0,0,0,undef,0,  0
       ],
     [ 'BLOB', DBI::SQL_LONGVARBINARY(),
       undef, "'","'", undef,0, 1,1,0,0,0,undef,1,999999
       ],
     [ 'BLOB', DBI::SQL_LONGVARBINARY(),
       undef, "'","'", undef,0, 1,1,0,0,0,undef,1,999999
       ],
     [ 'TEXT', DBI::SQL_LONGVARCHAR(),
       undef, "'","'", undef,0, 1,1,0,0,0,undef,1,999999
       ]
     ]
}


{
    my $names = ['TABLE_QUALIFIER', 'TABLE_OWNER', 'TABLE_NAME',
                 'TABLE_TYPE', 'REMARKS'];

    sub table_info ($) {
	my($dbh) = @_;
	my($dir) = $dbh->{f_dir};
	my($dirh) = Symbol::gensym();
	if (!opendir($dirh, $dir)) {
	    DBI::set_err($dbh, 1, "Cannot open directory $dir");
	    return undef;
	}
	my($file, @tables, %names);
	while (defined($file = readdir($dirh))) {
	    if ($file ne '.'  &&  $file ne '..'  &&  -f "$dir/$file") {
		my $user = eval { getpwuid((stat(_))[4]) };
		push(@tables, [undef, $user, $file, "TABLE", undef]);
	    }
	}
	if (!closedir($dirh)) {
	    DBI::set_err($dbh, 1, "Cannot close directory $dir");
	    return undef;
	}

	my $dbh2 = $dbh->{'csv_sponge_driver'};
	if (!$dbh2) {
	    $dbh2 = $dbh->{'csv_sponge_driver'} = DBI->connect("DBI:Sponge:");
	    if (!$dbh2) {
	        DBI::set_err($dbh, 1, $DBI::errstr);
		return undef;
	    }
	}

	# Temporary kludge: DBD::Sponge dies if @tables is empty. :-(
	return undef if !@tables;

	my $sth = $dbh2->prepare("TABLE_INFO", { 'rows' => \@tables,
						 'NAMES' => $names });
	if (!$sth) {
	    DBI::set_err($dbh, 1, $dbh2->errstr());
	}
	$sth;
    }
}
sub list_tables ($) {
    my $dbh = shift;
    my($sth, @tables);
    if (!($sth = $dbh->table_info())) {
	return ();
    }
    while (my $ref = $sth->fetchrow_arrayref()) {
	push(@tables, $ref->[2]);
    }
    @tables;
}

sub quote ($$;$) {
    my($self, $str, $type) = @_;
    if (defined($type)  &&
	($type == DBI::SQL_NUMERIC()   ||
	 $type == DBI::SQL_DECIMAL()   ||
	 $type == DBI::SQL_INTEGER()   ||
	 $type == DBI::SQL_SMALLINT()  ||
	 $type == DBI::SQL_FLOAT()     ||
	 $type == DBI::SQL_REAL()      ||
	 $type == DBI::SQL_DOUBLE()    ||
	 $type == DBI::TINYINT())) {
	return $str;
    }
    if (!defined($str)) { return "NULL" }
    $str =~ s/\\/\\\\/sg;
    $str =~ s/\0/\\0/sg;
    $str =~ s/\'/\\\'/sg;
    $str =~ s/\n/\\n/sg;
    $str =~ s/\r/\\r/sg;
    "'$str'";
}

sub commit ($) {
    my($dbh) = shift;
    if ($dbh->FETCH('Warn')) {
	warn("Commit ineffective while AutoCommit is on", -1);
    }
    1;
}

sub rollback ($) {
    my($dbh) = shift;
    if ($dbh->FETCH('Warn')) {
	warn("Rollback ineffective while AutoCommit is on", -1);
    }
    0;
}


package DBD::File::st; # ====== STATEMENT ======

$DBD::File::st::imp_data_size = 0;

sub bind_param ($$$;$) {
    my($sth, $pNum, $val, $attr) = @_;
    $sth->{f_params}->[$pNum-1] = $val;
    1;
}

sub execute {
    my $sth = shift;
    my $params;
    if (@_) {
	$sth->{'f_params'} = ($params = [@_]);
    } else {
	$params = $sth->{'f_params'};
    }
    my $stmt = $sth->{'f_stmt'};
    my $result = eval { $stmt->execute($sth, $params); };
    if ($@) {
        DBI::set_err($sth, 1, $@);
	return undef;
    }
    if ($stmt->{'NUM_OF_FIELDS'}  &&  !$sth->FETCH('NUM_OF_FIELDS')) {
	$sth->STORE('NUM_OF_FIELDS', $stmt->{'NUM_OF_FIELDS'});
    }
    return $result;
}

sub fetch ($) {
    my $sth = shift;
    my $data = $sth->{f_stmt}->{data};
    if (!$data  ||  ref($data) ne 'ARRAY') {
	DBI::set_err($sth, 1,
		     "Attempt to fetch row from a Non-SELECT statement");
	return undef;
    }
    my $dav = shift @$data;
    if (!$dav) {
	return undef;
    }
    if ($sth->FETCH('ChopBlanks')) {
	map { $_ =~ s/\s+$//; } @$dav;
    }
    $sth->_set_fbav($dav);
}
*fetchrow_arrayref = \&fetch;

sub FETCH ($$) {
    my ($sth, $attrib) = @_;
    return undef if ($attrib eq 'TYPE'); # Workaround for a bug in DBI 0.93
    return $sth->FETCH('f_stmt')->{'NAME'} if ($attrib eq 'NAME');
    if ($attrib eq 'NULLABLE') {
	my($meta) = $sth->FETCH('f_stmt')->{'NAME'}; # Intentional !
	if (!$meta) {
	    return undef;
	}
	my($names) = [];
	my($col);
	foreach $col (@$meta) {
	    push(@$names, 1);
	}
	return $names;
    }
    if ($attrib eq (lc $attrib)) {
	# Private driver attributes are lower cased
	return $sth->{$attrib};
    }
    # else pass up to DBI to handle
    return $sth->DBD::_::st::FETCH($attrib);
}

sub STORE ($$$) {
    my ($sth, $attrib, $value) = @_;
    if ($attrib eq (lc $attrib)) {
	# Private driver attributes are lower cased
	$sth->{$attrib} = $value;
	return 1;
    }
    return $sth->DBD::_::st::STORE($attrib, $value);
}

sub DESTROY ($) {
    undef;
}

sub rows ($) { shift->{'f_stmt'}->{'NUM_OF_ROWS'} };

sub finish ($) { 1; }


package DBD::File::Statement;

my $locking = $^O ne 'MacOS'  &&
              ($^O ne 'MSWin32' || !Win32::IsWin95())  &&
              $^O ne 'VMS';

@DBD::File::Statement::ISA = qw(SQL::Statement);

my $open_table_re =
    $haveFileSpec ?
    sprintf('(?:%s|%s�%s)',
	    quotemeta(File::Spec->curdir()),
	    quotemeta(File::Spec->updir()),
	    quotemeta(File::Spec->rootdir()))
    : '(?:\.?\.)?\/';
sub open_table ($$$$$) {
    my($self, $data, $table, $createMode, $lockMode) = @_;
    my $file = $table;
    if ($file !~ /^$open_table_re/o) {
	$file = $haveFileSpec ?
	    File::Spec->catfile($data->{Database}->{'f_dir'}, $table)
		: $data->{Database}->{'f_dir'} . "/$table";
    }
    my $fh;
    if ($createMode) {
	if (-f $file) {
	    die "Cannot create table $table: Already exists";
	}
	if (!($fh = IO::File->new($file, "a+"))) {
	    die "Cannot open $file for writing: $!";
	}
	if (!$fh->seek(0, 0)) {
	    die " Error while seeking back: $!";
	}
    } else {
	if (!($fh = IO::File->new($file, ($lockMode ? "r+" : "r")))) {
	    die " Cannot open $file: $!";
	}
    }
    binmode($fh);
    if ($locking) {
	if ($lockMode) {
	    if (!flock($fh, 2)) {
		die " Cannot obtain exclusive lock on $file: $!";
	    }
	} else {
	    if (!flock($fh, 1)) {
		die "Cannot obtain shared lock on $file: $!";
	    }
	}
    }
    my $columns = {};
    my $array = [];
    my $tbl = {
	file => $file,
	fh => $fh,
	col_nums => $columns,
	col_names => $array,
	first_row_pos => $fh->tell()
    };
    my $class = ref($self);
    $class =~ s/::Statement/::Table/;
    bless($tbl, $class);
    $tbl;
}


package DBD::File::Table;

@DBD::File::Table::ISA = qw(SQL::Eval::Table);

sub drop ($) {
    my($self) = @_;
    # We have to close the file before unlinking it: Some OS'es will
    # refuse the unlink otherwise.
    $self->{'fh'}->close();
    unlink($self->{'file'});
    return 1;
}

sub seek ($$$$) {
    my($self, $data, $pos, $whence) = @_;
    if ($whence == 0  &&  $pos == 0) {
	$pos = $self->{'first_row_pos'};
    } elsif ($whence != 2  ||  $pos != 0) {
	die "Illegal seek position: pos = $pos, whence = $whence";
    }
    if (!$self->{'fh'}->seek($pos, $whence)) {
	die "Error while seeking in " . $self->{'file'} . ": $!";
    }
}

sub truncate ($$) {
    my($self, $data) = @_;
    if (!$self->{'fh'}->truncate($self->{'fh'}->tell())) {
	die "Error while truncating " . $self->{'file'} . ": $!";
    }
    1;
}

1;


__END__

=head1 NAME

DBD::File - Base class for writing DBI drivers for plain files

=head1 SYNOPSIS

    use DBI;
    $dbh = DBI->connect("DBI:File:f_dir=/home/joe/csvdb")
        or die "Cannot connect: " . $DBI::errstr;
    $sth = $dbh->prepare("CREATE TABLE a (id INTEGER, name CHAR(10))")
        or die "Cannot prepare: " . $dbh->errstr();
    $sth->execute() or die "Cannot execute: " . $sth->errstr();
    $sth->finish();
    $dbh->disconnect();

=head1 DESCRIPTION

The DBD::File module is not a true DBI driver, but an abstract
base class for deriving concrete DBI drivers from it. The implication is,
that these drivers work with plain files, for example CSV files or
INI files. The module is based on the SQL::Statement module, a simple
SQL engine.

See L<DBI(3)> for details on DBI, L<SQL::Statement(3)> for details on
SQL::Statement and L<DBD::CSV(3)> or L<DBD::IniFile(3)> for example
drivers.


=head2 Metadata

The following attributes are handled by DBI itself and not by DBD::File,
thus they all work like expected:

    Active
    ActiveKids
    CachedKids
    CompatMode             (Not used)
    InactiveDestroy
    Kids
    PrintError
    RaiseError
    Warn                   (Not used)

The following DBI attributes are handled by DBD::File:

=over 4

=item AutoCommit

Always on

=item ChopBlanks

Works

=item NUM_OF_FIELDS

Valid after C<$sth->execute>

=item NUM_OF_PARAMS

Valid after C<$sth->prepare>

=item NAME

Valid after C<$sth->execute>; undef for Non-Select statements.

=item NULLABLE

Not really working, always returns an array ref of one's, as DBD::CSV
doesn't verify input data. Valid after C<$sth->execute>; undef for
Non-Select statements.

=back

These attributes and methods are not supported:

    bind_param_inout
    CursorName
    LongReadLen
    LongTruncOk

Additional to the DBI attributes, you can use the following dbh
attribute:

=over 4

=item f_dir

This attribute is used for setting the directory where CSV files are
opened. Usually you set it in the dbh, it defaults to the current
directory ("."). However, it is overwritable in the statement handles.

=back


=head2 Driver private methods

=over 4

=item data_sources

The C<data_sources> method returns a list of subdirectories of the current
directory in the form "DBI:CSV:f_dir=$dirname".

If you want to read the subdirectories of another directory, use

    my($drh) = DBI->install_driver("CSV");
    my(@list) = $drh->data_sources('f_dir' => '/usr/local/csv_data' );

=item list_tables

This method returns a list of file names inside $dbh->{'f_dir'}.
Example:

    my($dbh) = DBI->connect("DBI:CSV:f_dir=/usr/local/csv_data");
    my(@list) = $dbh->func('list_tables');

Note that the list includes all files contained in the directory, even
those that have non-valid table names, from the view of SQL. See
L<Creating and dropping tables> above.

=back


=head1 TODO

=over 4

=item Joins

The current version of the module works with single table SELECT's
only, although the basic design of the SQL::Statement module allows
joins and the likes.

=item Table name mapping

Currently it is not possible to use files with names like C<names.csv>.
Instead you have to use soft links or rename files. As an alternative
one might use, for example a dbh attribute 'table_map'. It might be a
hash ref, the keys being the table names and the values being the file
names.

=back


=head1 KNOWN BUGS

=over 8

=item *

The module is using flock() internally. However, this function is not
available on all platforms. Using flock() is disabled on MacOS and
Windows 95: There's no locking at all (perhaps not so important on
MacOS and Windows 95, as there's a single user anyways).

=back


=head1 AUTHOR AND COPYRIGHT

This module is currently maintained by

      Jeff Zucker
      <jeff@vpservices.com>

The original author is Jochen Wiedmann.

Copyright (C) 1998 by Jochen Wiedmann

All rights reserved.

You may distribute this module under the terms of either the GNU
General Public License or the Artistic License, as specified in
the Perl README file.

=head1 SEE ALSO

L<DBI(3)>, L<Text::CSV_XS(3)>, L<SQL::Statement(3)>


=cut
