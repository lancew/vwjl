#!/usr/bin/perl -wT
use strict;
use warnings;

use CGI;     
$CGI::DISABLE_UPLOADS = 1;            # Disable uploads
$CGI::POST_MAX        = 51_200;       # Maximum number of bytes per post

my $DEBUG    = 0;       #  If this is set to 1 then we see the debug messages.

use lib './MyLib';
use DBI;

my $query = CGI->new();    # Start a new cgi object

my $judoka_id;
my $judoka_name;
my $shiai_id;

print $query->header();
print $query->start_html( -title => 'Make Challenge' ),
print $query->h1("E-Judo Test Area - Make Challenge");

if ( $query->param ) {
    $judoka_id   = $query->url_param('judoka_id');
    $judoka_name = $query->url_param('judoka_name');

    # Setting this manually for now, needs to be a loop 
    # to access all Shiai at a later date.

    #TODO: Hardcoded teh shiai ID, should be param
    $shiai_id    = "lancewlw1";
      
    if ( $query->param("challenge") ) {
        enter_in_database($query);
        enter_chal_in_history();
        email_confirmation();
    }
    else {
        identify_judoka();
        my @temp = identify_shiai($shiai_id);
        my @returned_judoka_list = identify_other_judoka( $temp[0] );
        my @available_judoka
            = identify_available_judoka(@returned_judoka_list);
        display_list($query, @available_judoka);
    }
}
else
{ 
    print $query->h1("No Parameters passed so there was a problem");
     print $query->h1("CLICK YOUR BACK BUTTON");
}

print $query->end_html;

# ---------------------------------------------------
# Sub-routines
# ---------------------------------------------------

sub identify_judoka {}

sub identify_shiai {
    # In this sub we are finding what shiai this player is entered in
    #  Hmmm..... maybe we are approaching this all wrong?
    #  Does the Judoka only enter one shiai?

    my $shiai_id = shift;
    my $ladder_table
        = "data/shiai_data/"
        . $shiai_id
        . "_ldr";    # eg: data/shiai_data/userTest.ldr the ladder itself

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'ladder_db', 'CSV', $ladder_table, 'ad_catalog' );

    my $sql = "SELECT * FROM ladder_db";

    warn $ladder_table;
    warn $sql;

    my $sth = $dbh->prepare($sql);  
    $sth->execute();        

    my @sql_returned;

    my $judoka_found_flag = 0;
    while ( @sql_returned = $sth->fetchrow_array ) {
        my $found_id = $sql_returned[1];
        
        if ( $judoka_id eq $found_id ) {
            $judoka_found_flag = 1;
        }
    }

    $dbh->disconnect();
    return $shiai_id;
}

sub identify_other_judoka {
    my @passed_data = @_;

    my $the_ladder_table
        = "data/shiai_data/"
        . $passed_data[0]
        . "_ldr";    # eg: data/shiai_data/userTest.ldr the ladder itself

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'ladder_db', 'CSV', $the_ladder_table, 'ad_catalog' );

    my $sql = "SELECT * FROM ladder_db";

    my $sth = $dbh->prepare($sql);    
    $sth->execute();                  

    my @sql_returned;
    my @judoka_list;
    my @judoka_names;

    my $counter = 0;
    while ( @sql_returned = $sth->fetchrow_array ) {
        my $found_id = $sql_returned[1];
        my $found_name = $sql_returned[0];

        if ( $found_id ne $judoka_id ) {
            $judoka_list[$counter]  = $found_id;
            $judoka_names[$counter] = $found_name;
            $counter = $counter + 1;
        }
    }

    $dbh->disconnect();

    return @judoka_list, @judoka_names;
}

sub identify_available_judoka {
    # This sub is passed a list of all other Judoka in the shiai.
    # It returns a list of judoka you can challenge, based on what criteria?

    my @passed_list = @_;    # Accept the array/list of judoka passed to us.

    my $count            = @passed_list;
    my $number_of_judoka = $count / 2;

    my @available_list = @passed_list;
    return @available_list;
}

sub display_list {
    my $query = shift;
    my @incoming_list = @_;

   # take the list and work out how many entries there are.
   # The list is in fact two lists, names the IDs. So divide the total by two.
    my $item_count    = @incoming_list;
    my $judoka_number = $item_count / 2;

    my @judoka_names = @incoming_list[ $judoka_number .. $item_count ];

    my @judoka_ids = @incoming_list[ 0 .. $judoka_number - 1 ];

    my $loop = 0;
    for ( $loop = 0; $loop ne $judoka_number; $loop++ ) {
        my $this_url = $query->self_url();
        my $link_url = $this_url . "&challenge=" . $judoka_ids[$loop];
        print $query->p(
            $query->a( { -href => $link_url }, $judoka_names[$loop] ) );
    }
}

sub enter_in_database {
    my $query = shift;

    my $opponent_id = $query->param("challenge");

    # Challenge database fields = challenger opponent_id
    my $challenger = $judoka_id;

    # Accepted database field = 0 for unaccepted. 
    # 1 for accepted. (Default should be 0)
    my $accepted = "Yes";

    # TODO: hard coding shiai here.
    my $shiai_id = 'lancewlw1';
    my $challenge_table = "data/shiai_data/" . $shiai_id . "_chal";

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):');
    $dbh->func( 'challenge_db', 'CSV', $challenge_table, 'ad_catalog' );

    # add the data into a new record
    my $sql = "INSERT INTO challenge_db VALUES ( ?,?,? )";

    my @challenge_params = ( $challenger, $opponent_id, $accepted );

    my $sth = $dbh->prepare($sql);    
    $sth->execute(@challenge_params); 
    $dbh->disconnect();
    
    print $query->p("Challenge Entered");
}

sub enter_chal_in_history { }

sub email_confirmation { }

# ---------------------------------------------
# make_challenge.cgi   - Create by Lance Wicks
#
# (C) 2004, Lance Wicks. All Rights Reserved
#
# Description:
#
# History:
# ========
# 19 may 2004, Lance Wicks - Initial File created as prototype
# 21 May 2004, Lance Wicks - Started new file, shall add skeleton to help chris get started.
#
#
# Steps
# --------
#
# 1. identify the judoka
# 2. identify what shiai/competitions they are entered in
# 3. identify other judoka in the shiai
# 4. identify other judoka available to challenge
# 5. display this list
# 6. user selects a judoka to challenge
# 7. make entry in challenge table
# 8. email challenged player (?)
#
#