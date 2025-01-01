import csv
from datetime import datetime
from functools import reduce

from saju_algorithm.saju_core.saju import Saju
from collections import Counter


def get_10sin(type, idx):
    with open('../saju_data/10sin_{type}.csv'.format(type=type), encoding='utf-8') as f:
        rdr = csv.reader(f)
        gabja = [row for row in rdr]
        get_10sin_score = [float(0.0) if i == '' else float(i) for i in gabja[idx][1:]]
        ilgan = get_me_dd_gan()
        header = get_10sin_header(ilgan)
        result = {header[i]: float(get_10sin_score[i]) for i in range(0, 10)}
    return result


def get_me_dd_gan():
    ganji = Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0).getGanji()
    return ganji[1][0]


def get_10sin_header(ilgan):
    table = {
        "甲": ["편인", "정인", "비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관"],
        "乙": ["정인", "편인", "겁재", "비견", "상관", "식신", "정재", "편재", "정관", "편관"],
        "丙": ["편관", "정관", "편인", "정인", "비견", "겁재", "식신", "상관", "편재", "정재"],
        "丁": ["정관", "편관", "정인", "편인", "겁재", "비견", "상관", "식신", "정재", "편재"],
        "戊": ["편재", "정재", "편관", "정관", "편인", "정인", "비견", "겁재", "식신", "상관"],
        "己": ["정재", "편재", "정관", "편관", "정인", "편인", "겁재", "비견", "상관", "식신"],
        "庚": ["식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인", "비견", "겁재"],
        "辛": ["상관", "식신", "정재", "편재", "정관", "편관", "정인", "편인", "겁재", "비견"],
        "壬": ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"],
        "癸": ["겁재", "비견", "상관", "식신", "정재", "편재", "정관", "편관", "정인", "편인"]
    }
    return table[ilgan]


def get_dae_won(saju, in_year, yyyy, sex=1):
    age = (int(yyyy) - int(in_year)) + 1
    generation = int(age / 10)

    try:
        sex = int(sex)
    except:
        sex = 1

    luck = saju.getLuck(in_sex=sex)
    dea_luck = int(luck[0])
    dea_wonns = luck[1]

    generations = [0+dea_luck, 10+dea_luck, 20+dea_luck, 30+dea_luck, 40+dea_luck, 50+dea_luck, 60+dea_luck, 70+dea_luck, 80+dea_luck, 90+dea_luck]

    if age >= 0 + dea_luck and age < 10 + dea_luck:
        generation = 0
    elif age >= 10 + dea_luck and age < 20 + dea_luck:
        generation = 1
    elif age >= 20 + dea_luck and age < 30 + dea_luck:
        generation = 2
    elif age >= 30 + dea_luck and age < 40 + dea_luck:
        generation = 3
    elif age >= 40 + dea_luck and age < 50 + dea_luck:
        generation = 4
    elif age >= 50 + dea_luck and age < 60 + dea_luck:
        generation = 5
    elif age >= 60 + dea_luck and age < 70 + dea_luck:
        generation = 6
    elif age >= 70 + dea_luck and age < 80 + dea_luck:
        generation = 7
    elif age >= 80 + dea_luck and age < 90 + dea_luck:
        generation = 8
    elif age >= 90 + dea_luck and age < 100 + dea_luck:
        generation = 9
    else:
        generation = 9

    dea_woon = dea_wonns[generation]

    return dea_luck, dea_woon


def get_total_10sin_score(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1):
    saju = Saju(in_year=in_year, in_month=in_month, in_day=in_day, in_hour=in_hour, in_min=in_min)
    yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = saju.makeGanji()

    yyyy = int(datetime.today().strftime('%Y'))
    mm = int(datetime.today().strftime('%m'))
    dd = int(datetime.today().strftime('%d'))
    hh = int(datetime.today().strftime('%H'))
    M = int(datetime.today().strftime('%M'))

    now_saju = Saju(in_year=yyyy, in_month=mm, in_day=dd, in_hour=hh, in_min=M)
    now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = now_saju.makeGanji(in_syear=yyyy, in_smonth=mm, in_sday=dd, in_shour=hh, in_smin=M)

    # 대운
    _10sin_dae_won = get_dae_won(saju=saju, in_year=in_year, yyyy=yyyy, sex=sex)
    dae_won_idx = saju.caGanjiTable.index(_10sin_dae_won[1])

    # 연주, 월주, 일주, 시주
    _10sin_year = get_10sin("year", yeon_ju_idx)
    # print("년주", sum(_10sin_year.values()))

    _10sin_month = get_10sin("month", wol_ju_idx)
    # print("월주", sum(_10sin_month.values()))

    _10sin_day = get_10sin("day", il_ju_idx)
    # print("일주", sum(_10sin_day.values()))

    _10sin_time = get_10sin("time", si_ju_idx)
    # print("시주", sum(_10sin_time.values()))

    _10sin_dae_won = get_10sin("big_luck", dae_won_idx)
    # print("대운", _10sin_dae_won)

    _10sin_year_luck = get_10sin("year_luck", now_yeon_ju_idx)
    # print("세운", sum(_10sin_year_luck.values()))

    _10sin_month_luck = get_10sin("month_luck", now_wol_ju_idx)
    # print("월운", sum(_10sin_month_luck.values()))

    _10sin_day_luck = get_10sin("day_luck", now_il_ju_idx)
    # print("일운", sum(_10sin_day_luck.values()))

    _10sin_time_luck = get_10sin("time_luck", now_si_ju_idx)
    # print("시운", sum(_10sin_time_luck.values()))

    _10sin_idx_list = [
        si_ju_idx,
        il_ju_idx,
        wol_ju_idx,
        yeon_ju_idx,
        dae_won_idx,
        now_yeon_ju_idx,
        now_wol_ju_idx,
        now_il_ju_idx,
        now_si_ju_idx
    ]
    print("평균온도: ", saju.get_temperature(_10sin_idx_list))
    print("평균숩도: ", saju.get_humidity(_10sin_idx_list))
    print("날씨", saju.get_weather(saju.now_getGanji()[3][0]))

    dicts = [_10sin_year, _10sin_month, _10sin_day, _10sin_time, _10sin_dae_won, _10sin_year_luck, _10sin_month_luck, _10sin_day_luck, _10sin_time_luck]
    saju_dict = [_10sin_year, _10sin_month, _10sin_day, _10sin_time]
    total_10sin_score = reduce(lambda a, b: a.update(b) or a, dicts, Counter())
    total_10sin_only_saju_score = reduce(lambda a, b: a.update(b) or a, saju_dict, Counter())
    # print(total_10sin_only_saju_score)
    # print(total_10sin_score)
    _10sin_score = dict(zip(total_10sin_score.keys(), map(lambda x: round((x[1] / 380) * 100, 1), total_10sin_score.items())))
    # print(sum(_10sin_score.values()))

    # 재성( 편재, 정재 ) , 관성( 편관, 정관), 인성( 편인, 정인 ), 비겁( 비견, 겁재 ),
    if sex == 1:
        result = {
            "애정운": round((_10sin_score["편재"] + _10sin_score["정재"]) * (1 / 2) + _10sin_score["식신"] + _10sin_score["상관"], 1),  # 3
            "재물운": round((_10sin_score["편재"] + _10sin_score["정재"]) * (1 / 2) + _10sin_score["정관"], 1),  # 2
            "건강운": round(_10sin_score["비견"] + _10sin_score["겁재"], 1),  # 2
            "학업운": round(_10sin_score["편인"] + _10sin_score["정인"] + _10sin_score["편관"], 1),  # 3
        }
    else:
        result = {
            "애정운": round(_10sin_score["상관"] + _10sin_score["편관"] + _10sin_score["정관"], 1),  # 3
            "재물운": round(_10sin_score["편재"] + _10sin_score["정재"] + _10sin_score["식신"], 1),  # 3
            "건강운": round(_10sin_score["비견"] + _10sin_score["겁재"], 1),  # 2
            "학업운": round(_10sin_score["편인"] + _10sin_score["정인"], 1),  # 2
        }
    print(result)


if __name__ == '__main__':
    get_total_10sin_score(in_year=1994, in_month=7, in_day=4, in_hour=11, in_min=35, sex=2)  # 희나
    get_total_10sin_score(in_year=1997, in_month=10, in_day=10, in_hour=11, in_min=12, sex=2)  # 혜리
    get_total_10sin_score(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1)  # 영환
    get_total_10sin_score(in_year=1996, in_month=4, in_day=18, in_hour=11, in_min=0, sex=1)  # 규성
    get_total_10sin_score(in_year=1996, in_month=2, in_day=23, in_hour=5, in_min=47, sex=2)  # 은경
    get_total_10sin_score(in_year=1994, in_month=8, in_day=1, in_hour=14, in_min=0, sex=1)  # 창식
    get_total_10sin_score(in_year=1994, in_month=12, in_day=26, in_hour=18, in_min=30, sex=2)  # 지민
    get_total_10sin_score(in_year=1988, in_month=8, in_day=14, in_hour=17, in_min=30, sex=1)  # 영주
    get_total_10sin_score(in_year=1995, in_month=11, in_day=22, in_hour=13, in_min=7, sex=2)  # 수지
    get_total_10sin_score(in_year=2021, in_month=12, in_day=28, in_hour=11, in_min=7, sex=1)  # 오늘군
    get_total_10sin_score(in_year=1971, in_month=12, in_day=28, in_hour=11, in_min=7, sex=2)  # 오늘양
    get_total_10sin_score(in_year=1969, in_month=1, in_day=28, in_hour=12, in_min=0, sex=2)  # 창식어머님
    get_total_10sin_score(in_year=1969, in_month=8, in_day=30, in_hour=5, in_min=0, sex=2)  # 혜리어머님
    get_total_10sin_score(in_year=1995, in_month=2, in_day=25, in_hour=10, in_min=30, sex=1)  # 장원
    # saju = Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0).get_temperature()
