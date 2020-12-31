package waza;

use Moo;
use strict;
use warnings;

my %waza = (
    'nage_waza' => {
        'te_waza' => {
            'seoi_nage'         => { name => 'Seoi-nage', },
            'ippon_seoi_nage'   => { name => 'Ippon-seoi-nage', },
            'seoi_otoshi'       => { name => 'Seoi-otoshi', },
            'tai_otoshi'        => { name => 'Tai-otoshi', },
            'kata_guruma'       => { name => 'Kata-guruma', },
            'sukui_nage'        => { name => 'Sukui-nage', },
            'obi_otoshi'        => { name => 'Obi-otoshi', },
            'uki_otoshi'        => { name => 'Uki-otoshi', },
            'sumi_otoshi'       => { name => 'Sumi-otoshi', },
            'yama_arashi'       => { name => 'Yama-arashi', },
            'obi_tori_gaeshi'   => { name => 'Obi-tori-gaeshi', },
            'morote_gari'       => { name => 'Morote-gari', },
            'kuchiki_taoshi'    => { name => 'Kuchiki-taoshi', },
            'kibisu_gaeshi'     => { name => 'Kibisu-gaeshi', },
            'uchi_mata_sukashi' => { name => 'Uchi-mata-sukashi', },
            'ko_uchi_gaeshi'    => { name => 'Ko-uchi-gaeshi', },
        },
        'koshi_waza' => {
            'uki_goshi'            => { name => "Uki-goshi", },
            'o_goshi'              => { name => "O-goshi", },
            'koshi_guruma'         => { name => "Koshi-guruma", },
            'tsurikomi_goshi'      => { name => "Tsurikomi-goshi", },
            'sode_tsurikomi_goshi' => { name => "Sode-tsurikomi-goshi", },
            'harai_goshi'          => { name => "Harai-goshi", },
            'tsuri_goshi'          => { name => "Tsuri-goshi", },
            'hane_goshi'           => { name => "Hane-goshi", },
            'utsuri_goshi'         => { name => "Utsuri-goshi", },
            'ushiro_goshi'         => { name => "Ushiro-goshi", },
        },
        'ashi_waza' => {
            'de_ashi_harai'        => { name => 'De-ashi-harai', },
            'hiza_guruma'          => { name => 'Hiza-guruma', },
            'sasae_tsurikomi_ashi' => { name => 'Sasae-tsurikomi-ashi', },
            'o_soto_gari'          => { name => 'O-soto-gari', },
            'o_uchi_gari'          => { name => 'O-uchi-gari', },
            'ko_soto_gari'         => { name => 'Ko-soto-gari', },
            'ko_uchi_gari'         => { name => 'Ko-uchi-gari', },
            'okuri_ashi_harai'     => { name => 'Okuri-ashi-harai', },
            'uchi_mata'            => { name => 'Uchi-mata', },
            'ko_soto_gake'         => { name => 'Ko-soto-gake', },
            'ashi_guruma'          => { name => 'Ashi-guruma', },
            'harai_tsurikomi_ashi' => { name => 'Harai-tsurikomi-ashi', },
            'o_guruma'             => { name => 'O-guruma', },
            'o_soto_guruma'        => { name => 'O-soto-guruma', },
            'o_soto_otoshi'        => { name => 'O-soto-otoshi', },
            'tsubame_gaeshi'       => { name => 'Tsubame-gaeshi', },
            'o_soto_gaeshi'        => { name => 'O-soto-gaeshi', },
            'o_uchi_gaeshi'        => { name => 'O-uchi-gaeshi', },
            'hane_goshi_gaeshi'    => { name => 'Hane-goshi-gaeshi', },
            'harai_goshi_gaeshi'   => { name => 'Harai-goshi-gaeshi', },
            'uchi_mata_gaeshi'     => { name => 'Uchi-mata-gaeshi', },
        },
        'ma_sutemi_waza' => {
            'tomoe_nage'      => { name => 'Tomoe-nage', },
            'sumi_gaeshi'     => { name => 'Sumi-gaeshi', },
            'hikikomi_gaeshi' => { name => 'Hikikomi-gaeshi', },
            'tawara_gaeshi'   => { name => 'Tawara-gaeshi', },
            'ura_nage'        => { name => 'Ura-nage', },
        },
        'yoko_sutemi_waza' => {
            'yoko_otoshi'        => { name => 'Yoko-otoshi', },
            'tani_otoshi'        => { name => 'Tani-otoshi', },
            'hane_makikomi'      => { name => 'Hane-makikomi', },
            'soto_makikomi'      => { name => 'Soto-makikomi', },
            'uchi_makikomi'      => { name => 'Uchi-makikomi', },
            'uki_waza'           => { name => 'Uki-waza', },
            'yoko_wakare'        => { name => 'Yoko-wakare', },
            'yoko_guruma'        => { name => 'Yoko-guruma', },
            'yoko_gake'          => { name => 'Yoko-gake', },
            'daki_wakare'        => { name => 'Daki-wakare', },
            'o_soto_makikomi'    => { name => 'O-soto-makikomi', },
            'uchi_mata_makikomi' => { name => 'Uchi-mata-makikomi', },
            'harai_makikomi'     => { name => 'Harai-makikomi', },
            'ko_uchi_makikomi'   => { name => 'Ko-uchi-makikomi', },
            'kani_basami'        => { name => 'Kani-basami', },
            'kawazu_gake'        => { name => 'Kawazu-gake', },
        },
    },
    'katame_waza' => {
        'osaekomi_waza' => {
            'kesa_gatame'              => { name => 'Kesa-gatame', },
            'kuzure_kesa_gatame'       => { name => 'Kuzure-kesa-gatame', },
            'ushiro_kesa_gatame'       => { name => 'Ushiro-kesa-gatame', },
            'kata_gatame'              => { name => 'Kata-gatame', },
            'kami_shiho_gatame'        => { name => 'Kami-shiho-gatame', },
            'kuzure_kami_shiho_gatame' =>
                { name => 'Kuzure-kami-shiho-gatame', },
            'yoko_shiho_gatame' => { name => 'Yoko-shiho-gatame', },
            'tate_shiho_gatame' => { name => 'Tate-shiho-gatame', },
            'uki_gatame'        => { name => 'Uki-gatame', },
            'ura_gatame'        => { name => 'Ura-gatame', },
        },
        'shime_waza' => {
            'nami_juji_jime' => {
                name => 'Nami-juji-jime',

            },
            'gyaku_juji_jime'  => { name => 'Gyaku-juji-jime', },
            'kata_juji_jime'   => { name => 'Kata-juji-jime', },
            'hadaka_jime'      => { name => 'Hadaka-jime', },
            'okuri_eri_jime'   => { name => 'Okuri-eri-jime', },
            'kataha_jime'      => { name => 'Kataha-jime', },
            'katate_jime'      => { name => 'Katate-jime', },
            'ryote_jime'       => { name => 'Ryote-jime', },
            'sode_guruma_jime' => { name => 'Sode-guruma-jime', },
            'tsukkomi_jime'    => { name => 'Tsukkomi-jime', },
            'sankaku_jime'     => { name => 'Sankaku-jime', },
            'do_jime'          => { name => 'Do-jime', },
        },
        'kansetsu_waza' => {
            'ude_garami'              => { name => 'Ude-garami', },
            'ude_hishigi_juji_gatame' =>
                { name => 'Ude-hishigi-juji-gatame', },
            'ude_hishigi_ude_gatame' => { name => 'Ude-hishigi-ude-gatame', },
            'ude_hishigi_hiza_gatame' =>
                { name => 'Ude-hishigi-hiza-gatame', },
            'ude_hishigi_waki_gatame' =>
                { name => 'Ude-hishigi-waki-gatame', },
            'ude_hishigi_hara_gatame' =>
                { name => 'Ude-hishigi-hara-gatame', },
            'ude_hishigi_ashi_gatame' =>
                { name => 'Ude-hishigi-hara-gatame', },
            'ude_hishigi_te_gatame' => { name => 'Ude-hishigi-te-gatame', },
            'ude_hishigi_sankaku_gatame' =>
                { name => 'Ude-hishigi-sankaku-gatame', },
            'ashi_garami' => { name => 'Ashi-garami', },
        },
    },
);

sub all {
    return \%waza;
}

sub all_names {
    my $self = shift;
    my @names;

    my @tachi_waza  = $self->tachi_waza_names;
    my @katame_waza = $self->katame_waza_names;

    push @names, @tachi_waza;
    push @names, @katame_waza;

    @names = sort @names;

    return \@names;
}

sub tachi_waza_names {
    my @names;

    my @te_waza          = keys %{ $waza{nage_waza}{te_waza} };
    my @koshi_waza       = keys %{ $waza{nage_waza}{koshi_waza} };
    my @ashi_waza        = keys %{ $waza{nage_waza}{ashi_waza} };
    my @ma_sutemi_waza   = keys %{ $waza{nage_waza}{ma_sutemi_waza} };
    my @yoko_sutemi_waza = keys %{ $waza{nage_waza}{yoko_sutemi_waza} };

    for my $w ( @te_waza, @koshi_waza, @ashi_waza, @ma_sutemi_waza,
        @yoko_sutemi_waza )
    {
        $w =~ s/_/-/g;

        push @names, ucfirst($w);
    }

    return @names;
}

sub katame_waza_names {
    my @names;

    my @osaekomi_waza = keys %{ $waza{katame_waza}{osaekomi_waza} };
    my @shime_waza    = keys %{ $waza{katame_waza}{shime_waza} };
    my @kansetsu_waza = keys %{ $waza{katame_waza}{kansetsu_waza} };

    for my $w ( @osaekomi_waza, @shime_waza, @kansetsu_waza, ) {
        $w =~ s/_/-/g;

        push @names, ucfirst($w);
    }

    return @names;
}
1;
