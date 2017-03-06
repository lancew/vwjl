#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;

print header();
print start_html("e-Judo Test Area");
print h1("VIEW SHIAI");

# TODO: Hardcode the shiai for now
my $shiai = 'lancewlw1';

show_history($shiai);

sub show_history {
    my @shiai         = @_;
    my $history_table = "data/shiai_data/" . $shiai[0] . "_hst";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'history_db', 'CSV', $history_table, 'ad_catalog' );

    my $sql = "SELECT * FROM history_db ORDER BY DATE_TIME ASC ";

    my $sth = $dbh->prepare($sql);
    $sth->execute();

    print h2("History");
    print("<table width=85% border=1>");

    while ( my @sql_returned = $sth->fetchrow_array ) {
        print(
            "<TR><TD>$sql_returned[0]</TD><TD>$sql_returned[1]</TD><TD>$sql_returned[2]</TD></TR>"
        );
    }

    print("</table>");

    $dbh->disconnect();
}

# ---------------------------------------------
# view_history.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script allows you to view the Shiai on the system
#
# How does it work?
# =================
#
#
# History:
# ========
# 20 January 2004, Lance Wicks - File created
