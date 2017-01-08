#!/usr/bin/perl -w

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
#                                Presently the user ID from login is passed directly as a parameter, this will eventually need to be changed to cookie?

my $DEBUG = 0;    #  If this is set to 1 then we see the debug messages.

# The following 4 lines set strict PERL coding then load the CGI DBI and DBD::Anydata modules.
# ---------------------------------------------------------------------------------------------
use strict;               # force strict programming controls
use CGI qw(:standard);    # use the CGI.PM module
use lib './MyLib'
    ; # use the modules in MyLib, this is the DBD::Anydata used for database activities
use DBI
    ; # This calls the DBI module, which along with the line above allows us to do database activities

# Sub routines
# --------------

# end of subroutines
# -------------------

sub print_menu {
    print p("start of print_menu")
        if
        $DEBUG;   # debug option indicates on screen that this sub has started
    my $id = param("id");
    print p(" <a href=create_judoka.cgi?id=$id>Create a Judoka</a>");
    print p(" <a href=view_judoka.cgi?id=$id>View a Judoka</a>");
    print hr;
#                print p(" <a href=create_shiai.cgi?id=$id>Create a Shiai</a>");
    print p(" <a href=view_shiai.cgi?id=$id>View Shiai</a>");
    print hr;
    print p(" <a href=simulate.cgi>Simulate matches</a>");
    print p(" <a href=view_history.cgi?shiai_id=lw1>View History</a>");
    print p(" <a href=view_ranks.cgi>View Ranks</a>");
    print p("end of print_menu")
        if $DEBUG;    # debug option, shows the end of this sub
}

# main code block
# ---------------

print header(), start_html("e-Judo Test Area"),
    h1("Main Menu");    # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p( "parameters: ", param() ) if $DEBUG;
#   print p("no parameters so print the form") if !(param());
if ( param() )
{ # If there is a parameter(or parameters) then validate, else show the login screen.
        # the following lines are excecuted if paramaters HAVE been entered
    print p( "user: ", param("id") ) if $DEBUG;
    print_menu();

}
else
{   # if there are no parameters (the form has not yet been filled in then....
    print p("Error, you do not seem to have logged in okay");
    print p("<a href=e-judo.cgi>CLick here to continue</a>");
}
print end_html;    # this closes the web page properly
print p("End of main block") if $DEBUG;

