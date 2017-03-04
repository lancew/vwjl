#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;

print header();
print start_html("e-Judo Test Area");
print h1("VIEW JUDOKA");

if ( param("id") ) {
    if ( param("judoka") ) {
        my $judoka      = param("judoka");
        my $judoka_name = param("name");
        my @judoka_info = read_judoka_data($judoka);
        print p(
            " <a href=entershiai.cgi?judoka_id=$judoka&judoka_name=$judoka_name>Enter a shiai</a>"
        );
        print p(
            " <a href=make_challenge.cgi?judoka_id=$judoka&judoka_name=$judoka_name>Make a challenge</a>"
        );

        display_judoka_data(@judoka_info);
    }
    else {
        list_users_judoka( param("id") );
    }
}
else {
    print p("Problem!");
    print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
}

# --------------
sub read_judoka_data {
    my @passed_info = @_;
    my $judoka_id   = $passed_info[0];

    my @judoka_data;
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' );

    my $sql_query  = "SELECT * FROM judoka WHERE judoka_id = ?";
    my $sql_params = ($judoka_id);

    my $sth = $dbh->prepare($sql_query);
    $sth->execute($sql_params);

    my @result = $sth->fetchrow_array;
    $dbh->disconnect();

    return @result;
}

sub display_judoka_data {
    my @passed_info = @_;
    print h1( "Judoka: ", $passed_info[2] );
    my $number_of_items = @passed_info;

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'judoka', 'CSV', 'data/judoka_csv', 'ad_catalog' );

    my $sql_dataquery = "SELECT * FROM judoka";

    my $sth = $dbh->prepare($sql_dataquery);
    $sth->execute();

    my @result = $sth->fetchrow_array;

    my @headings           = @{ $sth->{NAME} };
    my $number_of_headings = @headings;

    $dbh->disconnect();
    print("<table width=85% border=1>");
    for ( my $loop = 2; $loop ne 123; $loop++ ) {
        print("<TR><TD>$headings[$loop]</TD><TD>$passed_info[$loop]</TD>");
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
