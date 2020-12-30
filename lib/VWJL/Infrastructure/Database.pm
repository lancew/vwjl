package VWJL::Infrastructure::Database;

sub get {
    my %args = @_;

    my %fake_data = {
        lancew => {
            name      => 'Hifumi Maruyama',
            weight    => '65.2',
            dojo      => 'Kodokan',
            country   => 'Japan',
            sensei    => 'Inoue Kosei',
            wins      => 0,
            losses    => 0,
            biography =>
                'Just a Judoka trying to make his way in the universe',
            physical => {
                left_arm => {
                    strength => 50,
                    fatigue  => 0,
                    injury   => 0,
                },
                right_arm => {
                    strength => 50,
                    fatigue  => 0,
                    injury   => 0,
                },
                left_leg => {
                    strength => 50,
                    fatigue  => 0,
                    injury   => 0,
                },
                right_leg => {
                    strength => 50,
                    fatigue  => 0,
                    injury   => 0,
                },
            },
            waza => {
                ippon_seoi_nage => {
                    attack  => 80,
                    defence => 70,
                    form    => 50,
                },
            },
        }
    };

    return $fake_data{ $args{'user'} };
}

true;

# Data fields: user_id,judoka_id,name,start_date,dojo,country,date_of_birth,weight,active,sensei,wins,losses,bio,password,strength,fitness,speed,ki,injury_level,injury_desc,total_shiai,earnings,cash,grade,retired,activity_points,experience_points,strategy_1,strategy_2,strategy_3,strategy_4,strategy_5,strategy_6,strategy_7,strategy_8,strategy_9,strategy_10,strategy_11,strategy_12,strategy_13,strategy_14,strategy_15,jami_juji_jime,gyaku_juji_jime,kata_juji_jime,hadaka_jime,okuri_eri_jime,kata_ha_jime,katate_jime,ryote_jime,sode_guruma_jime,tsukkomi_jime,sankaku_jime,ude_garami,ude_hishigi_juji_gatame,ude_hishigi_ude_gatame,ude_hishigi_hiza_gatame,ude_hishigi_waki_gatame,ude_hishigi_hara_gatame,ude_hishigi_ashi_gatame,ude_hishigi_te_gatame,ude_hishigi_sankaku_gatame,hon_kesa_gatame,kuzure_kesa_gatame,kata_gatame,kami_shiho_gatame,kuzure_kami_shiho_gatame,yoko_shiho_gatame,tate_shiho_gatame,de_ashi_harai,hiza_guruma,sasae_tsurikomi_ashi,uki_goshi,osoto_gari,o_goshi,ouchi_gari,seoi_nage,kosoto_gari,kouchi_gari,koshi_guruma,tsurikomi_goshi,okuri_ashi_harai,tai_otoshi,harai_goshi,uchi_mata,kosoto_gake,tsuri_goshi,yoko_otoshi,ashi_guruma,hane_goshi,harai_tsurikomi_ashi,tomoe_nage,kata_guruma,sumi_gaeshi,tani_otoshi,hane_makikomi,sukui_nage,utsuri_goshi,o_guruma,soto_makikomi,uki_otoshi,osoto_guruma,uki_waza,yoko_wakare,yoko_guruma,ushiro_goshi,ura_nage,sumi_otoshi,yoko_gake,morote_gari,kuchiki_taoshi,kibisu_gaeshi,uchi_mata_sukashi,tsubame_gaeshi,osoto_gaeshi,ouchi_gaeshi,kouchi_gaeshi,hane_goshi_gaeshi,harai_goshi_gaeshi,uchi_mata_gaeshi,osoto_makikomi,uchi_mata_makikomi,harai_makikomi
