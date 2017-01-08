#!/usr/bin/perl -w

# ---------------------------------------------
# Accept_Challenges.cgi   - Create by Lance Wicks
#                       e-judo.sourceforge.net
# This is free open source software! Released under GPL
#
# Description:
# This script allows you to make and accept challenges in Shiai
#
# How does it work?
# =================
# Steps/Stages
# ------------
#
#
# History:
# ========
# 19 May 2004, Lance Wicks - File created
# 26 July 2004, Lance Wicks - Restarted work on this script.


    my $DEBUG = 1; #  If this is set to 1 then we see the debug messages.

# Scripts header    -   Standard settings for all scripts
# ---------------------------------------------------------------
    my $DEBUG = 1;                                  #  If this is set to 1 then we see the debug messages.
    my $max_post = 51_200;			    #  To have messages appear use the following example in the code: print p("message in debug only") if $DEBUG;
    use strict; # force strict programming controls
    use CGI; # use the CGI.PM module

    $CGI::DISABLE_UPLOADS = 1;                          # Disable uploads
    $CGI::POST_MAX        = $max_post;                  # Maximum number of bytes per post


    use lib './MyLib';                                  # use the modules in MyLib, this is the DBD::Anydata used for database activities
    use DBI;                                            # This calls the DBI module, which along with the line above allows us to do database activities


    my $query = CGI->new();          # Start a new cgi object
# Sub routines
# --------------

# ------------------
# End of Subroutines


# Main Code Block
# ----------------

print header(), start_html("e-Judo Test Area"), h1("Accept CHALLENGES"); # This line uses CGI.PM to to create the webpage
print p("Start main block") if $DEBUG;
print p("parameters: ", param()) if $DEBUG;
print p("values: ", param("id")) if $DEBUG;









print h3("under development");


print p("END main block") if $DEBUG;
print end_html; # this closes the web page properly
# --------------------
# End of Main Block

