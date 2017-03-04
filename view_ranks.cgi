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

    my $sql = "SELECT * FROM judoka_db";

    my $sth = $dbh->prepare($sql);
    $sth->execute();            
    
    my %ranking;
    while ( my @sql_returned = $sth->fetchrow_array ) {
        $ranking{ $sql_returned[2] } = $sql_returned[10];
    }

    print h2("JUDOKA - Ranked by number of Wins");
    print("<table width=85% border=1>");
    print("<TR><TD>Name</TD><TD>Wins</TD></TR>");

    for my $key ( sort { $ranking{$b} <=> $ranking{$a} } ( keys %ranking ) ) {
        print p("<TR><TD> $key </TD><TD>$ranking{$key}</TD></TR>");
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