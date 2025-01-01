
def chun_gan_ji(saju_yyyy, saju_mm, saju_dd, saju_hh, woon_dea, woon_yyyy, woon_mm, woon_dd, woon_hh):
    sky_s_y = saju_yyyy[0]
    grd_s_y = saju_yyyy[1]

    sky_s_m = saju_mm[0]
    grd_s_m = saju_mm[1]

    sky_s_d = saju_dd[0]
    grd_s_d = saju_dd[1]

    sky_s_h = saju_hh[0]
    grd_s_h = saju_hh[1]

    sky_s_b = woon_dea[0]
    grd_s_b = woon_dea[1]

    sky_w_y = woon_yyyy[0]
    grd_w_y = woon_yyyy[1]

    sky_w_m = woon_mm[0]
    grd_w_m = woon_mm[1]

    sky_w_d = woon_dd[0]
    grd_w_d = woon_dd[1]

    sky_w_h = woon_hh[0]
    grd_w_h = woon_hh[1]

    sky = '{sky_s_y}{sky_s_m}{sky_s_d}{sky_s_h}{sky_s_b}{sky_w_y}{sky_w_m}{sky_w_d}{sky_w_h}'.format(
        sky_s_y=sky_s_y, sky_s_m=sky_s_m, sky_s_d=sky_s_d, sky_s_h=sky_s_h,
        sky_s_b=sky_s_b,
        sky_w_y=sky_w_y, sky_w_m=sky_w_m, sky_w_d=sky_w_d, sky_w_h=sky_w_h
    )
    grd = '{grd_s_y}{grd_s_m}{grd_s_d}{grd_s_h}{grd_s_b}{grd_w_y}{grd_w_m}{grd_w_d}{grd_w_h}'.format(
        grd_s_y=grd_s_y, grd_s_m=grd_s_m, grd_s_d=grd_s_d, grd_s_h=grd_s_h,
        grd_s_b=grd_s_b,
        grd_w_y=grd_w_y, grd_w_m=grd_w_m, grd_w_d=grd_w_d, grd_w_h=grd_w_h
    )

    return {
        'sky': sky, 'grd': grd,

        'sky_s_y': sky_s_y, 'sky_s_m': sky_s_m, 'sky_s_d': sky_s_d, 'sky_s_h': sky_s_h,
        'sky_s_b': sky_s_b,
        'sky_w_y': sky_w_y, 'sky_w_m': sky_w_m, 'sky_w_d': sky_w_d, 'sky_w_h': sky_w_h,

        'grd_s_y': grd_s_y, 'grd_s_m': grd_s_m, 'grd_s_d': grd_s_d, 'grd_s_h': grd_s_h,
        'grd_s_b': grd_s_b,
        'grd_w_y': grd_w_y, 'grd_w_m': grd_w_m, 'grd_w_d': grd_w_d, 'grd_w_h': grd_w_h,

        'saju_yyyy': saju_yyyy, 'saju_mm': saju_mm, 'saju_dd': saju_dd, 'saju_hh': saju_hh,
        'woon_dea': woon_dea,
        'woon_yyyy': woon_yyyy, 'woon_mm': woon_mm, 'woon_dd': woon_dd, 'woon_hh': woon_hh
    }


def chungan_sum(sky, dea, yyyy, mm, dd, hh):
    # 갑(甲)	을(乙)	병(丙)	정(丁)	무(戊)	기(己)	경(庚)	신(辛)	임(壬)	계(癸)
    sum = {"甲": {'k': '甲', 's': '목', 'e': '토'},
           "乙": {'k': '乙', 's': '목', 'e': '금'},
           "丙": {'k': '丙', 's': '화', 'e': '수'},
           "丁": {'k': '丁', 's': '화', 'e': '목'},
           "戊": {'k': '戊', 's': '토', 'e': '화'},
           "己": {'k': '己', 's': '토', 'e': '토'},
           "庚": {'k': '庚', 's': '금', 'e': '금'},
           "辛": {'k': '辛', 's': '금', 'e': '수'},
           "壬": {'k': '壬', 's': '수', 'e': '목'},
           "癸": {'k': '癸', 's': '수', 'e': '화'}, }

    def sum_oheag_change(woon):
        # 갑(甲)	을(乙)	병(丙)	정(丁)	무(戊)	기(己)	경(庚)	신(辛)	임(壬)	계(癸)
        sum_val = None
        if woon == "甲":
            if "己" in sky:
                sum_val = sum[woon]
        elif woon == "乙":
            if "庚" in sky:
                sum_val = sum[woon]
        elif woon == "丙":
            if "辛" in sky:
                sum_val = sum[woon]
        elif woon == "丁":
            if "壬" in sky:
                sum_val = sum[woon]
        elif woon == "戊":
            if "癸" in sky:
                sum_val = sum[woon]
        elif woon == "己":
            if "甲" in sky:
                sum_val = sum[woon]
        elif woon == "庚":
            if "乙" in sky:
                sum_val = sum[woon]
        elif woon == "辛":
            if "丙" in sky:
                sum_val = sum[woon]
        elif woon == "壬":
            if "丁" in sky:
                sum_val = sum[woon]
        elif woon == "癸":
            if "戊" in sky:
                sum_val = sum[woon]

        return sum_val

    print(sky, dea, yyyy, mm, dd, hh)
    b = sum_oheag_change(dea)
    y = sum_oheag_change(yyyy)
    m = sum_oheag_change(mm)
    d = sum_oheag_change(dd)
    h = sum_oheag_change(hh)

    return {'b':b,'y':y,'m':m,'d':d,'h':h,}


def jiji_6_sum(ground, dea, yyyy, mm, dd, hh):
    # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
    # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)

    sum = {"子": {'k': '子', 's': '수', 'e': '토'},
           "丑": {'k': '丑', 's': '토', 'e': '토'},
           "寅": {'k': '寅', 's': '목', 'e': '목'},
           "卯": {'k': '卯', 's': '목', 'e': '화'},
           "辰": {'k': '辰', 's': '토', 'e': '금'},
           "巳": {'k': '巳', 's': '화', 'e': '수'},
           "午": {'k': '午', 's': '화', 'e': '화'},
           "未": {'k': '未', 's': '토', 'e': '화'},
           "申": {'k': '申', 's': '금', 'e': '수'},
           "酉": {'k': '酉', 's': '그', 'e': '금'},
           "戌": {'k': '戌', 's': '토', 'e': '화'},
           "亥": {'k': '亥', 's': '수', 'e': '목'}, }

    def sum_oheag_change(woon):
        # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)
        sum_val = None
        if woon == "子":
            if "丑" in ground:
                sum_val = sum[woon]
        elif woon == "丑":
            if "子" in ground:
                sum_val = sum[woon]
        elif woon == "寅":
            if "亥" in ground:
                sum_val = sum[woon]
        elif woon == "卯":
            if "戌" in ground:
                sum_val = sum[woon]
        elif woon == "辰":
            if "酉" in ground:
                sum_val = sum[woon]
        elif woon == "巳":
            if "申" in ground:
                sum_val = sum[woon]
        elif woon == "午":
            if "未" in ground:
                sum_val = sum[woon]
        # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)
        elif woon == "未":
            if "午" in ground:
                sum_val = sum[woon]
        elif woon == "申":
            if "巳" in ground:
                sum_val = sum[woon]
        elif woon == "酉":
            if "辰" in ground:
                sum_val = sum[woon]
        elif woon == "戌":
            if "卯" in ground:
                sum_val = sum[woon]
        elif woon == "亥":
            if "寅" in ground:
                sum_val = sum[woon]

        return sum_val

    print(ground, dea, yyyy, mm, dd, hh)
    b = sum_oheag_change(dea)
    y = sum_oheag_change(yyyy)
    m = sum_oheag_change(mm)
    d = sum_oheag_change(dd)
    h = sum_oheag_change(hh)

    return {'b':b,'y':y,'m':m,'d':d,'h':h,}


def jiji_3_sum(ground, dea, yyyy, mm, dd, hh):
    # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
    # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)

    sum = {"子": {'k': '子', 's': '수', 'e': '금'},
           "丑": {'k': '丑', 's': '토', 'e': '수'},
           "寅": {'k': '寅', 's': '목', 'e': '화'},
           "卯": {'k': '卯', 's': '목', 'e': '목'},
           "辰": {'k': '辰', 's': '토', 'e': '금'},
           "巳": {'k': '巳', 's': '화', 'e': '수'},
           "午": {'k': '午', 's': '화', 'e': '화'},
           "未": {'k': '未', 's': '토', 'e': '목'},
           "申": {'k': '申', 's': '금', 'e': '금'},
           "酉": {'k': '酉', 's': '금', 'e': '수'},
           "戌": {'k': '戌', 's': '토', 'e': '화'},
           "亥": {'k': '亥', 's': '수', 'e': '목'}, }

    def sum_oheag_change(woon):
        # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)
        sum_val = None
        if woon == "子":
            # 신申 자子 진辰 # 진辰 자子 신申
            if "申子辰" in ground or "辰子辰" in ground:
                sum_val = sum[woon]
        elif woon == "丑":
            # 사巳 유酉 축丑 # 축丑 유酉 사巳
            if "巳酉丑" in ground or "丑酉巳" in ground:
                sum_val = sum[woon]
        elif woon == "寅":
            # 인寅 오午 술戌 # 술戌 오午 인寅
            if "寅午戌" in ground or "戌午寅" in ground:
                sum_val = sum[woon]
        elif woon == "卯":
            # 해亥 묘卯 미未 # 미未 묘卯 해亥
            if "亥卯未" in ground or "未卯亥" in ground:
                sum_val = sum[woon]
        elif woon == "辰":
            if "申子辰" in ground or "辰子辰" in ground:
                sum_val = sum[woon]
        elif woon == "巳":
            if "巳酉丑" in ground or "丑酉巳" in ground:
                sum_val = sum[woon]
        elif woon == "午":
            if "寅午戌" in ground or "戌午寅" in ground:
                sum_val = sum[woon]
        # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)
        elif woon == "未":
            if "亥卯未" in ground or "未卯亥" in ground:
                sum_val = sum[woon]
        elif woon == "申":
            if "申子辰" in ground or "辰子辰" in ground:
                sum_val = sum[woon]
        elif woon == "酉":
            if "巳酉丑" in ground or "丑酉巳" in ground:
                sum_val = sum[woon]
        elif woon == "戌":
            if "寅午戌" in ground or "戌午寅" in ground:
                sum_val = sum[woon]
        elif woon == "亥":
            if "亥卯未" in ground or "未卯亥" in ground:
                sum_val = sum[woon]

        return sum_val

    print(ground, dea, yyyy, mm, dd, hh)
    b = sum_oheag_change(dea)
    y = sum_oheag_change(yyyy)
    m = sum_oheag_change(mm)
    d = sum_oheag_change(dd)
    h = sum_oheag_change(hh)

    return {'b':b,'y':y,'m':m,'d':d,'h':h,}


def jiji_bang_sum(ground, dea, yyyy, mm, dd, hh):
    # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
    # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)

    sum = {"子":{'s':'수','e':'수'},
           "丑":{'s':'토','e':'수'},
           "寅":{'s':'목','e':'목'},
           "卯":{'s':'목','e':'목'},
           "辰":{'s':'토','e':'목'},
           "巳":{'s':'화','e':'화'},
           "午":{'s':'화','e':'화'},
           "未":{'s':'토','e':'화'},
           "申":{'s':'금','e':'금'},
           "酉":{'s':'금','e':'금'},
           "戌":{'s':'토','e':'금'},
           "亥":{'s':'수','e':'수'},}

    def sum_oheag_change(woon):
        # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)
        sum_val = None
        if woon == "子":
            # 해	자	축
            # 축	자	해
            if "亥子丑" in ground or "丑子亥" in ground:
                sum_val = sum[woon]
        elif woon == "丑":
            # 해	자	축
            # 축	자	해
            if "亥子丑" in ground or "丑子亥" in ground:
                sum_val = sum[woon]
        elif woon == "寅":
            # 인	묘	진
            # 진	묘	인
            if "寅卯辰" in ground or "辰卯寅" in ground:
                sum_val = sum[woon]
        elif woon == "卯":
            # 인	묘	진
            # 진	묘	인
            if "寅卯辰" in ground or "辰卯寅" in ground:
                sum_val = sum[woon]
        elif woon == "辰":
            # 인	묘	진
            # 진	묘	인
            if "寅卯辰" in ground or "辰卯寅" in ground:
                sum_val = sum[woon]
        elif woon == "巳":
            # 사	오	미
            # 미	오	사
            if "巳午未" in ground or "未午巳" in ground:
                sum_val = sum[woon]
        elif woon == "午":
            # 사	오	미
            # 미	오	사
            if "巳午未" in ground or "未午巳" in ground:
                sum_val = sum[woon]
        # "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        # 자(子)	축(丑)	인(寅)	묘(卯)	진(辰)	사(巳)	오(午)	미(未)	신(申)	유(酉)	술(戌)	해(亥)
        elif woon == "未":
            # 사	오	미
            # 미	오	사
            if "巳午未" in ground or "未午巳" in ground:
                sum_val = sum[woon]
        elif woon == "申":
            # 신	유	술
            # 술	유	신
            if "申酉戌" in ground or "辰酉申" in ground:
                sum_val = sum[woon]
        elif woon == "酉":
            # 신	유	술
            # 술	유	신
            if "申酉戌" in ground or "辰酉申" in ground:
                sum_val = sum[woon]
        elif woon == "戌":
            # 신	유	술
            # 술	유	신
            if "申酉戌" in ground or "戌酉申" in ground:
                sum_val = sum[woon]
        elif woon == "亥":
            # 해	자	축
            # 축	자	해
            if "亥子丑" in ground or "丑子亥" in ground:
                sum_val = sum[woon]

        return sum_val

    print(ground, dea, yyyy, mm, dd, hh)
    b = sum_oheag_change(dea)
    y = sum_oheag_change(yyyy)
    m = sum_oheag_change(mm)
    d = sum_oheag_change(dd)
    h = sum_oheag_change(hh)

    return {'b':b,'y':y,'m':m,'d':d,'h':h,}


def oheang_hab(saju_yyyy='xx', saju_mm='xx', saju_dd='xx', saju_hh='xx',
                woon_dea='xx',
                woon_yyyy='xx', woon_mm='xx', woon_dd='xx', woon_hh='xx'):
    cgj = chun_gan_ji(saju_yyyy=saju_yyyy, saju_mm=saju_mm, saju_dd=saju_dd, saju_hh=saju_hh,
                woon_dea=woon_dea,
                woon_yyyy=woon_yyyy, woon_mm=woon_mm, woon_dd=woon_dd, woon_hh=woon_hh)

    sky_sum = chungan_sum(sky=cgj['sky'], dea=cgj['sky_s_b'],
                yyyy=cgj['sky_w_y'], mm=cgj['sky_w_m'], dd=cgj['sky_w_d'], hh=cgj['sky_w_h'])

    grd_6_sum = jiji_6_sum(ground=cgj['grd'], dea=cgj['grd_s_b'],
                          yyyy=cgj['grd_w_y'], mm=cgj['grd_w_m'], dd=cgj['grd_w_d'], hh=cgj['grd_w_h'])

    grd_3_sum = jiji_3_sum(ground=cgj['grd'], dea=cgj['grd_s_b'],
                           yyyy=cgj['grd_w_y'], mm=cgj['grd_w_m'], dd=cgj['grd_w_d'], hh=cgj['grd_w_h'])

    grd_bang_sum = jiji_bang_sum(ground=cgj['grd'], dea=cgj['grd_s_b'],
                           yyyy=cgj['grd_s_y'], mm=cgj['grd_s_m'], dd=cgj['grd_s_d'], hh=cgj['grd_s_h'])
    print(cgj)
    print(sky_sum)
    print(grd_6_sum)
    print(grd_3_sum)
    print(grd_bang_sum)

    return {'천간지':cgj, '천간합':sky_sum, '지지육합':grd_6_sum, '지지삼합':grd_3_sum,'지지방합':grd_bang_sum}


if __name__ == '__main__':
    hab = oheang_hab(saju_yyyy='丙辰', saju_mm='戊酉', saju_dd='丁申', saju_hh='丁未',
               woon_dea='丙午',
               woon_yyyy='辛丑', woon_mm='辛卯', woon_dd='丙辰', woon_hh='己亥')

    print(hab)