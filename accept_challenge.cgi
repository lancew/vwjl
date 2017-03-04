#!/usr/bin/perl -w
use strict;
use warnings;

use CGI;

$CGI::DISABLE_UPLOADS = 1;         # Disable uploads
$CGI::POST_MAX        = 51_200;    # Maximum number of bytes per post

use lib './MyLib';
use DBI;

my $query = CGI->new();

print header();
print start_html("e-Judo Test Area");
print h1("Accept CHALLENGES");

print h3("under development");

print end_html;

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
