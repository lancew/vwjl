#!/usr/bin/perl -w
use strict;
use warnings;

use CGI qw(:standard);
use lib './MyLib';
use DBI;
use VWJL;

print header();
print start_html("e-Judo Test Area");
print h1("e-Judo test area");

if ( param() ) {
    my $name     = param("ID");
    my $password = param("ejudopass");

    if ( $name eq "" or $password eq "" ) {
        print "Come on, enter some data!!";
        exit;
    }

    my $user = VWJL::get_user($name);
    my $pass = $user->{PASSWORD};
    
    if ($pass) {
        if ( $pass eq $password ) {
            print p("OK");
            print(
                "<a href='main_menu.cgi?id=$name'>Click here to continue</a>"
            );
        }
        else {
            print('Invalid Credentials');
        }
    }
    else {
        print p('Invalid Credentials');
    }
}
else {
    unless ( -e "./data/judoka_csv" ) {
        create_judoka_file();
    }

    unless ( -e "./data/users_csv" ) {
        create_users_file();
    }

    unless ( -e "./data/shiai_csv" ) {
       create_shiai_file();
    }

    print hr;
    print start_form;
    print p( "What is your user ID: ", textfield("ID") );
    print p( "Your Password: ",        password_field("ejudopass") );
    print submit( -name => 'submit button' );
    print end_form;
    print hr;
    print(
        'else click <a href="create_user.cgi">HERE</a> to create a new user');
}

print end_html;

# ----------------------------

sub create_judoka_file {
    # This sub creates the data/judoka_csv file

    # create the scalers we need to use in the sql
    # ----------------------------------------------
    my $judoka_table = "./data/judoka_csv";
    # Okay now we must create the database files
    # here is the DBI/SQL code
    # ----------------------------------------------------

# First create the array and hash to hold the table fields and data definitions
# ------------------------------------------------------------------------------
    my @judoka_fields
        = qw/ user_id judoka_id name start_date dojo country date_of_birth weight active sensei wins losses bio password strength fitness speed ki injury_level injury_desc total_shiai earnings cash grade retired activity_points experience_points strategy_1 strategy_2 strategy_3 strategy_4 strategy_5 strategy_6 strategy_7 strategy_8 strategy_9 strategy_10 strategy_11 strategy_12 strategy_13 strategy_14 strategy_15 jami_juji_jime gyaku_juji_jime kata_juji_jime hadaka_jime okuri_eri_jime kata_ha_jime katate_jime ryote_jime sode_guruma_jime tsukkomi_jime sankaku_jime ude_garami ude_hishigi_juji_gatame ude_hishigi_ude_gatame ude_hishigi_hiza_gatame ude_hishigi_waki_gatame ude_hishigi_hara_gatame ude_hishigi_ashi_gatame ude_hishigi_te_gatame ude_hishigi_sankaku_gatame hon_kesa_gatame kuzure_kesa_gatame kata_gatame kami_shiho_gatame kuzure_kami_shiho_gatame yoko_shiho_gatame tate_shiho_gatame de_ashi_harai hiza_guruma sasae_tsurikomi_ashi uki_goshi osoto_gari o_goshi ouchi_gari seoi_nage kosoto_gari kouchi_gari koshi_guruma tsurikomi_goshi okuri_ashi_harai tai_otoshi harai_goshi uchi_mata kosoto_gake tsuri_goshi yoko_otoshi ashi_guruma hane_goshi harai_tsurikomi_ashi tomoe_nage kata_guruma sumi_gaeshi tani_otoshi hane_makikomi sukui_nage utsuri_goshi o_guruma soto_makikomi uki_otoshi osoto_guruma uki_waza yoko_wakare yoko_guruma ushiro_goshi ura_nage sumi_otoshi yoko_gake morote_gari kuchiki_taoshi kibisu_gaeshi uchi_mata_sukashi tsubame_gaeshi osoto_gaeshi ouchi_gaeshi kouchi_gaeshi hane_goshi_gaeshi harai_goshi_gaeshi uchi_mata_gaeshi osoto_makikomi uchi_mata_makikomi harai_makikomi /;
    my %judoka_field_def = (
        user_id                    => 'char(20)',
        judoka_id                  => 'char(20)',
        name                       => 'char(20)',
        start_date                 => 'char(20)',
        dojo                       => 'char(20)',
        country                    => 'char(20)',
        date_of_birth              => 'char(20)',
        weight                     => 'char(20)',
        active                     => 'char(20)',
        sensei                     => 'char(20)',
        wins                       => 'char(20)',
        losses                     => 'char(20)',
        bio                        => 'char(20)',
        password                   => 'char(20)',
        strength                   => 'char(20)',
        fitness                    => 'char(20)',
        speed                      => 'char(20)',
        ki                         => 'char(20)',
        injury_level               => 'char(20)',
        injury_desc                => 'char(20)',
        total_shiai                => 'char(20)',
        earnings                   => 'char(20)',
        cash                       => 'char(20)',
        grade                      => 'char(20)',
        retired                    => 'char(20)',
        activity_points            => 'char(20)',
        experience_points          => 'char(20)',
        strategy_1                 => 'char(20)',
        strategy_2                 => 'char(20)',
        strategy_3                 => 'char(20)',
        strategy_4                 => 'char(20)',
        strategy_5                 => 'char(20)',
        strategy_6                 => 'char(20)',
        strategy_7                 => 'char(20)',
        strategy_8                 => 'char(20)',
        strategy_9                 => 'char(20)',
        strategy_10                => 'char(20)',
        strategy_11                => 'char(20)',
        strategy_12                => 'char(20)',
        strategy_13                => 'char(20)',
        strategy_14                => 'char(20)',
        strategy_15                => 'char(20)',
        jami_juji_jime             => 'char(20)',
        gyaku_juji_jime            => 'char(20)',
        kata_juji_jime             => 'char(20)',
        hadaka_jime                => 'char(20)',
        okuri_eri_jime             => 'char(20)',
        kata_ha_jime               => 'char(20)',
        katate_jime                => 'char(20)',
        ryote_jime                 => 'char(20)',
        sode_guruma_jime           => 'char(20)',
        tsukkomi_jime              => 'char(20)',
        sankaku_jime               => 'char(20)',
        ude_garami                 => 'char(20)',
        ude_hishigi_juji_gatame    => 'char(20)',
        ude_hishigi_ude_gatame     => 'char(20)',
        ude_hishigi_hiza_gatame    => 'char(20)',
        ude_hishigi_waki_gatame    => 'char(20)',
        ude_hishigi_hara_gatame    => 'char(20)',
        ude_hishigi_ashi_gatame    => 'char(20)',
        ude_hishigi_te_gatame      => 'char(20)',
        ude_hishigi_sankaku_gatame => 'char(20)',
        hon_kesa_gatame            => 'char(20)',
        kuzure_kesa_gatame         => 'char(20)',
        kata_gatame                => 'char(20)',
        kami_shiho_gatame          => 'char(20)',
        kuzure_kami_shiho_gatame   => 'char(20)',
        yoko_shiho_gatame          => 'char(20)',
        tate_shiho_gatame          => 'char(20)',
        de_ashi_harai              => 'char(20)',
        hiza_guruma                => 'char(20)',
        sasae_tsurikomi_ashi       => 'char(20)',
        uki_goshi                  => 'char(20)',
        osoto_gari                 => 'char(20)',
        o_goshi                    => 'char(20)',
        ouchi_gari                 => 'char(20)',
        seoi_nage                  => 'char(20)',
        kosoto_gari                => 'char(20)',
        kouchi_gari                => 'char(20)',
        koshi_guruma               => 'char(20)',
        tsurikomi_goshi            => 'char(20)',
        okuri_ashi_harai           => 'char(20)',
        tai_otoshi                 => 'char(20)',
        harai_goshi                => 'char(20)',
        uchi_mata                  => 'char(20)',
        kosoto_gake                => 'char(20)',
        tsuri_goshi                => 'char(20)',
        yoko_otoshi                => 'char(20)',
        ashi_guruma                => 'char(20)',
        hane_goshi                 => 'char(20)',
        harai_tsurikomi_ashi       => 'char(20)',
        tomoe_nage                 => 'char(20)',
        kata_guruma                => 'char(20)',
        sumi_gaeshi                => 'char(20)',
        tani_otoshi                => 'char(20)',
        hane_makikomi              => 'char(20)',
        sukui_nage                 => 'char(20)',
        utsuri_goshi               => 'char(20)',
        o_guruma                   => 'char(20)',
        soto_makikomi              => 'char(20)',
        uki_otoshi                 => 'char(20)',
        osoto_guruma               => 'char(20)',
        uki_waza                   => 'char(20)',
        yoko_wakare                => 'char(20)',
        yoko_guruma                => 'char(20)',
        ushiro_goshi               => 'char(20)',
        ura_nage                   => 'char(20)',
        sumi_otoshi                => 'char(20)',
        yoko_gake                  => 'char(20)',
        morote_gari                => 'char(20)',
        kuchiki_taoshi             => 'char(20)',
        kibisu_gaeshi              => 'char(20)',
        uchi_mata_sukashi          => 'char(20)',
        tsubame_gaeshi             => 'char(20)',
        osoto_gaeshi               => 'char(20)',
        ouchi_gaeshi               => 'char(20)',
        kouchi_gaeshi              => 'char(20)',
        hane_goshi_gaeshi          => 'char(20)',
        harai_goshi_gaeshi         => 'char(20)',
        uchi_mata_gaeshi           => 'char(20)',
        osoto_makikomi             => 'char(20)',
        uchi_mata_makikomi         => 'char(20)',
        harai_makikomi             => 'char(20)'
    );

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        or die "Can not create database connection";

    # build the JUDOKA table using SQL
    # ---------------------------------
    $dbh->do(
        "CREATE TABLE judoka ("
            . join( ',',
            map { $_ . ' ' . $judoka_field_def{$_} } @judoka_fields )
            . ")"
    ) or die "Can not create table";

    $dbh->func( 'judoka', 'CSV', $judoka_table, 'ad_export' );
}

sub create_users_file {
    my $users_table = "./data/users_csv";
    my @users_fields
        = qw/ id first_name surname date_of_birth email password active last_login create_date earnings cash judoka_limit sensei_limit dojo_limit team_limit rank /;
    my %users_field_def = (
        user_id       => 'char(20)',
        id            => 'char(20)',
        first_name    => 'char(20)',
        surname       => 'char(20)',
        date_of_birth => 'char(20)',
        email         => 'char(20)',
        password      => 'char(20)',
        active        => 'char(20)',
        last_login    => 'char(20)',
        create_date   => 'char(20)',
        earnings      => 'char(20)',
        cash          => 'char(20)',
        judoka_limit  => 'char(20)',
        sensei_limit  => 'char(20)',
        dojo_limit    => 'char(20)',
        team_limit    => 'char(20)',
        rank          => 'char(20)'
    );

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        or die "Can not create database connection";

    # build the USERS table using SQL
    # ---------------------------------
    $dbh->do(
        "CREATE TABLE users ("
            . join(
            ',', map { $_ . ' ' . $users_field_def{$_} } @users_fields
            )
            . ")"
    ) or die "Can not create table";
}

sub create_shiai_file {
    my $shiai_table = "./data/shiai_csv";
    # Okay now we must create the database files
    # here is the DBI/SQL code
    # ----------------------------------------------------

# First create the array and hash to hold the table fields and data definitions
# ------------------------------------------------------------------------------
    my @shiai_fields
        = qw/ owner_id shiai_id name closedate type eventdate admins_name active earnings cash entry_fee createdate first_prize second_prize third_prize fourth_prize fith_prize description /;
    my %shiai_field_def = (
        owner_id     => 'char(20)',
        shiai_id     => 'char(20)',
        name         => 'char(20)',
        closedate    => 'char(20)',
        type         => 'char(20)',
        eventdate    => 'char(20)',
        admins_name  => 'char(20)',
        active       => 'char(20)',
        earnings     => 'char(20)',
        cash         => 'char(20)',
        entry_fee    => 'char(20)',
        createdate   => 'char(20)',
        first_prize  => 'char(20)',
        second_prize => 'char(20)',
        third_prize  => 'char(20)',
        fourth_prize => 'char(20)',
        fith_prize   => 'char(20)',
        description  => 'char(20)'
    );

    my $dbh = DBI->connect('dbi:AnyData(RaiseError=>1):')
        or die "Can not create database connection";

    # build the shiai table using SQL
    # ---------------------------------
    $dbh->do(
        "CREATE TABLE shiai ("
            . join(
            ',', map { $_ . ' ' . $shiai_field_def{$_} } @shiai_fields
            )
            . ")"
    ) or die "Can not create table";

    $dbh->func( 'shiai', 'CSV', $shiai_table, 'ad_export' );
}

# ---------------------------------------------
# e-judo.cgi   - Create by Lance Wicks
# This is free open source software! Released under GPL
#
# Description:
# This script is the initial login screen for the new e-Judo code.
# this screen allows you to login, or link to script to create a new user
# this script will validate a user from the users_csv data file.
#
# History:
# ========
# 20 December 2003, Lance Wicks - Created initial file.
# 02 January 2004, Lance Wicks - Create USer complete, so start on Create user, first create a main menu script.
# 16 March 2004, Lance Wicks - Added code to create the JUDOKA_CSV file if it does not exist. (Also my brithday if you are bored enough to care!)
# 16 March 2004, Lance Wicks - Added code to create the users file if it does not exist already.
# 01 March 2017, Lance Wicks - Restarting the project.
