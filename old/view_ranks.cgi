#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;

print header();
print start_html("e-Judo View Ranks");
print h1("VIEW Ranks");

show_ranks();

sub show_ranks {
    my $judoka_table = "data/judoka_csv";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka_db', 'CSV', $judoka_table, 'ad_catalog' );

    my $judoka_list = $dbh->selectall_arrayref(
        'SELECT * FROM judoka_db',
        {Slice=>{}}
    );

    print h2("JUDOKA - Ranked by number of Wins");
    print("<table width=85% border=1>");
    print("<TR><TD>Name</TD><TD>Wins</TD><TD>Losses</TD></TR>");

    for my $judoka ( sort { $b->{WINS} <=> $a->{WINS} } @$judoka_list ) {
        print p("<TR><TD> $judoka->{NAME} </TD><TD>$judoka->{WINS}</TD><TD>$judoka->{LOSSES}</TD></TR>");
    }
    print("</table>");

    $dbh->disconnect();
}

# ---------------------------------------------
# view_ranks.cgi   - Create by Lance Wicks
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
# 21 September 2004, Lance Wicks - File created
