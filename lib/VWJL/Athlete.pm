package VWJL::Athlete;

use utf8;
use Moo;
use VWJL::Infrastructure;
use VWJL::Waza;
use waza;

has [
    qw/
        biography
        country
        dojo
        name
        sensei
        username
        /
] => (
    is      => 'rw',
    default => '',
);

has [
    qw/
        left_arm_fatigue
        left_arm_injury
        left_arm_strength
        left_leg_fatigue
        left_leg_injury
        left_leg_strength
        physical_fatigue
        physical_fitness
        physical_form
        right_arm_fatigue
        right_arm_injury
        right_arm_strength
        right_leg_fatigue
        right_leg_injury
        right_leg_strength
        /
] => (
    is      => 'rw',
    default => 1,
);

has [
    qw/
        seoi_nage
        ippon_seoi_nage
        seoi_otoshi
        tai_otoshi
        kata_guruma
        sukui_nage
        obi_otoshi
        uki_otoshi
        sumi_otoshi
        yama_arashi
        obi_tori_gaeshi
        morote_gari
        kuchiki_taoshi
        kibisu_gaeshi
        uchi_mata_sukashi
        ko_uchi_gaeshi
        uki_goshi
        o_goshi
        koshi_guruma
        tsurikomi_goshi
        sode_tsurikomi_goshi
        harai_goshi
        tsuri_goshi
        hane_goshi
        utsuri_goshi
        ushiro_goshi
        de_ashi_harai
        hiza_guruma
        sasae_tsurikomi_ashi
        o_soto_gari
        o_uchi_gari
        ko_soto_gari
        ko_uchi_gari
        okuri_ashi_harai
        uchi_mata
        ko_soto_gake
        ashi_guruma
        harai_tsurikomi_ashi
        o_guruma
        o_soto_guruma
        o_soto_otoshi
        tsubame_gaeshi
        o_soto_gaeshi
        o_uchi_gaeshi
        hane_goshi_gaeshi
        harai_goshi_gaeshi
        uchi_mata_gaeshi
        tomoe_nage
        sumi_gaeshi
        hikikomi_gaeshi
        tawara_gaeshi
        ura_nage
        yoko_otoshi
        tani_otoshi
        hane_makikomi
        soto_makikomi
        uchi_makikomi
        uki_waza
        yoko_wakare
        yoko_guruma
        yoko_gake
        daki_wakare
        o_soto_makikomi
        uchi_mata_makikomi
        harai_makikomi
        ko_uchi_makikomi
        kani_basami
        kawazu_gake
        kesa_gatame
        kuzure_kesa_gatame
        ushiro_kesa_gatame
        kata_gatame
        kami_shiho_gatame
        kuzure_kami_shiho_gatame
        yoko_shiho_gatame
        tate_shiho_gatame
        uki_gatame
        ura_gatame
        gyaku_juji_jime
        kata_juji_jime
        hadaka_jime
        okuri_eri_jime
        kataha_jime
        katate_jime
        ryote_jime
        sode_guruma_jime
        tsukkomi_jime
        sankaku_jime
        do_jime
        ude_garami
        ude_hishigi_juji_gatame
        ude_hishigi_ude_gatame
        ude_hishigi_hiza_gatame
        ude_hishigi_waki_gatame
        ude_hishigi_hara_gatame
        ude_hishigi_ashi_gatame
        ude_hishigi_te_gatame
        ude_hishigi_sankaku_gatam
        ashi_garami
        /
] => ( is => 'lazy', builder => sub { VWJL::Waza->new }, );

has [qw/wins losses/] => (
    is      => 'rw',
    default => 0,
);

sub win_percentage {
    my $self = shift;

    return
        int(
        100 * ( $self->wins / ( ( $self->losses + $self->wins ) || 1 ) ) );
}

has 'inf' => (
    is      => 'lazy',
    builder => sub {
        VWJL::Infrastructure->new;
    },
);

sub get {
    my ( $self, %args ) = @_;

    my $athlete = $self->inf->get_athlete_data( user => $args{'user'} );

    if ( $athlete->{wins} && $athlete->{losses} ) {
        $athlete->{win_percentage} = int(
            100 * (
                $athlete->{wins} / ( $athlete->{wins} + $athlete->{losses} )
            )
        );
    }

    return $athlete;
}

sub uchi_komi {
    my ( $self, %args ) = @_;

    my $athlete = $self->inf->get_athlete_data( user => $args{'user'} );

    $self->inf->update_athlete_waza(
        athlete_id    => $athlete->{'id'},
        waza          => $args{'waza'},
        attack_delta  => 1,
        defence_delta => 0,
    );

    $self->inf->update_athlete(
        user  => $args{'user'},
        field => 'physical_fatigue',
        value => $athlete->{'physical_fatigue'} + 1,
    );

    return 1;
}

1;

