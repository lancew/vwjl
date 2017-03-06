#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;
use VWJL;

print header();
print start_html("e-Judo Test Area");
print h1("VIEW JUDOKA");

if ( param("id") ) {
    if ( my $judoka_id = param("judoka") ) {
        my $judoka = VWJL::get_judoka( $judoka_id );

        print p(
            " <a href=entershiai.cgi?judoka_id=$judoka_id&judoka_name=$judoka->{NAME}>Enter a shiai</a>"
        );
        print p(
            " <a href=make_challenge.cgi?judoka_id=$judoka_id&judoka_name=$judoka->{NAME}>Make a challenge</a>"
        );

        display_judoka_data($judoka);
    }
    else {
        list_users_judoka( param("id") );
    }
}
else {
    print p("Problem!");
    print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
}


sub display_judoka_data {
    my $judoka = shift;
    print h1( "Judoka: ", $judoka->{NAME} );
    print h2('| Wins: ', $judoka->{WINS}, ' | Losses: ', $judoka->{LOSSES}, ' |');

    print("<table width=85% border=1>");
    for ( sort keys %$judoka  ) {
        print("<TR><TD>$_</TD><TD>$judoka->{$_}</TD>");
        print("</TR>");
    }
    print("</table>");
}

sub list_users_judoka {
    my @passed_info = @_;
    my $user_id     = $passed_info[0];

    my @judoka_found;

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' );

    my $sql    = "SELECT judoka_id,name FROM judoka WHERE user_id = ?";
    my @params = ($user_id);

    my $sth = $dbh->prepare($sql);
    $sth->execute(@params);

    print h2("JUDOKA LIST");
    while ( my @sql_returned = $sth->fetchrow_array ) {
        my $judoka_id   = $sql_returned[0];
        my $judoka_name = $sql_returned[1];
        print p(
            "<a href=view_judoka.cgi?id=$user_id&judoka=$judoka_id&name=$judoka_name>$judoka_name</a>"
        );
    }

    $dbh->disconnect();
}

# ---------------------------------------------
# view_judoka.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script allows you to view your Judoka(s) and their statistics
#
# How does it work?
# =================
# Basically it uses your userID, accesses the Judoka database finds all your Judoka and lets you choose which one you want to look at
# Then it takes which ever one you clicked on and displays it
#
# History:
# ========
# 07 January 2004, Lance Wicks - File created
