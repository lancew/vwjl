#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;

print header();
print start_html("e-Judo Test Area");
print h1("Main Menu");

if ( param() ) { 
    # If there is a parameter(or parameters) then validate,
    # else show the login screen.
    # the following lines are excecuted if paramaters HAVE been entered
    
    print_menu();
}
else {   
    # if there are no parameters (the form has not
    # yet been filled in then....
    print p("Error, you do not seem to have logged in okay");
    print p("<a href=e-judo.cgi>CLick here to continue</a>");
}

print end_html;    # this closes the web page properly

sub print_menu {
    my $id = param("id");
    print p(" <a href=create_judoka.cgi?id=$id>Create a Judoka</a>");
    print p(" <a href=view_judoka.cgi?id=$id>View a Judoka</a>");
    print hr;
    # Hide create option for now
    #print p(" <a href=create_shiai.cgi?id=$id>Create a Shiai</a>");
    print p(" <a href=view_shiai.cgi?id=$id>View Shiai</a>");
    print hr;
    print p(" <a href=simulate.cgi>Simulate matches</a>");
    print p(" <a href=view_history.cgi?shiai_id=lw1>View History</a>");
    print p(" <a href=view_ranks.cgi>View Ranks</a>");
}

# ---------------------------------------------
# main_menu.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script prints the main menu
#
# History:
# =========
# 03 January 2004, Lance Wicks - Created this file, which is linked to from e-judo.cgi if you login correctly.
