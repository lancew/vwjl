#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;

print header();
print start_html("e-Judo Test Area");
print h1("VIEW SHIAI");   

if ( param("id") ) { 
    if ( param("shiai") ) {
        my $shiai = param("shiai");

        my @shiai_info = read_shiai_data($shiai);
        display_shiai_data(@shiai_info);
        show_players($shiai);
    }
    else
    { 
        list_shiai( param("id") );
    }
}
else { 
    print p("Problem!");
    print p("-> <a href=e-judo.cgi>Click HERE to continue</a>");
}

sub read_shiai_data {
    my @passed_info = @_;  
    my $shiai_id = $passed_info[0];

    my @shiai_data;
    my $dbh1 = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh1->func( 'shiaidb', 'CSV', 'data/shiai_csv', 'ad_catalog' );

    my $the_query = "SELECT * FROM shiaidb WHERE shiai_id = ?";
    my $the_params = ($shiai_id);

    my $sth1 = $dbh1->prepare($the_query);  
    $sth1->execute($the_params);    

    my @query_result = $sth1->fetchrow_array;
    $dbh1->disconnect();

    return @query_result;
}

sub display_shiai_data {
    my @passed_info = @_;
    print h1( "Shiai: ", $passed_info[2] );
    my $number_of_items = @passed_info;

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' );

    my $sql_dataquery = "SELECT * FROM shiai_db";

    my $sth = $dbh->prepare($sql_dataquery);
    $sth->execute();

    my @result = $sth->fetchrow_array;

    my @headings = @{ $sth->{NAME} };
    my $number_of_headings = @headings;

    $dbh->disconnect();

    print("<table width=85% border=1>");
    for ( my $loop = 2; $loop ne $number_of_headings; $loop++ ) {
        print("<TR><TD>$headings[$loop]</TD><TD>$passed_info[$loop]</TD>");
        print("</TR>");
    }
    print("</table>");
}

sub list_shiai {
    my @passed_info = @_;
    my $user_id = $passed_info[0];

    my @shiai_found;

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'shiai_db', 'CSV', 'data/shiai_csv', 'ad_catalog' );

    my $sql = "SELECT shiai_id,name FROM shiai_db";

    my $sth = $dbh->prepare($sql);   
    $sth->execute();                 

    print h2("SHIAI LIST");
    while (my @sql_returned = $sth->fetchrow_array ) {
        my $shiai_id = $sql_returned[0];
        my $shiai_name = $sql_returned[1];
        print p(
            "<a href=view_shiai.cgi?id=$user_id&shiai=$shiai_id>$shiai_name</a>"
        );
    }

    $dbh->disconnect();
}

sub show_players {
    my @passed_info = @_;
    my $shiai_id = $passed_info[0];
    my $ladder_table
        = "data/shiai_data/"
        . $shiai_id
        . "_ldr";
        
    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog' );

    my $sql = "SELECT * FROM ladder_db";

    my $sth = $dbh->prepare($sql);
    $sth->execute();              

    print h2("Judoka Entered LIST");
    while ( my @sql_returned = $sth->fetchrow_array ) {
        my $name = $sql_returned[0];
        print br($name);
    }

    $dbh->disconnect();
}

# ---------------------------------------------
# view_shiai.cgi   - Create by Lance Wicks
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
# 10 January 2004, Lance Wicks - File created
