import math
import csv
import random
import os
from collections import Counter
from datetime import datetime
from functools import reduce

from django.conf import settings

module_dir = os.path.dirname(__file__)
base_file_path = os.path.join(module_dir, '../../saju_data/10sin_{type}.csv')
temperature_file_path = os.path.join(module_dir, '../../saju_data/saju_temperature.csv')
humidity_file_path = os.path.join(module_dir, '../../saju_data/saju_humidity.csv')
# base_file_path = settings.BASE_DIR / 'saju_data' / 'oheang_{type}.csv'


class Saju():
    # = == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # Name: CSaju --> init
    # Desc: 클래스 선언
    # Input: None
    # Output: None
    # = == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    def __init__(self, in_year=0, in_month=0, in_day=0, in_hour=0, in_min=0, sex=1):
        self.PREV_24TERMS = 0
        self.MID_24TERMS = 1
        self.NEXT_24TERMS = 2

        self.me_year = in_year       # 사주 검색 대상 년도
        self.me_month = in_month     # 사주 검색 대상 월
        self.me_day = in_day         # 사주 검색 대상 일
        self.me_hour = in_hour       # 사주 검색 대상 시
        self.me_min = in_min         # 사주 검색 대상 분
        self.sex = sex               # 사주 검색 대상 성별

        self.m_unityear = 1996
        self.m_unitmonth = 2
        self.m_unitday = 4
        self.m_unithour = 22
        self.m_unitmin = 8

        self.now_year = int(datetime.today().strftime('%Y'))  # 현재 년도
        self.now_month = int(datetime.today().strftime('%m'))  # 현재 월
        self.now_day = int(datetime.today().strftime('%d'))   # 현재 일
        self.now_hour = int(datetime.today().strftime('%H'))   # 현재 시간
        self.now_min = int(datetime.today().strftime('%M'))   # 현재 분

        self.m_GanjiYear = -1    # 년 간지
        self.m_GanjiMonth = -1   # 월 간지
        self.m_GanjiDay = -1     # 일 간지
        self.m_GanjiHour = -1    # 시 간지

        self.naMonthTable = [0, 21355, 42843, 64498, 86335, 108366, 130578, 152958,
                             175471, 198077, 220728, 243370, 265955, 288432, 310767, 332928,
                             354903, 376685, 398290, 419736, 441060, 462295, 483493, 504693, 525949]

        self.ca24TermsTable = ["입춘", "우수", "경칩", "춘분", "청명", "곡우",
                               "입하", "소만", "망종", "하지", "소서", "대서",
                               "입추", "처서", "백로", "추분", "한로", "상강",
                               "입동", "소설", "대설", "동지", "소한", "대한", "입춘"]  # 백로 (절기)

        self.caGanTable = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]  # 갑.을.병.정.무.기.경.신.임.계

        self.caJiTable = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]  # 자(子), 축(丑), 인(寅), 묘(卯), 진(辰), 사(巳), 오(午), 미(未), 신(申), 유(酉), 술(戌), 해(亥)

        self.caGanjiTable = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰",
                             "己巳", "庚午", "辛未", "壬申", "癸酉",
                             "甲戌", "乙亥", "丙子", "丁丑", "戊寅",
                             "己卯", "庚辰", "辛巳", "壬午", "癸未",
                             "甲申", "乙酉", "丙戌", "丁亥", "戊子",
                             "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
                             "甲午", "乙未", "丙申", "丁酉", "戊戌",
                             "己亥", "庚子", "辛丑", "壬寅", "癸卯",
                             "甲辰", "乙巳", "丙午", "丁未", "戊申",
                             "己酉", "庚戌", "辛亥", "壬子", "癸丑",
                             "甲寅", "乙卯", "丙辰", "丁巳", "戊午",
                             "己未", "庚申", "辛酉", "壬戌", "癸亥"]

        self.ko_GanjiTable = ["갑자", "을축", "병인", "정묘", "무진", "기사", "경오", "신미", "임신", "계유", "갑술", "을해", "병자", "정축", "무인", "기묘", "경진", "신사", "임오", "계미",
                              "갑신", "을유", "병술", "정해", "무자", "기축", "경인", "신묘", "임진", "계사", "갑오", "을미", "병신", "정유", "무술", "기해", "경자", "신축", "임인", "계묘",
                              "갑진", "을사", "병오", "정미", "무신", "기유", "경술", "신해", "임자", "계축", "갑인", "을묘", "병진", "정사", "무오", "기미", "경신", "신유", "임술", " 계해"]

        self.caWeeknameTable = ["일", "월", "화", "수", "목", "금", "토"]

        self.caYearTable = [
                        # 1881: 0
                        "1212122322121", "1212121221220", "1121121222120", "2112132122122", "2112112121220",
                        "2121211212120", "2212321121212", "2122121121210", "2122121212120", "1232122121212",
                        # 1891: 10
                        "1212121221220", "1121123221222", "1121121212220", "1212112121220", "2121231212121",
                        "2221211212120", "1221212121210", "2123221212121", "2121212212120", "1211212232212",
                        # 1901: 20
                        "1211212122210", "2121121212220", "1212132112212", "2212112112210", "2212211212120",
                        "1221412121212", "1212122121210", "2112212122120", "1231212122212", "1211212122210",
                        # 1911: 30
                        "2121123122122", "2121121122120", "2212112112120", "2212231212112", "2122121212120",
                        "1212122121210", "2132122122121", "2112121222120", "1211212322122", "1211211221220",
                        # 1921: 40
                        "2121121121220", "2122132112122", "1221212121120", "2121221212110", "2122321221212",
                        "1121212212210", "2112121221220", "1231211221222", "1211211212220", "1221123121221",
                        # 1931: 50
                        "2221121121210", "2221212112120", "1221241212112", "1212212212120", "1121212212210",
                        "2114121212221", "2112112122210", "2211211412212", "2211211212120", "2212121121210",
                        # 1941: 60
                        "2212214112121", "2122122121120", "1212122122120", "1121412122122", "1121121222120",
                        "2112112122120", "2231211212122", "2121211212120", "2212121321212", "2122121121210",
                        # 1951: 70
                        "2122121212120", "1212142121212", "1211221221220", "1121121221220", "2114112121222",
                        "1212112121220", "2121211232122", "1221211212120", "1221212121210", "2121223212121",
                        # 1961: 80
                        "2121212212120", "1211212212210", "2121321212221", "2121121212220", "1212112112210",
                        "2223211211221", "2212211212120", "1221212321212", "1212122121210", "2112212122120",
                        # 1971: 90
                        "1211232122212", "1211212122210", "2121121122210", "2212312112212", "2212112112120",
                        "2212121232112", "2122121212110", "2212122121210", "2112124122121", "2112121221220",
                        # 1981: 100
                        "1211211221220", "2121321122122", "2121121121220", "2122112112322", "1221212112120",
                        "1221221212110", "2122123221212", "1121212212210", "2112121221220", "1211231212222",
                        # 1991: 110
                        "1211211212220", "1221121121220", "1223212112121", "2221212112120", "1221221232112",
                        "1212212122120", "1121212212210", "2112132212221", "2112112122210", "2211211212210",
                        # 2001: 120
                        "2221321121212", "2212121121210", "2212212112120", "1232212122112", "1212122122120",
                        "1121212322122", "1121121222120", "2112112122120", "2211231212122", "2121211212120",
                        # 2011: 130
                        "2122121121210", "2124212112121", "2122121212120", "1212121223212", "1211212221220",
                        "1121121221220", "2112132121222", "1212112121220", "2121211212120", "2122321121212",
                        # 2021: 140
                        "1221212121210", "2121221212120", "1232121221212", "1211212212210", "2121123212221",
                        "2121121212220", "1212112112220", "1221231211221", "2212211211220", "1212212121210",
                        # 2031: 150
                        "2123212212121", "2112122122120", "1211212322212", "1211212122210", "2121121122120",
                        "2212114112122", "2212112112120", "2212121211210", "2212232121211", "2122122121210",
                        # 2041: 160
                        "2112122122120", "1231212122212", "1211211221220"]

        self.naDayPerMonthTable = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        '''
         조후용신표: 일간과 월지의 조합, 
         갑: 0, 을: 1, 병: 2, 정: 3, 무: 4, 기: 5, 경: 6, 신: 7, 임: 8, 계: 9
        '''
        self.caJohuTable = ["332669996666",  # 일간: 갑
                            "222299992992",  # 일간: 을
                            "888888888800",  # 일간: 병
                            "000600800000",  # 일간: 정
                            "222200892200",  # 일간: 무
                            "222029992202",  # 일간: 기
                            "324308833303",  # 일간: 경
                            "225888888888",  # 일간: 신
                            "426468974004",  # 일간: 임
                            "227627663776"]  # 일간: 계

        ''' 현재상태표: 일간과
        현재일시의
        조합(일간, 가로: 시, 세로: 일),
        // 갑: 0, 을: 1, 병: 2, 정: 3, 무: 4, 기: 5, 경: 6, 신: 7, 임: 8, 계: 9
        '''
        self.caCurrentGanTable = [
            # 일간: 갑(0)
            ["0123329800", "1223238911", "0245452301", "0145452310", "2345328901",
             "2323329810", "2323989801", "8923010189", "0101010101", "0101019801"],
            # 일간: 을(1)
            ["0123329800", "1123238911", "0123454501", "0123454501", "2345456701",
             "2345456701", "8923898901", "8923898910", "0101010101", "0101010101"],
            # 일간: 병(2)
            ["0123459801", "1123238911", "2323454501", "3323454510", "2345456701",
             "2345456710", "6745456701", "7645456701", "2345450101", "2345450101"],
            # 일간: 정(3)
            ["0123329800", "0123238911", "2345454501", "2345454510", "2345456701",
             "2345456710", "2345456701", "3245456701", "0101450101", "0101450101"],
            # 일간: 무(4)
            ["3223236723", "1223236723", "2345454501", "2345454510", "2345328901",
             "2323329810", "6645459801", "7774576789", "3245676789", "2345676789"],
            # 일간: 기(5)
            ["2223456745", "2223456745", "2345454545", "2223454545", "6745456789",
             "2223679867", "6789676689", "6745456789", "2345676767", "2345676767"],
            # 일간: 경(6)
            ["8945668966", "8945238989", "4545458989", "4545458989", "6645456766",
             "6645456711", "8988666701", "9833456789", "0189666701", "0189666701"],
            # 일간: 신(7)
            ["8945018989", "8945778989", "6745456789", "8945456789", "6745456776",
             "6745456776", "8989456789", "8989456789", "0189776789", "0189776789"],
            # 일간: 임(8)
            ["0123018800", "0123018911", "2223778901", "3301758910", "0167776767",
             "0167776710", "8889776789", "8889776789", "0101016789", "0101016789"],
            # 일간: 계(9)
            ["0123018900", "1123018911", "0123678801", "0123678801", "0167678901",
             "0167678910", "2223676789", "3323676789", "0101016789", "0101016789"]]

        ''' 
        현재상태간과 색과의 조합, 
        갑: 0, 을: 1, 병: 2, 정: 3, 무: 4, 기: 5, 경: 6, 신: 7, 임: 8, 계: 9
        '''
        self.caColorGanTable = ["8901678989",  # 검정 COLOR_BLACK
                                "8945676789",  # 흰색 COLOR_WHITE
                                "0110019801",  # 청록 COLOR_BLUISHGREEN
                                "0110019823",  # 초록 COLOR_GREEN
                                "3223452301",  # 황록 COLOR_YELLOWISHGREEN
                                "2323454501",  # 진홍 COLOR_CRIMSON
                                "3232454501",  # 주홍 COLOR_SCARLET
                                "2323454501",  # 주황 COLOR_ORANGE
                                "3232454545",  # 노랑 COLOR_YELLOW
                                "1010458901",  # 보라 COLOR_VIOLET
                                "8810018989",  # 파랑 COLOR_BLUE
                                "0123678901"]  # 자주 COLOR_PURPLE

        '''
        십간에 따른 12 지(무, 기는 현재시간에 따라 다름)
        자: 0, 축: 1, 인: 2, 묘: 3, 진: 4, 사: 5, 오: 6, 미: 7, 신: 8, 유: 9, 술: 10, 해: 11
        '''
        self.naGanJiTable = [2, 3, 5, 6, -1, -1, 8, 9, 11, 0]

        ''' 
        12 지에 따른 음악 조성: [메이저:0, 마이너: 1][12지]
        '''
        self.caJosengTable = [
            ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"],
            ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]]

        self.weather_table_case1 = {
            '甲': ["번개", "안개", "황사", "미세먼지", "폭우", "태풍", "미풍", "미세먼지", "황사", "소나기"],
            '乙': ["황사", "달빛", "쨍쨍", "구름", "쨍쨍", "미세먼지", "무지개", "맑음", "흐림", "맑음"],
            '丙': ["달빛", "소나기", "폭우", "달빛", "태풍", "무지개", "폭우", "소나기", "무지개", "번개"],
            '丁': ["소나기", "맑음", "무지개", "안개", "무지개", "폭우", "쨍쨍", "달빛", "미풍", "달빛"],
            '戊': ["쨍쨍", "쨍쨍", "흐림", "가랑눈", "황사", "맑음", "맑음", "구름", "함박눈", "미세먼지"],
            '己': ["안개", "맑음", "함박눈", "맑음", "안개", "미풍", "쨍쨍", "가랑눈", "쨍쨍", "미풍"],
            '庚': ["흐림", "번개", "미풍", "소나기", "맑음", "구름", "태풍", "안개", "폭우", "쨍쨍"],
            '辛': ["함박눈", "구름", "안개", "맑음", "함박눈", "가랑눈", "흐림", "미풍", "쨍쨍", "가랑눈"],
            '壬': ["폭우", "가랑눈", "태풍", "흐림", "달빛", "소나기", "함박눈", "번개", "구름", "무지개"],
            '癸': ["맑음", "폭우", "맑음", "미풍", "흐림", "쨍쨍", "소나기", "쨍쨍", "안개", "구름"],
        }

        self.weather_table_case2 = {
            '甲': ["태풍", "미풍", "미세먼지", "황사", "소나기", "번개", "안개", "황사", "미세먼지", "폭우"],
            '乙': ["미세먼지", "무지개", "맑음", "흐림", "맑음", "황사", "달빛", "쨍쨍", "구름", "쨍쨍"],
            '丙': ["무지개", "소나기", "소나기", "무지개", "번개", "달빛", "폭우", "폭우", "달빛", "태풍"],
            '丁': ["폭우", "쨍쨍", "달빛", "미풍", "달빛", "소나기", "맑음", "무지개", "안개", "무지개"],
            '戊': ["맑음", "맑음", "구름", "함박눈", "미세먼지", "쨍쨍", "쨍쨍", "흐림", "가랑눈", "황사"],
            '己': ["미풍", "쨍쨍", "가랑눈", "쨍쨍", "미풍", "안개", "맑음", "함박눈", "맑음", "안개"],
            '庚': ["구름", "태풍", "안개", "태풍", "쨍쨍", "흐림", "번개", "미풍", "번개", "맑음"],
            '辛': ["가랑눈", "미세먼지", "미풍", "쨍쨍", "가랑눈", "함박눈", "황사", "안개", "맑음", "함박눈"],
            '壬': ["소나기", "함박눈", "번개", "구름", "무지개", "폭우", "가랑눈", "태풍", "흐림", "달빛"],
            '癸': ["쨍쨍", "폭우", "쨍쨍", "안개", "구름", "맑음", "소나기", "맑음", "미풍", "흐림"],
        }

        self.oheng_table = {
            '甲': {"재성": "토", "식상": "화", "인성": "수", "비겁": "목", "관성": "금"},
            '乙': {"재성": "토", "식상": "화", "인성": "수", "비겁": "목", "관성": "금"},

            '丙': {"식상": "토", "비겁": "화", "관성": "수", "인성": "목", "재성": "금"},
            '丁': {"식상": "토", "비겁": "화", "관성": "수", "인성": "목", "재성": "금"},

            '戊': {"비겁": "토", "인성": "화", "재성": "수", "관성": "목", "식상": "금"},
            '己': {"비겁": "토", "인성": "화", "재성": "수", "관성": "목", "식상": "금"},

            '庚': {"인성": "토", "관성": "화", "식상": "수", "재성": "목", "비겁": "금"},
            '辛': {"인성": "토", "관성": "화", "식상": "수", "재성": "목", "비겁": "금"},

            '壬': {"관성": "토", "재성": "화", "비겁": "수", "식상": "목", "인성": "금"},
            '癸': {"관성": "토", "재성": "화", "비겁": "수", "식상": "목", "인성": "금"},
        }

        self.table_woonsung = ['장생', '목욕', '관대', '건록', '제왕', '쇠', '병', '사', '묘', '절', '태', '양']
        self.table_12 = {
            '甲': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
            # '乙': ['午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未'],
            '乙': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
            '丙': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
            # '丁': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
            '丁': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午',  '未'],
            '戊': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
            # '己': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
            '己': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午',  '未'],
            '庚': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
            # '辛': ['子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑'],
            '辛': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
            '壬': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'],
            # '癸': ['卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰'],
            '癸': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        }
        self.music_playlist_set = {
            '태': ["Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3"],
            '양': ["Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3"],
            '장생': ["Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1"],
            '목욕': ["Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3"],
            '관대': ["Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1"],
            '건록': ["Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1"],
            '제왕': ["Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1"],
            '쇠': ["Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2"],
            '병': ["Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2"],
            '사': ["Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2"],
            '묘': ["Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3", "Set 4", "Set 3"],
            '절': ["Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2", "Set 1", "Set 2"],
        }
        self.jiji_10sin_table = {
            '甲': ["정인", "정재", "비견", "겁재", "편재", "식신", "상관", "정재", "편관", "정관", "편관", "편인"],
            '乙': ["편인", "편재", "겁재", "비견", "정재", "상관", "식신", "편재", "정관", "편관", "정관", "정인"],
            '丙': ["정관", "상관", "편인", "정인", "식신", "비견", "겁재", "상관", "편재", "정재", "식신", "편관"],
            '丁': ["편관", "식신", "정인", "편인", "상관", "겁재", "비견", "식신", "정재", "편재", "상관", "정관"],
            '戊': ["정재", "겁재", "편관", "정관", "비견", "편인", "정인", "겁재", "식신", "상관", "비견", "편재"],
            '己': ["편재", "비견", "정관", "편관", "겁재", "정인", "편인", "비견", "상관", "식신", "겁재", "정재"],
            '庚': ["상관", "정인", "편재", "정재", "편인", "편관", "정관", "정인", "비견", "겁재", "편인", "식신"],
            '辛': ["식신", "편인", "정재", "편재", "정인", "정관", "편관", "편인", "겁재", "비견", "정인", "상관"],
            '壬': ["겁재", "정관", "식신", "상관", "편관", "편재", "정재", "정관", "편인", "정인", "편관", "비견"],
            '癸': ["비견", "편관", "상관", "식신", "정관", "정재", "편재", "편관", "정인", "편인", "정관", "겁재"],
        }
        self.josung_table = {
            "子": "C, a, c, Eb/D#",
            "丑": "Db/C#, a#, db/c#, E",
            "寅": "D, b, d, F",
            "卯": "Eb/D#, c, eb/d#, F#",
            "辰": "E, db/c#, e, G",
            "巳": "F, d, f, Ab/G#",
            "午": "F#, eb/d#, f#, A",
            "未": "G, e, g, Bb/A#",
            "申": "Ab/G#, f, ab/g#, B",
            "酉": "A, f#, a, C",
            "戌": "Bb/A#, g, bb/a#, Db/C#",
            "亥": "B, ab/g#, b, D"
        }

        # self.music_recommend = {
        #     "Set 1": ["장조", "장조", "장조", "장조", "장조", "장조", "장조", "장조", "장조", "장조", "장조", "장조"],
        #     "Set 2": ["단조", "단조", "단조", "단조", "단조", "단조", "단조", "단조", "단조", "단조", "단조", "단조"],
        #     "Set 3": ["장조", "장조", "장조", "단조", "단조", "단조", "장조", "장조", "장조", "단조", "단조", "단조"],
        #     "Set 4": ["단조", "단조", "단조", "장조", "장조", "장조", "단조", "단조", "단조", "장조", "장조", "장조"],
        # }

    ''' 
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    // Name: getDayOfDate
    // Desc: in_year의 1월 1일부터 in_year의 in_month월, in_day일까지의 날수계산
    // Input: int in_year: 특정 년
    // int in_month: 월
    // int in_day: 일
    // Output: long: 날수
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    '''
    def getDayOfDate(self, in_year, in_month, in_day):
        lDayCnt = 0

        for i in range(1, in_month):
            lDayCnt += 31;
            if i == 2 or i == 4 or i == 6 or i == 9 or i == 11:
                lDayCnt = lDayCnt - 1

            if i == 2:
                lDayCnt = lDayCnt - 2

                if in_year % 4 == 0:
                    lDayCnt = lDayCnt + 1
                if in_year % 100 == 0:
                    lDayCnt = lDayCnt - 1
                if in_year % 400 == 0:
                    lDayCnt = lDayCnt + 1
                if in_year % 4000 == 0:
                    lDayCnt = lDayCnt - 1

        return lDayCnt + in_day
    '''
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    // Name: getDayByDays
    // Desc: from에서 to까지의 일수 계산
    // Input: int in_fromyear  : 시작 년
    //		  int in_frommonth 	:      월
    //	      int in_fromday   	:      일
    //        int in_toyear  	:종료 년
    //		  int in_tomonth 	:      월
    //		  int in_today   	:      일
    //  Outpt : log : 날수
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    '''
    def getDayByDays(self, in_fromyear, in_frommonth, in_fromday, in_toyear, in_tomonth, in_today):
        lCalcYear1 = 0
        lCalcYear2 = 0
        #
        if in_toyear > in_fromyear:
            lToCnt = self.getDayOfDate(in_toyear, in_tomonth, in_today)
            lFromCnt = self.getDayOfDate(in_fromyear, in_frommonth, in_fromday)
            lToTotalCnt = self.getDayOfDate(in_fromyear, 12, 31)
            lCompareYear1 = in_fromyear
            lCompareYear2 = in_toyear
            pr = -1
        else:
            lFromCnt = self.getDayOfDate(in_toyear, in_tomonth, in_today)
            lToTotalCnt = self.getDayOfDate(in_toyear, 12, 31)
            lToCnt = self.getDayOfDate(in_fromyear, in_frommonth, in_fromday)
            lCompareYear1 = in_toyear
            lCompareYear2 = in_fromyear
            pr = +1

        if in_toyear == in_fromyear:
            lTotalDayCnt = lToCnt - lFromCnt
        else:
            lTotalDayCnt = lToTotalCnt - lFromCnt
            lCalcYear1 = lCompareYear1 + 1
            lCalcYear2 = lCompareYear2 - 1

            i = lTotalDayCnt

            while lCalcYear1 <= lCalcYear2:
                if (lCalcYear1 == -9000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 4014377
                elif (lCalcYear1 == -8000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 3649135
                elif (lCalcYear1 == -7000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 3283893
                elif (lCalcYear1 == -6000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 2918651
                elif (lCalcYear1 == -5000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 2553408
                elif (lCalcYear1 == -4000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 2188166
                elif (lCalcYear1 == -3000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1822924
                elif (lCalcYear1 == -2000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1457682
                elif (lCalcYear1 == -1750) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1366371
                elif (lCalcYear1 == -1500) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1275060
                elif (lCalcYear1 == -1250) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1183750
                elif (lCalcYear1 == -1000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1092439
                elif (lCalcYear1 == -750) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 1001128
                elif (lCalcYear1 == -500) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 909818
                elif (lCalcYear1 == -250) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 818507
                elif (lCalcYear1 == 0) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 727197
                elif (lCalcYear1 == 250) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 635887
                elif (lCalcYear1 == 500) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 544576
                elif (lCalcYear1 == 750) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 453266
                elif (lCalcYear1 == 1000) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 361955
                elif (lCalcYear1 == 1250) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 270644
                elif (lCalcYear1 == 1500) and (lCalcYear2 > 1990):
                        lCalcYear1 = 1991
                        i = i + 179334
                elif (lCalcYear1 == 1750) and (lCalcYear2 > 1990):
                    lCalcYear1 = 1991
                    i = i + 88023

                i = i + self.getDayOfDate(lCalcYear1, 12, 31)
                lCalcYear1 = lCalcYear1 + 1

            lTotalDayCnt = i
            lTotalDayCnt = lTotalDayCnt + lToCnt
            lTotalDayCnt = lTotalDayCnt * pr

        return lTotalDayCnt
    '''
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    // Name: getMinByTimes
    // Desc: 특점시점에서 특정시점까지의 분 계산
    // Input: int in_fromyear  : 시작 년
    //			 int in_frommonth 	:      월
    //			 int in_fromday   	:      일
    //			 int in_fromhor	:	   시
    //			 int in_frommin		:	   분
    //           int in_toyear  	: 종료 년
    //			 int in_tomonth 	:      월
    //			 int in_today   	:      일
    //			 int in_tohour		:	   시
    //			 int in_tomin		:	   분
    //  Outpt : log : 분 수
    / /= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    '''
    def getMinByTimes(self, in_fromyear, in_frommonth, in_fromday, in_fromhour, in_frommin, in_toyear, in_tomonth, in_today, in_tohour, in_tomin):
        lDayCnt = self.getDayByDays(in_fromyear, in_frommonth, in_fromday, in_toyear, in_tomonth, in_today)
        lTotalCnt = lDayCnt * 24 * 60 + (in_fromhour - in_tohour) * 60 + (in_frommin - in_tomin)

        # time1 = datetime(int(in_fromyear), int(in_frommonth), int(in_fromday), int(in_fromhour), int(in_frommin))
        # time2 = datetime(int(in_toyear), int(in_tomonth), int(in_today), int(in_tohour), int(in_tomin))
        #
        # lTotalCnt = int((time1 - time2).seconds / 60)

        return lTotalCnt
    '''
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    // Name: getDate2Min
    // Desc: 특정시점으로부터 in_mincnt 떨어진 날짜를 계산
    // Input: long in_mincnt: 분 수
    // int in_year  : 특정 년
    //			 it in_month 	:      월
    //			 it in_day   	:      일
    //			 it in_hor	    :	   시
    //			 it in_min		:	   분
    //  Outpt : it out_year  	:   계산된 년
    //			 it out_month 	:        월
    //			 it out_day   	:        일
    //			 it out_hor	    :	     시
    //			 it out_mn	    :	     분
    / /= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    '''
    # def getDate2Min(self, in_mincnt, in_year, in_month, in_day, in_hour, in_min, out_year, out_month, out_day, out_hour, out_min):
    def getDate2Min(self, in_mincnt, in_year, in_month, in_day, in_hour, in_min):
        out_year = int(in_year - (in_mincnt / 525949))
        out_month = 0

        # time1 = datetime(int(in_year), int(in_month), int(in_day), int(in_hour), int(in_min))
        # time1 = time1 + timedelta(minutes=in_mincnt)
        #
        # int(time1.year)
        #
        # out_year = 0
        # out_month = int(time1.month)
        # out_day = int(time1.day)
        # out_hour = int(time1.hour)
        # out_min = int(time1.minute)

        if in_mincnt >= 0:
            out_year = out_year + 2

            out_year = out_year - 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, 1, 1, 0, 0)

            while lMinCnt < in_mincnt:
                out_year = out_year - 1
                lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, 1, 1, 0,0)


            out_month = 13

            out_month = out_month - 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, out_month, 1, 0, 0)

            while lMinCnt < in_mincnt:
                out_month = out_month - 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, 1, 0,0)

            out_day = 32
            out_day = out_day - 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, out_month, out_day, 0, 0)
            while lMinCnt < in_mincnt:
                out_day = out_day - 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, out_day, 0, 0)


            out_hour = 24
            while lMinCnt < in_mincnt:
                out_hour = out_hour - 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, out_day, out_hour, 0)


            lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, out_day, out_hour, 0)
            out_min = lMinCnt - in_mincnt
        else:
            out_year = out_year - 2

            out_year = out_year + 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, 1, 1, 0, 0)

            while lMinCnt < in_mincnt:
                out_year = out_year + 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, 1, 1, 0,0)


            out_year = out_year - 1

            out_month = out_month + 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, out_month, 1, 0, 0)

            out_month = 0
            while lMinCnt < in_mincnt:
                out_month = out_month + 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year,out_month, 1, 0,0)

            out_month = out_month - 1

            out_day = 0

            out_day = out_day + 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, out_month, out_day, 0, 0)

            while lMinCnt < in_mincnt:
                out_day = out_day + 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, out_day, 0,0)

            out_day = out_day - 1

            out_hour = -1

            out_hour = out_hour + 1
            lMinCnt = self.getMinByTimes(in_year, in_month, in_day, in_hour, in_min, out_year, out_month, out_day, out_hour, 0)

            while lMinCnt < in_mincnt:
                out_hour = out_hour + 1
                lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, out_day, out_hour, 0)

            out_hour = out_hour - 1;

            lMinCnt = self.getMinByTimes(in_year,in_month,in_day,in_hour,in_min, out_year, out_month, out_day, out_hour, 0)
            out_min = lMinCnt - in_mincnt

        return out_year, out_month, out_day, out_hour, out_min
    '''
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    // Name: makeGanji
    // Desc: 양력생일을 이용하여 사주간지 추출
    // Input: int in_syear: 계산할 양력 년
    // int in_smonth: 월
    // int in_sday :			  일
    //			 int in_shour	:			  시
    //			 int in_smin	:			  분
    //  Output : int *out_GanjiYear: 계산한 간지 년
    // int * out_GanjiMonth: 월
    // int * out_GanjiDay: 일
    // int * out_GanjiHour: 시
    //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    '''
    def makeGanji(self, in_syear=None, in_smonth=None, in_sday=None, in_shour=None, in_smin=None):
        # 양력생일의 인풋이 없을경우 멤버 변수의 양력생일를 사용한다.

        if in_syear is None:
            in_syear = self.me_year

        if in_smonth is None:
            in_smonth = self.me_month

        if in_sday is None:
            in_sday = self.me_day

        if in_shour is None:
            in_shour = self.me_hour

        if in_smin is None:
            in_smin = self.me_min

        lMinCnt = self.getMinByTimes(self.m_unityear, self.m_unitmonth, self.m_unitday, self.m_unithour, self.m_unitmin, in_syear, in_smonth, in_sday, in_shour, in_smin)
        lDayCnt = self.getDayByDays(self.m_unityear, self.m_unitmonth, self.m_unitday, in_syear, in_smonth, in_sday)
        so24 = int(lMinCnt / 525949)  # 무인년(1996) 입춘시점부터 해당일시까지 경과년수

        if lMinCnt >= 0:
            so24 = so24 + 1

        out_GanjiYear = -1 * (so24 % 60)
        out_GanjiYear = out_GanjiYear + 12

        if out_GanjiYear < 0:
           out_GanjiYear = out_GanjiYear + 60
        if out_GanjiYear > 59:
           out_GanjiYear = out_GanjiYear - 60 # 년주 구함 끝

        monthmin100 = lMinCnt % 525949
        monthmin100 = 525949 - monthmin100

        if monthmin100 < 0:
            monthmin100 = monthmin100 + 525949
        if monthmin100 >= 525949:
            monthmin100 = monthmin100 - 525949

        for i in range(0, 12):
            j = i * 2
            if (self.naMonthTable[j] <= monthmin100) and (monthmin100 < self.naMonthTable[j + 2]):
               out_GanjiMonth = i

        i = out_GanjiMonth
        t = out_GanjiYear % 10
        t = t % 5
        t = t * 12 + 2 + i
        out_GanjiMonth = t

        if out_GanjiMonth > 59:
           out_GanjiMonth = out_GanjiMonth - 60  # 월주 구함 끝

        out_GanjiDay = lDayCnt % 60
        out_GanjiDay = -1 * out_GanjiDay
        out_GanjiDay = out_GanjiDay + 7

        if out_GanjiDay < 0:
           out_GanjiDay = out_GanjiDay + 60
        if out_GanjiDay > 59:
           out_GanjiDay = out_GanjiDay - 60  # 일주 구함 끝

        nHourMin = in_shour * 100 + in_smin
        if (nHourMin >= 0) and (nHourMin < 130):
            i = 0
        if (nHourMin >= 130) and (nHourMin < 330):
            i = 1
        if (nHourMin >= 330) and (nHourMin < 530):
            i = 2
        if (nHourMin >= 530) and (nHourMin < 730):
            i = 3
        if (nHourMin >= 730) and (nHourMin < 930):
            i = 4
        if (nHourMin >= 930) and (nHourMin < 1130):
            i = 5
        if (nHourMin >= 1130) and (nHourMin < 1330):
            i = 6
        if (nHourMin >= 1330) and (nHourMin < 1530):
            i = 7
        if (nHourMin >= 1530) and (nHourMin < 1730):
            i = 8
        if (nHourMin >= 1730) and (nHourMin < 1930):
            i = 9
        if (nHourMin >= 1930) and (nHourMin < 2130):
            i = 10
        if (nHourMin >= 2130) and (nHourMin < 2330):
            i = 11
        if nHourMin >= 2330:
            out_GanjiDay = out_GanjiDay + 1
            if out_GanjiDay == 60:
               out_GanjiDay = 0
            i = 0

        t = out_GanjiDay % 10
        t = t % 5
        t = t * 12 + i
        out_GanjiHour = t  # 시주 구함 끝

        self.m_GanjiYear = math.ceil(out_GanjiYear)
        self.m_GanjiMonth = math.ceil(out_GanjiMonth)
        self.m_GanjiDay = math.ceil(out_GanjiDay)
        self.m_GanjiHour = math.ceil(out_GanjiHour)

        return self.m_GanjiYear, self.m_GanjiMonth, self.m_GanjiDay, self.m_GanjiHour
    # //======================================================================
    # //  Name   : getGanji
    # //  Desc   : 양력생년월일을 이용하여 사주명을 추출
    # //  Input  : None
    # //  Output : char *out_ganjiyear  : 연간지명
    # //			 char *out_ganjimonth : 월간지명
    # //			 char *out_ganjiday   : 일간지명
    # //			 char *out_ganjihour  : 시간지명
    # //======================================================================

    def getGanji(self):
        self.makeGanji()
        out_ganjiyear = self.caGanjiTable[self.m_GanjiYear]
        out_ganjimonth = self.caGanjiTable[self.m_GanjiMonth]
        out_ganjiday = self.caGanjiTable[self.m_GanjiDay]
        out_ganjihour = self.caGanjiTable[self.m_GanjiHour]
        return out_ganjiyear, out_ganjimonth, out_ganjiday, out_ganjihour, self.m_GanjiYear, self.m_GanjiMonth, self.m_GanjiDay, self.m_GanjiHour

    def get_ganji(self, year, month, day, hour, min):
        yyyy = int(year)
        mm = int(month)
        dd = int(day)
        hh = int(hour)
        M = int(min)

        self.makeGanji(in_syear=yyyy, in_smonth=mm, in_sday=dd, in_shour=hh, in_smin=M)
        out_ganjiyear = self.caGanjiTable[self.m_GanjiYear]
        out_ganjimonth = self.caGanjiTable[self.m_GanjiMonth]
        out_ganjiday = self.caGanjiTable[self.m_GanjiDay]
        out_ganjihour = self.caGanjiTable[self.m_GanjiHour]
        return out_ganjiyear, out_ganjimonth, out_ganjiday, out_ganjihour, self.m_GanjiYear, self.m_GanjiMonth, self.m_GanjiDay, self.m_GanjiHour

    def now_getGanji(self):
        yyyy = int(datetime.today().strftime('%Y'))
        mm = int(datetime.today().strftime('%m'))
        dd = int(datetime.today().strftime('%d'))
        hh = int(datetime.today().strftime('%H'))
        M = int(datetime.today().strftime('%M'))

        self.makeGanji(in_syear=yyyy, in_smonth=mm, in_sday=dd, in_shour=hh, in_smin=M)
        out_ganjiyear = self.caGanjiTable[self.m_GanjiYear]
        out_ganjimonth = self.caGanjiTable[self.m_GanjiMonth]
        out_ganjiday = self.caGanjiTable[self.m_GanjiDay]
        out_ganjihour = self.caGanjiTable[self.m_GanjiHour]
        return out_ganjiyear, out_ganjimonth, out_ganjiday, out_ganjihour, self.m_GanjiYear, self.m_GanjiMonth, self.m_GanjiDay, self.m_GanjiHour
    # # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # # // Name: get24terms
    # # // Desc: 기 지정한 양력생년월일이 들어있는 시작절기, 중기 다음절기 추출
    # # // Input: int in_type: PREV_24TERMS(시작절기), MID_24TERMS(중기), NEXT_24TERMS(다음절기)
    # # // Output: char * out_year: 해당 절기 년
    # # // char * out_month: 월
    # # // char * out_day: 일
    # # // char * out_hour: 시
    # # // int			: 해당 절기의 ca24TermsTabl 상의 array
    # # //===== == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # def get24terms(self, in_type):
    #     i = 0
    #     monthmin100 = 0
    #     j = 0
    #     tmin = 0
    #     lMinCnt = 0
    #     y = 0
    #     mo = 0
    #     d = 0
    #     h = 0
    #     mi = 0
    #     n24terms = 0
    #
    #     if self.m_GanjiMonth == -1:
    #         self.makeGanji()
    #
    #     lMinCnt = self.getMinByTimes(self.m_unityear, self.m_unitmonth, self.m_unitday, self.m_unithour, self.m_unitmin, self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min)
    #
    #     monthmin100 = lMinCnt % 525949
    #     monthmin100 = 525949 - monthmin100
    #
    #     if monthmin100 <  0:
    #         monthmin100 = monthmin100 + 525949
    #     if monthmin100 >= 525949:
    #         monthmin100 = monthmin100 - 525949
    #
    #     i = self.m_GanjiMonth % 12 - 2
    #
    #     if i == -2:
    #         i = 10
    #
    #     if i == -1:
    #         i = 11
    #
    #
    #     n24terms = i * 2 + in_type
    #     out_terms24 = self.ca24TermsTable[n24terms]
    #
    #     j = i * 2 + in_type
    #     tmin =  lMinCnt + (monthmin100 - self.naMonthTable[j])
    #     self.getDate2Min(tmin ,self.m_unityear ,self.m_unitmonth ,self.m_unitday ,self.m_unithour ,self.m_unitmin)
    #
    #     out_year = y
    #     out_month = mo
    #     out_day = d
    #     out_hour = h
    #     out_min = mi
    #
    #     return n24terms, out_terms24, out_year, out_month, out_day, out_hour, out_min

    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: get24terms
    # // Desc: 특정일자가 들어있는 시작절기, 중기 다음절기 추출
    # // Input: int in_syear: 특정 년
    # // int in_smonth: 월
    # // int in_sday: 일
    # // int in_shour: 시
    # // int in_smin: 분
    # // int in_type : PREV_24TERMS(시작절기), MID_24TERMS(중기), NEXT_24TERMS(다음절기)
    # //  Output : char *out_year: 해당 절기 년
    # // char * out_month: 월
    # // char * out_day: 일
    # // char * out_hour: 시
    # // int			: 해당 절기의 ca24TermsTabl 상의 array
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    def get24terms(self, in_syear, in_smonth, in_sday, in_shour, in_smin, in_type):
        lMinCnt = self.getMinByTimes(self.m_unityear, self.m_unitmonth, self.m_unitday, self.m_unithour, self.m_unitmin, in_syear, in_smonth, in_sday, in_shour, in_smin)

        monthmin100 = lMinCnt % 525949
        monthmin100 = 525949 - monthmin100

        if monthmin100 < 0:
            monthmin100 = monthmin100 + 525949
        if monthmin100 >= 525949:
            monthmin100 = monthmin100 - 525949

        i = self.m_GanjiMonth % 12 - 2
        if i == -2:
            i = 10
        if i == -1:
            i = 11

        n24terms = i * 2 + in_type
        out_terms24 = self.ca24TermsTable[n24terms]

        print("n24terms", n24terms)
        j = i * 2 + in_type
        tmin = int(lMinCnt + (monthmin100 - self.naMonthTable[j]))
        y, mo, d, h, mi = self.getDate2Min(tmin, self.m_unityear, self.m_unitmonth, self.m_unitday, self.m_unithour, self.m_unitmin)
        # y, mo, d, h, mi = self.getDate2Min(tmin, in_syear, in_smonth, in_sday, in_shour, in_smin)

        return n24terms, out_terms24, int(y), int(mo), int(d), int(h), int(mi)
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: Solar2Lunar
    # // Desc: 그레고리력 년월일 --> 태음태양력 년, 월, 일, 평 / 윤
    # // Input: int in_syear: 특정 양력 년
    # // int in_smonth: 월
    # // int in_sday: 일
    # // Output: char * out_lyear: 음력 년
    # // char * out_lmonth: 월
    # // char * out_lday: 일
    # // bool * out_lmoonyun: true(윤달), false(평달)
    # // bool			: true( 변환 가능), false (변환 오류 )
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =====

    def SolarToLunar(self, in_syear, in_smonth, in_sday):
        out_lyear = 0
        out_lmonth = 0
        out_lday = 0
        out_lmoonyun = 0

        if in_syear < 1881 or in_syear > 2043:
            return False, out_lyear, out_lmonth, out_lday, out_lmoonyun

        laDayCnt = None
        for i in range(0, 163):
            for j in range(0, 13):
                if self.caYearTable[i][j] == '0' or self.caYearTable[i][j] == '1' or self.caYearTable[i][j] == '3':
                    laDayCnt[i] += 29
                elif self.caYearTable[i][j] == '2' or self.caYearTable[i][j] == '4':
                    laDayCnt[i] += 30
                else:
                    return False, out_lyear, out_lmonth, out_lday, out_lmoonyun

        # 1880년 1월 30일까지의 총일수
        # lTotalDay1 = (1880 * 365) + (1880 / 4) - (1880 / 100) + (1880 / 400) + 30
        lTotalDay1 = 686685
        nBeforeYear = in_syear - 1
        # 입력된 년도 1년전까지의 총일수
        lTotalDay2 = nBeforeYear * 365 + nBeforeYear / 4 - nBeforeYear / 100 + nBeforeYear / 400

        if ((in_syear % 400) == 0) or ((in_syear % 100) != 0) and ((in_syear % 4) == 0):
            self.naDayPerMonthTable[1] = 29
        else:
            self.naDayPerMonthTable[1] = 28

        for i in range(0, in_smonth):
            lTotalDay2 = lTotalDay2 + self.naDayPerMonthTable[i]

        # 입력된 일자까지의 총일수
        lTotalDay2 = lTotalDay2 + in_sday

        # 1880-01-30 부터 현재까지의 총일수
        lTotalDay = lTotalDay2 - lTotalDay1  # + 1

        # 1881년부터 현재까지의 총일수와 Table상의 숫자(음력)들의 합을 비교 반복
        lTotalDay0 = laDayCnt[0]
        for i in range(0, 163):
            if lTotalDay <= lTotalDay0:
                break
            lTotalDay0 = lTotalDay0 + laDayCnt[i + 1]

        # 음력년도
        nLunYear = i + 1880 + 1

        out_lyear = nLunYear

        # 현재년도의 음력일수 감산
        lTotalDay0 = lTotalDay0 - laDayCnt[i]
        # 양력 총일수에서 음력 총일수 감산
        lTotalDay  = lTotalDay - lTotalDay0

        if self.caYearTable[i][12] == '0':
            nCount = 12
        else:
            nCount = 13

        m2 = 0
        for j in range(0, nCount):
            if self.caYearTable[i][j] <= '2':
                m2 = m2 +1
                m1 = self.caYearTable[i ] [j]  - '0' + 28
            else:
                m1 = self.caYearTable[i][j] - '0' + 26

            if lTotalDay <= m1:
                break
            lTotalDay = lTotalDay - m1

        # 음력일자 \ \
        out_lmonth = m2
        out_lday = lTotalDay

        # 윤달 여부 판단
        if self.caYearTable[nLunYear-1881][12] != '0' and self.caYearTable[nLunYear-1881][j] > '2':
            out_lmoonyun = True
        else:
            out_lmoonyun = False

        return True, out_lyear, out_lmonth, out_lday, out_lmoonyun
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: Solar2Lunar
    # // Desc: 기 입력된 년월일 --> 태음태양력 년, 월, 일, 평 / 윤
    # // Input: None
    # // Output: char * out_lyear: 음력 년
    # // char * out_lmonth: 월
    # // char * out_lday: 일
    # // bool * out_lmoonyun: true(윤달), false(평달)
    # // bool			: true(변환 가능), false (변환 오류 )
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =====

    def Solar2Lunar(self):

        ret, out_lyear, out_lmonth, out_lday, out_lmoonyun = self.SolarToLunar(self.me_year, self.me_month, self.me_day)

        return ret, out_lyear, out_lmonth, out_lday, out_lmoonyun
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: Lunar2Solar
    # // Desc: 태음태양력 년월일 --> 그레고리력 년월일
    # // Input: int in_lyear: 특정 음력 년
    # // int in_lmonth: 월
    # // int in_lday: 일
    # // Output: char * out_syear: 양력 년
    # // char * out_smonth: 월
    # // char * out_sday: 일
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    def lunar_to_solar(self, in_lyear, in_lmonth, in_lday):
        j = in_lmonth - 1

        for i in range(0, 13):
            if int(self.caYearTable[in_lyear - 1880 - 1][i]) > 2:
                j = j + 1

        m1 = 0
        td = 0

        # 구하는 일자까지의 날짜를 더함
        if in_lyear != 1881:
            m1 = in_lyear - 1881
            for i in range(0, m1):
                for j in range(0, 13):
                    td = td + (int(self.caYearTable[i][j]) - 0)

                if int(self.caYearTable[i][12]) == 0:
                    td = td + 336
                else:
                    td = td + 362  # 윤월

        n2 = in_lmonth
        m2 = 0

        while True:
            if int(self.caYearTable[m1][m2]) > 2:
                td = td + 26 + (int(self.caYearTable[m1][m2]) - 0)
                n2 = n2 + 1
            elif (m2 + 1) == n2:
                break
            else:
                td = td + 28 + (int(self.caYearTable[m1][m2]) - 0)
            m2 = m2 + 1

        td = td + in_lday + 29
        m1 = 1880

        while True:
            # 1 년씩 윤년을 구분하여 날수를 뺌
            m1 = m1 + 1
            if ((m1 % 400) == 0) or ((m1 % 100) != 0) and ((m1 % 4) == 0):
                leap = 1
            else:
                leap = 0

            if leap == 1:
                m2 = 366
            else:
                m2 = 365

            if td < m2:
                break
            td = td - m2

        out_syear = m1  # 구하는 일자의 해
        self.naDayPerMonthTable[1] = m2 - 337  # 구하는 일자의 2월의 날짜
        m1 = 0

        #= 달과 일을 구함
        while True:
            if td <= self.naDayPerMonthTable[m1]:
                break
            td = td - self.naDayPerMonthTable[m1]
            m1 = m1 + 1

        out_smonth = m1 + 1
        out_sday = td

        return out_syear, out_smonth, out_sday
    # //======================================================================
    # //  Name   : Lunar2Solar
    # //  Desc   : 기 입력된 년월일 --> 그레고리력 년월일
    # //  Input  : None
    # //  Output : char *out_syear  : 양력 년
    # //		   char *out_smonth : 	 월
    # //		   char *out_sday   : 	 일
    # //======================================================================
    def set_me_lunar_to_solar(self):
        out_syear, out_smonth, out_sday = self.lunar_to_solar(self.me_year, self.me_month, self.me_day);
        self.me_year = out_syear
        self.me_month = out_smonth
        self.me_day = out_sday
        return out_syear, out_smonth, out_sday
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getWeekname
    # // Desc: 기 입력된 년월일의 요일 구하기(필요에 따라 특정일자에 대한 기능으로 변경 / 추가 가능)
    # // Input: None
    # // Output: char * out_name: 요일
    # // int 		: caWeeknameTabl 상의 해당 array(일요일 : 0)
    # / /= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =====
    def getWeekname(self):
        d = self.getDayByDays(self.me_year, self.me_month, self.me_day, self.m_unityear, self.m_unitmonth, self.m_unitday)
        i = d / 7
        d = d - (i * 7)

        while (d > 6) or (d < 0):
            if d > 6:
                d = d - 7
            else:
                d = d + 7

            if d < 0:
                d = d + 7
        out_name = self.caWeeknameTable[d]

        return d, out_name
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getOheng
    # // Desc: 기 입력된 생년월일시분을 이용해서 오행값, 신강 / 신약을 추출
    # // Input: None
    # // Output: double * out_woodNum : 오행중 목의 값
    # //			 double *out_fireNum : 오행중 불의 값
    # //			 double *out_groundNum: 오행중 토의 값
    # // double * out_goldNum: 오행중 금의 값
    # // double * out_waterNum : 오행중 물의 값
    # //			 int					: true(신강), false(신약), -1(계산 실패)
    # // == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
    def getOheng(self):

        if self.m_GanjiYear == -1:
            self.makeGanji()

        siGan = self.m_GanjiHour % 10 # 시간을 구한다.
        siJi = self.m_GanjiHour % 12 # 시지를 구한다.
        ilGan = self.m_GanjiDay % 10 # 일간을 구한다.
        ilJi = self.m_GanjiDay % 12 # 일지를 구한다.
        wolGan = self.m_GanjiMonth % 10 # 월간을 구한다.
        wolJi = self.m_GanjiMonth % 12 # 월지를 구한다.
        nyunGan = self.m_GanjiYear % 10 # 년간을 구한다.
        nyunJi = self.m_GanjiYear % 12 # 년지를 구한다.

        woodNum = fireNum = groundNum = goldNum = waterNum = 0.0
        # '간에 해당하는 숫자
        for i in range(0, 3):
            if i == 0:
                baseGan = siGan
                baseValue = 0.2
            elif i == 1:
                baseGan = wolGan
                baseValue = 0.25
            else:
                baseGan = nyunGan
                baseValue = 0.2

            if baseGan == 0 or baseGan == 1: # 목
                woodNum = woodNum + baseValue
            elif baseGan == 2 or baseGan == 3: # 화
                fireNum = fireNum + baseValue
            elif baseGan == 4 or baseGan == 5:  # 토
                groundNum = groundNum + baseValue
            elif baseGan == 6 or baseGan == 7:  # 금
                goldNum = goldNum + baseValue
            elif baseGan == 8 or baseGan == 9:  # 수
                waterNum = waterNum + baseValue

        #// '지에 해당하는 숫자
        #// '자축인묘진사오미신유술해
        #// '0 1 2 3 4 5 6 7 8 9 1011
        #// '4, 10, 1, 7(진술축미)
        for i in range(0, 4):
            if i == 0:
                baseJi = siJi
            elif i == 1:
                baseJi = ilJi
            elif (i == 2):
                baseJi = wolJi
            else:
                baseJi = nyunJi

            if baseJi == 0 or baseJi == 11:
                waterNum = waterNum + 1
            elif baseJi == 1: # 축 토 진술축미에 해당하는 부분이다.
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    if (i == 1): # 일지
                        waterNum = waterNum + 0.5 + 1
                    else: # 시지, 월지, 년지
                        waterNum = waterNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    if i == 0: # 시지
                        waterNum = waterNum + 0.3 # + 1
                        groundNum = groundNum + 0.7 + 1
                    elif i == 1: # 일지
                        waterNum = waterNum + 0.3 + 1
                        groundNum = groundNum + 0.7 # + 1
                    else: # 월지, 년지
                        waterNum = waterNum + 0.3 # + 1
                        groundNum = groundNum + 0.7 # + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    if i == 0: # 시지
                        waterNum = waterNum + 0.5 # + 1
                        groundNum = groundNum + 0.5 + 1
                    elif i == 1: # 일지
                        waterNum = waterNum + 0.5 + 1
                        groundNum = groundNum + 0.5 # + 1
                    else: # 월지, 년지
                        waterNum = waterNum + 0.5 # + 1
                        groundNum = groundNum + 0.5 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    if i == 0: # 시지
                        waterNum = waterNum + 0.7 # + 1
                        groundNum = groundNum + 0.3 + 1

                    elif i == 1: # 일지
                        waterNum = waterNum + 0.7 + 1
                        groundNum = groundNum + 0.3 # + 1
                    else: # 월지, 년지
                        waterNum = waterNum + 0.7 # + 1
                        groundNum = groundNum + 0.3 # + 1
            elif baseJi == 4:
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    woodNum = woodNum + 0.7 # + 1
                    groundNum = groundNum + 0.3 # + 1
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    woodNum = woodNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    woodNum = woodNum + 0.3 # + 1
                    groundNum = groundNum + 0.7 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    woodNum = woodNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
            elif baseJi == 7: # '미
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    fireNum = fireNum + 0.5
                    groundNum = groundNum + 0.5
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    fireNum = fireNum + 0.7 # + 1
                    groundNum = groundNum + 0.3 # + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    fireNum = fireNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    fireNum = fireNum + 0.3 # + 1
                    groundNum = groundNum + 0.7 # + 1
            elif baseJi == 10: # '술
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    goldNum = goldNum + 0.3 # + 1
                    groundNum = groundNum + 0.7 # + 1
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    goldNum = goldNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    goldNum = goldNum + 0.7 # + 1
                    groundNum = groundNum + 0.3 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    goldNum = goldNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif baseJi == 2 or baseJi == 3:
                    woodNum = woodNum + 1;
                elif baseJi == 5 or baseJi == 6:
                    fireNum = fireNum + 1;
                elif baseJi == 8 or baseJi == 9:
                    goldNum = goldNum + 1;

        # // printf("\n%d, wood=%f, fire=%f, ground=%f, gold=%f, water=%f",
        # // i, woodNum, fireNum, groundNum, goldNum, waterNum);


        out_woodNum = woodNum;
        out_fireNum = fireNum;
        out_groundNum = groundNum;
        out_goldNum = goldNum;
        out_waterNum = waterNum;

        # // '신강과 신약을 구한다. 일간의 오행이 1.21이거나 일간을 생하는 숫자가 1.21이 넘으면
        # // '신강이고 아니면 신약이다.
        # // '생하는 관계는 수->목->화->토->금이다.

        if ilGan == 0 or ilGan == 0: # 목
            il_Num = woodNum
            il_LiveNum = waterNum
        elif ilGan == 2 or ilGan == 3: # 화
            il_Num = fireNum
            il_LiveNum = woodNum
        elif ilGan == 4 or ilGan == 5: # 토
            il_Num = groundNum
            il_LiveNum = fireNum
        elif ilGan == 6 or ilGan == 7: # 금
            il_Num = goldNum
            il_LiveNum = groundNum
        elif ilGan == 8 or ilGan == 9:  # 수
            il_Num = waterNum;
            il_LiveNum = goldNum;

        if (il_Num + 1.5 >= 2.71) or (il_LiveNum >= 2.71): # 신강
            nStrong = True
        elif (il_Num + 1.5 < 2.71) or (il_LiveNum < 2.71): # 신약
            nStrong = False
        else:
            nStrong = -1

        return nStrong, out_woodNum, out_fireNum, out_groundNum, out_goldNum, out_waterNum

    def getOheng_A(self, m_GanjiYear, m_GanjiMonth, m_GanjiDay, m_GanjiHour):
        siGan = m_GanjiHour % 10 # 시간을 구한다.
        siJi = m_GanjiHour % 12 # 시지를 구한다.
        ilGan = m_GanjiDay % 10 # 일간을 구한다.
        ilJi = m_GanjiDay % 12 # 일지를 구한다.
        wolGan = m_GanjiMonth % 10 # 월간을 구한다.
        wolJi = m_GanjiMonth % 12 # 월지를 구한다.
        nyunGan = m_GanjiYear % 10 # 년간을 구한다.
        nyunJi = m_GanjiYear % 12 # 년지를 구한다.

        woodNum = 0.0
        fireNum = 0.0
        groundNum = 0.0
        goldNum = 0.0
        waterNum = 0.0

        # '간에 해당하는 숫자
        for i in range(0, 3):
            if i == 0:
                baseGan = siGan
                baseValue = 0.2
            elif i == 1:
                baseGan = wolGan
                baseValue = 0.25
            else:
                baseGan = nyunGan
                baseValue = 0.2

            if baseGan == 0 or baseGan == 1: # 목
                woodNum = woodNum + baseValue
            elif baseGan == 2 or baseGan == 3: # 화
                fireNum = fireNum + baseValue;
            elif baseGan == 4 or baseGan == 5:  # 토
                groundNum = groundNum + baseValue
            elif baseGan == 6 or baseGan == 7:  # 금
                goldNum = goldNum + baseValue
            elif baseGan == 8 or baseGan == 9:  # 수
                waterNum = waterNum + baseValue


        #// '지에 해당하는 숫자
        #// '자축인묘진사오미신유술해
        #// '0 1 2 3 4 5 6 7 8 9 1011
        #// '4, 10, 1, 7(진술축미)
        for i in range(0, 4):
            if i == 0:
                baseJi = siJi
            elif i == 1:
                baseJi = ilJi
            elif (i == 2):
                baseJi = wolJi
            else:
                baseJi = nyunJi

            if baseJi == 0 or baseJi == 11:
                waterNum = waterNum + 1
            elif baseJi == 1: # 축 토 진술축미에 해당하는 부분이다.
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    if (i == 1): # 일지
                        waterNum = waterNum + 0.5 + 1
                    else: # 시지, 월지, 년지
                        waterNum = waterNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    if i == 0: # 시지
                        waterNum = waterNum + 0.3 # + 1
                        groundNum = groundNum + 0.7 + 1
                    elif i == 1: # 일지
                        waterNum = waterNum + 0.3 + 1
                        groundNum = groundNum + 0.7 # + 1
                    else: # 월지, 년지
                        waterNum = waterNum + 0.3 # + 1
                        groundNum = groundNum + 0.7 # + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    if i == 0: # 시지
                        waterNum = waterNum + 0.5 # + 1
                        groundNum = groundNum + 0.5 + 1
                    elif i == 1: # 일지
                        waterNum = waterNum + 0.5 + 1
                        groundNum = groundNum + 0.5 # + 1
                    else: # 월지, 년지
                        waterNum = waterNum + 0.5 # + 1
                        groundNum = groundNum + 0.5 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    if i == 0: # 시지
                        waterNum = waterNum + 0.7 # + 1
                        groundNum = groundNum + 0.3 + 1

                    elif i == 1: # 일지
                        waterNum = waterNum + 0.7 + 1
                        groundNum = groundNum + 0.3 # + 1
                    else: # 월지, 년지
                        waterNum = waterNum + 0.7 # + 1
                        groundNum = groundNum + 0.3 # + 1
            elif baseJi == 4:
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    woodNum = woodNum + 0.7 # + 1
                    groundNum = groundNum + 0.3 # + 1
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    woodNum = woodNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    woodNum = woodNum + 0.3 # + 1
                    groundNum = groundNum + 0.7 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    woodNum = woodNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
            elif baseJi == 7: # '미
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    fireNum = fireNum + 0.5
                    groundNum = groundNum + 0.5
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    fireNum = fireNum + 0.7 # + 1
                    groundNum = groundNum + 0.3 # + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    fireNum = fireNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    fireNum = fireNum + 0.3 # + 1
                    groundNum = groundNum + 0.7 # + 1
            elif baseJi == 10: # '술
                if wolJi == 2 or wolJi == 3 or wolJi == 4:
                    goldNum = goldNum + 0.3 # + 1
                    groundNum = groundNum + 0.7 # + 1
                elif wolJi == 5 or wolJi == 6 or wolJi == 7:
                    goldNum = goldNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 + 1
                elif wolJi == 8 or wolJi == 9 or wolJi == 10:
                    goldNum = goldNum + 0.7 # + 1
                    groundNum = groundNum + 0.3 # + 1
                elif wolJi == 11 or wolJi == 0 or wolJi == 1:
                    goldNum = goldNum + 0.5 # + 1
                    groundNum = groundNum + 0.5 # + 1
                elif baseJi == 2 or baseJi == 3:
                    woodNum = woodNum + 1;
                elif baseJi == 5 or baseJi == 6:
                    fireNum = fireNum + 1;
                elif baseJi == 8 or baseJi == 9:
                    goldNum = goldNum + 1;
            elif baseJi == 2 or baseJi == 3:  # 목
                woodNum = woodNum + 1
            elif baseJi == 5 or baseJi == 6:  # 목
                fireNum = fireNum + 1;
            elif baseJi == 8 or baseJi == 9:  # 목
                goldNum = goldNum + 1;
        # // printf("\n%d, wood=%f, fire=%f, ground=%f, gold=%f, water=%f",
        # // i, woodNum, fireNum, groundNum, goldNum, waterNum);


        out_woodNum = woodNum;
        out_fireNum = fireNum;
        out_groundNum = groundNum;
        out_goldNum = goldNum;
        out_waterNum = waterNum;

        # // '신강과 신약을 구한다. 일간의 오행이 1.21이거나 일간을 생하는 숫자가 1.21이 넘으면
        # // '신강이고 아니면 신약이다.
        # // '생하는 관계는 수->목->화->토->금이다.
        il_Num = 0
        il_LiveNum = 0
        if ilGan == 0 or ilGan == 0: # 목
            il_Num = woodNum
            il_LiveNum = waterNum
        elif ilGan == 2 or ilGan == 3: # 화
            il_Num = fireNum
            il_LiveNum = woodNum
        elif ilGan == 4 or ilGan == 5: # 토
            il_Num = groundNum
            il_LiveNum = fireNum
        elif ilGan == 6 or ilGan == 7: # 금
            il_Num = goldNum
            il_LiveNum = groundNum
        elif ilGan == 8 or ilGan == 9:  # 수
            il_Num = waterNum;
            il_LiveNum = goldNum;

        if (il_Num + 1.5 >= 2.71) or (il_LiveNum >= 2.71): # 신강
            nStrong = True
        elif (il_Num + 1.5 < 2.71) or (il_LiveNum < 2.71): # 신약
            nStrong = False
        else:
            nStrong = -1

        return nStrong, out_woodNum, out_fireNum, out_groundNum, out_goldNum, out_waterNum

    def getOheng_B(self, type, hh, sky_sum=None, ground_6_sum=None, gorund_3_sum=None, gorund_b_sum=None):
        gabja = []
        print(base_file_path)
        with open(base_file_path.format(type=type), encoding='utf-8') as f:
            rdr = csv.reader(f)
            for row in rdr:
                gabja.append(row)

        oheng = gabja[hh]
        ganji = self.caGanjiTable[hh]
        print("60 갑자 ---->", ganji)

        _sums = []
        # 지지방합 적용
        if type == 'yyyy' or type == 'mm' or type == 'dd' or type == 'hh':
            jiji = ganji[1]
            type_name = ''
            _gorund_b_sum = None
            if type == 'yyyy':
                type_name = '연주'
                _gorund_b_sum = gorund_b_sum['y']
            if type == 'mm':
                type_name = '월주'
                _gorund_b_sum = gorund_b_sum['m']
            if type == 'dd':
                type_name = '일주'
                _gorund_b_sum = gorund_b_sum['d']
            if type == 'hh':
                type_name = '시주'
                _gorund_b_sum = gorund_b_sum['h']

            print('{type_name} ----> 지지방합 확인'.format(type_name=type_name))
            print('지지방합 ---->', _gorund_b_sum)
            print('지지 ---->', jiji)

            if _gorund_b_sum != None:
                if jiji == _gorund_b_sum['k']:
                    _sums.append(_gorund_b_sum)

        # 천간합 적용
        if type == 'dea' or type == 'nyyyy' or type == 'nmm' or type == 'ndd' or type == 'nhh':
            _sky_sum = None
            chun = ganji[0]
            type_name = ''
            _gorund_b_sum = None
            if type == 'dea':
                type_name = '대운'
                _sky_sum = sky_sum['y']

            if type == 'nyyyy':
                type_name = '세운운'
                _sky_sum = sky_sum['y']

            if type == 'nmm':
                type_name = '월운'
                _sky_sum = sky_sum['m']
            if type == 'ndd':
                type_name = '일운'
                _sky_sum = sky_sum['d']
            if type == 'nhh':
                type_name = '시운'
                _sky_sum = sky_sum['h']

            print('{type_name} ----> 천간합 확인'.format(type_name=type_name))
            print('천간합 ---->', _sky_sum)
            print('천간 ---->', chun)

            if _sky_sum != None:
                if chun == _sky_sum['k']:
                    _sums.append(_sky_sum)

        # 지지육합 적용
        if type == 'dea' or type == 'nyyyy' or type == 'nmm' or type == 'ndd' or type == 'nhh':
            _ground_6_sum = None
            jiji = ganji[1]
            type_name = ''
            _gorund_b_sum = None
            if type == 'dea':
                type_name = '대운'
                _ground_6_sum = ground_6_sum['b']

            if type == 'nyyyy':
                type_name = '세운운'
                _ground_6_sum = ground_6_sum['y']

            if type == 'nmm':
                type_name = '월운'
                _ground_6_sum = ground_6_sum['m']
            if type == 'ndd':
                type_name = '일운'
                _ground_6_sum = ground_6_sum['d']
            if type == 'nhh':
                type_name = '시운'
                _ground_6_sum = ground_6_sum['h']

            print('{type_name} ----> 지지육합 확인'.format(type_name=type_name))
            print('지지육합 ---->', _ground_6_sum)
            print('지지 ---->', jiji)

            if _ground_6_sum != None:
                if jiji == _ground_6_sum['k']:
                    _sums.append(_ground_6_sum)

        # 지지삼합 적용
        if type == 'dea' or type == 'nyyyy' or type == 'nmm' or type == 'ndd' or type == 'nhh':
            _gorund_3_sum = None
            jiji = ganji[1]
            type_name = ''
            if type == 'dea':
                type_name = '대운'
                _gorund_3_sum = gorund_3_sum['b']

            if type == 'nyyyy':
                type_name = '세운운'
                _gorund_3_sum = gorund_3_sum['y']

            if type == 'nmm':
                type_name = '월운'
                _gorund_3_sum = gorund_3_sum['m']
            if type == 'ndd':
                type_name = '일운'
                _gorund_3_sum = gorund_3_sum['d']
            if type == 'nhh':
                type_name = '시운'
                _gorund_3_sum = gorund_3_sum['h']

            print('{type_name} ----> 지지삼합 확인'.format(type_name=type_name))
            print('지지삼합 ---->', _gorund_3_sum)
            print('지지 ---->', jiji)

            if _gorund_3_sum != None:
                if jiji == _gorund_3_sum['k']:
                    _sums.append(_gorund_3_sum)

        print('오행합 변환 조건 -----------------> ', _sums)

        wood_change = []
        fire_change = []
        ground_change = []
        gold_change = []
        water_change = []
        for _sum in _sums:
            print(_sums)
            start = _sum['s']
            end = _sum['e']

            if(start == '목'):
                wood_change.append(end)

            if (start == '화'):
                fire_change.append(end)

            if (start == '토'):
                ground_change.append(end)

            if (start == '금'):
                gold_change.append(end)

            if (start == '수'):
                water_change.append(end)

        print('====변환 속성 리스트')
        print('**목속성 변환', wood_change)
        print('**화속성 변환', fire_change)
        print('**토속성 변환', ground_change)
        print('**금속성 변환', gold_change)
        print('**수속성 변환', water_change)
        print('******************')

        wood = 0
        fire = 0
        ground = 0
        gold = 0
        water = 0

        try:

            value = float(oheng[1])
            if len(wood_change) > 0:
                try:
                    change = wood_change[0]
                except:
                    change = ''

                print('목 --------------------------->', change)
                if change == '목':
                    wood = wood + value

                if change == '화':
                    fire = fire + value

                if change == '토':
                    ground = ground + value

                if change == '금':
                    gold = gold + value

                if change == '수':
                    water = water + value
            else:
                wood = wood + value
        except:
            pass

        try:
            value = float(oheng[2])
            if len(fire_change) > 0:
                try:
                    change = fire_change[0]
                except:
                    change = ''

                print('화 --------------------------->', change)
                if change == '목':
                    wood = wood + value

                if change == '화':
                    fire = fire + value

                if change == '토':
                    ground = ground + value

                if change == '금':
                    gold = gold + value

                if change == '수':
                    water = water + value
            else:
                fire = fire + value
        except:
            pass

        try:
            value = float(oheng[3])
            if len(ground_change) > 0:
                try:
                    change = ground_change[0]
                except:
                    change = ''

                print('토 --------------------------->', change)
                if change == '목':
                    wood = wood + value

                if change == '화':
                    fire = fire + value

                if change == '토':
                    ground = ground + value

                if change == '금':
                    gold = gold + value

                if change == '수':
                    water = water + value
            else:
                ground = ground + value
        except:
            pass

        try:
            value = float(oheng[4])
            if len(gold_change) > 0:
                try:
                    change = gold_change[0]
                except:
                    change = ''

                print('금 --------------------------->', change)
                if change == '목':
                    wood = wood + value

                if change == '화':
                    fire = fire + value

                if change == '토':
                    ground = ground + value

                if change == '금':
                    gold = gold + value

                if change == '수':
                    water = water + value
            else:
                gold = gold + value
        except:
            pass

        try:
            value = float(oheng[5])
            if len(water_change) > 0:
                try:
                    change = water_change[0]
                except:
                    change = ''

                print('수 --------------------------->', change)
                if change == '목':
                    wood = wood + value

                if change == '화':
                    fire = fire + value

                if change == '토':
                    ground = ground + value

                if change == '금':
                    gold = gold + value

                if change == '수':
                    water = water + value
            else:
                water = water + value
        except:
            pass

        print(oheng)
        print(wood, fire, ground, gold, water)

        return wood, fire, ground, gold, water

    def getOheng_C(self, type, hh, weight=1):
        gabja = []
        with open(base_file_path.format(type=type), encoding='utf-8') as f:
            rdr = csv.reader(f)
            for row in rdr:
                gabja.append(row)

        oheng = gabja[hh]
        ganji = self.caGanjiTable[hh]
        print("간지:", ganji)

        _sums = []

        wood = 0
        fire = 0
        ground = 0
        gold = 0
        water = 0

        try:
            value = int(float(oheng[1]) * 100) / 100
            wood = wood + value * weight
        except:
            pass

        try:
            value = int(float(oheng[2]) * 100) / 100
            fire = fire + value * weight
        except:
            pass

        try:
            value = int(float(oheng[3]) * 100) / 100
            ground = ground + value * weight
        except:
            pass

        try:
            value = int(float(oheng[4]) * 100) / 100
            gold = gold + value * weight
        except:
            pass

        try:
            value = int(float(oheng[5]) * 100) / 100
            water = water + value * weight
        except:
            pass

        return wood, fire, ground, gold, water
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getJohu
    # // Desc: 기 입력된 생년월일시분을 이용해서 조후용신을 추출
    # // Input: None
    # // Output: char * out_johuname: 추출한 조후용신 명
    # // int			: caGanTab e의 해당 array
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    def getOheng_D(self):
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()
        # print(self.makeGanji())
        _10sin_year = self.get_10sin("year", yeon_ju_idx)
        _10sin_month = self.get_10sin("month", wol_ju_idx)
        _10sin_day = self.get_10sin("day", il_ju_idx)
        _10sin_time = self.get_10sin("time", si_ju_idx)
        saju_dict = [_10sin_year, _10sin_month, _10sin_day, _10sin_time]
        total_10sin_only_saju_score = reduce(lambda a, b: a.update(b) or a, saju_dict, Counter())
        _10sin_score = dict(
            zip(total_10sin_only_saju_score.keys(), map(lambda x: round((x[1] / 110) * 100, 1), total_10sin_only_saju_score.items())))
        _6chin_score = {
            "인성": round(_10sin_score["편인"] + _10sin_score["정인"], 1),
            "비겁": round(_10sin_score["비견"] + _10sin_score["겁재"], 1),
            "식상": round(_10sin_score["식신"] + _10sin_score["상관"], 1),
            "재성": round(_10sin_score["편재"] + _10sin_score["정재"], 1),
            "관성": round(_10sin_score["편관"] + _10sin_score["정관"], 1),
        }
        _5heng_score = self.oheng_table[self.get_me_il_gan()]
        result_mapper = {"목": "wood", "화": "fire", "토": "ground", "금": "gold", "수": "water"}
        result = {result_mapper[value]: _6chin_score[key] for key, value in _5heng_score.items()}

        return result

    def getJohu(self):
        tmp = []

        if self.m_GanjiYear == -1:
            self.makeGanji()

        ilGan = self.m_GanjiDay % 10 # 일간을 구한다
        wolJi = self.m_GanjiMonth % 12 # 월지를 구한다.

        tmp[0] = self.caJohuTable[ilGan][wolJi]
        tmp[1] = None
        nJohu = tmp

        out_johuname = self.caGanTable[nJohu]
        return nJohu, out_johuname
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getLuck
    # // Desc: 기 입력된 생년월일시분을 이용해서 대운세수와 해당해의 간지를 추출
    # // Input: int in_sex: 성별 1(남), 2(여)
    # // Output: int * out_luckyear: 대운세수
    # // char * out_name	: 대운세수에 해당하는 10개년의 간지
    # //			 int			   : out_name의 길이
    # // == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
    def getLuck(self):
        self.makeGanji()

        out_name = []
        # 년간을 구한다
        nyunGan = self.m_GanjiYear % 10

        if nyunGan % 2 == 0:  # "甲", "丙", "戊", "庚", "壬": 양년
            bPlus = True
            intPlus = 1
        else:  # "乙", "丁", "己", "辛", "癸": 음년
            bPlus = False
            intPlus = 0

        if intPlus + self.sex == 2:  # 양년(1) 의 남자(1), 음년(0) 의 여자(2) 면 순행한다.
            bAscending = True
        else:  # 음년(0) 의 남자(1), 양년(1) 의 여자(2) 면 역행한다.
            bAscending = False


        PREV_24TERMS, terms24_1, prev_year, prev_month, prev_day, prev_hour, prev_min = self.get24terms(self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min, self.PREV_24TERMS)
        MID_24TERMS, terms24_2, mid_year, mid_month, mid_day, mid_hour, mid_min = self.get24terms(self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min, self.MID_24TERMS)
        NEXT_24TERMS, terms24_3, next_year, next_month, next_day, next_hour, next_min = self.get24terms(self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min, self.NEXT_24TERMS)
        sDate = int(self.me_year * 10000 + self.me_month * 100 + self.me_day)
        prevDate = int(prev_year * 10000 + prev_month * 100 + prev_day)
        midDate = int(mid_year * 10000 + mid_month * 100 + mid_day)

        # // printf("\nsDate=%f, prevDate=%f, midDate=%f", sDate, prevDate, midDate);

        if bAscending:  # 순행하는 사주면
            if sDate > prevDate:  # 초기보다 크면
                nDays = self.getDayByDays(next_year, next_month, next_day, self.me_year, self.me_month, self.me_day)
            elif sDate < prevDate:  # 초기보다 작으면
                nDays = self.getDayByDays(prev_year, prev_month, prev_day, self.me_year, self.me_month, self.me_day)
        else:  # 역행하는 사주면
            if sDate > prevDate:  # 초기보다 크면
                nDays = self.getDayByDays(self.me_year, self.me_month, self.me_day, prev_year, prev_month, prev_day)
            elif sDate < prevDate:  # 초기보다 작으면
                # int    prevmonth_year, prevmonth_month, prevmonth_day, prevmonth_hour, prevmonth_min;
                prevmonth_year, prevmonth_month, prevmonth_day, prevmonth_hour, prevmonth_min = self.getDate2Min(
                    30 * 24 * 60 * -1, self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min)
                PREV_24TERMS, terms24, mid_year, mid_month, mid_day, mid_hour, mid_min = self.get24terms(prevmonth_year,
                                                                                                         prevmonth_month,
                                                                                                         prevmonth_day,
                                                                                                         prevmonth_hour,
                                                                                                         prevmonth_min,
                                                                                                         self.PREV_24TERMS)
                midDate = int(mid_year * 10000 + mid_month * 100 + mid_day)
                nDays = self.getDayByDays(self.me_year, self.me_month, self.me_day, mid_year, mid_month, mid_day)
        if sDate == prevDate or sDate == midDate:
            nDays = 1

        if nDays <= 4:
            nLuck = 1
        else:
            nLuck = int(nDays / 3)
            if (nDays % 3) == 2:
                nLuck = nLuck + 1

        if nLuck > 10:
            nLuck = 10

        out_luckyear = nLuck

        if bAscending:
            for idx in range(0, 10):
                if (self.m_GanjiMonth + 1 + idx) > 60:
                    ganidx = 60 - self.m_GanjiMonth + 21 + idx
                else:
                    ganidx = self.m_GanjiMonth + 1 + idx

                if (ganidx >= 60):
                    ganidx = 59

                if (ganidx < 0):
                    ganidx = 0

                out_name.append(self.caGanjiTable[ganidx])
        # 역행...
        else:
            minusidx = 0
            for idx in range(0, 10):
                ganidx = self.m_GanjiMonth - idx - 1
                if ganidx <= 0:
                    ganidx = 60 - minusidx
                    minusidx = minusidx + 1

                if(ganidx >= 60):
                    ganidx = 59

                if (ganidx < 0):
                    ganidx = 0

                out_name.append(self.caGanjiTable[ganidx])

        return out_luckyear, out_name, bAscending
    # # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # # // Name: getJoseng
    # # // Desc: 일간과 현재일시를 이용하여 현재의 간을 구한다.
    # # // Input: int in_gan : 현재간의 array
    # # //							  (갑:0 ,을:1 ,병:2 ,정:3 ,무:4 ,기:5 ,경:6 ,신:7 ,임:8 ,계:9)
    # # //  Output : char *out_name: 추출한 음악 조성 명
    # # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # def getJoseng(self, in_gan):
    #     if in_gan == 4 or in_gan == 5: # 간이 무, 기인 경우
    #         if in_gan == 4: # 무면 메이저
    #             nMajorMinor = 0
    #         else: # 기면 마이너
    #             nMajorMinor = 1
    #
    #         # time_t temp;
    #         # time( & temp);
    #         # struct tm * tmCurrent = localtime( & temp);
    #
    #         nDay = 100 + tmCurrent[m_mday]
    #         if nDay >= 204 and nDay <= 504: # 양력 2 월 4 일부터 5 월 4 일까지 - -진
    #             nJi = 4
    #         elif nDay >= 505 and nDay <= 806: # 양력 5월 5일부터 8월 6일까지--미
    #             nJi = 7
    #         elif nDay >= 807 and nDay <= 1008: # 양력 8월 7일부터 10월8일까지--술
    #             nJi = 10
    #         else: # 양력 10월9일부터 2월 3일까지--축
    #             nJi = 1
    #     else: # 기타사항
    #         if self.m_GanjiYear == -1:
    #             self.makeGanji()
    #
    #         ilGan = self.m_GanjiDay % 10 # 일간을 구한다.
    #         # "甲", "丙", "戊", "庚", "壬": 양끼리 조합 또는
    #         # "乙", "丁", "己", "辛", "癸": 음끼리 조합이면 메이저
    #         if ((ilGan % 2 == 0) and (in_gan % 2 == 0)) or ((ilGan % 2 == 1) and (in_gan % 2 == 1)):
    #             nMajorMinor = 0
    #         else:
    #             nMajorMinor = 1
    #             nJi = self.naGanJiTable[in_gan]
    #
    #     out_name = self.caJosengTable[nMajorMinor][nJi]
    #     # printf("\n(in_gan=%d, nMajorMinor=%d, nJi=%d, out=%s)", in_gan, nMajorMinor, nJi, out_name);
    #
    #     return out_name

    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getCurrentGan
    # // Desc: 일간과 현재일시를 이용하여 현재의 간을 구한다.
    # // Input: None
    # // Output: char * out_name: 추출한 간의 한자명
    # // int		: caGanTabl 의 해당 array
    # / /= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    def getCurrentGan(self):
        # if self.m_GanjiYear == -1:
        #     self.makeGanji()

        ilGan = self.m_GanjiDay % 10 # 일간을 구한다.

        # //	printf("\nCurrent:%d.%d.%d %d:%d",
        # //			tmCurrent->tm_year + 1900, tmCurrent->tm_mon + 1, tmCurrent->tm_mday,
        # // tmCurrent->tm_hour, tmCurrent->tm_min);
        yyyy = int(datetime.today().strftime('%Y'))
        mm = int(datetime.today().strftime('%m'))
        dd = int(datetime.today().strftime('%d'))
        hh = int(datetime.today().strftime('%H'))
        M = int(datetime.today().strftime('%M'))

        nGanjiYear, nGanjiMonth, nGanjiDay, nGanjiHour = self.makeGanji(yyyy, mm, dd, hh, M)

        nCurilGan = nGanjiDay % 10 # 일간을 구한다.
        nCursiGan = nGanjiHour % 10 # 시간을 구한다.

        nAry = int(self.caCurrentGanTable[ilGan][nCurilGan][nCursiGan])

        out_name = self.caGanTable[nAry]
        print(ilGan, nCurilGan, nCursiGan, out_name)
        return nAry, out_name
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getCurrentJoseng
    # // Desc: 일간과 현재일시를 이용하여 음악조성을 구한다.
    # // Input: None
    # // Output: char * out_name: 추출한 조성
    # // int		: 추 한 현 의 간(caGanTabl 의 해당 array)
    # / /= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===

    # self.getJoseng()이 동작하지 않음
    def getCurrentJoseng(self):
        # tmp = [100]
        # nCurrentGan = self.getCurrentGan(tmp)
        nCurrentGan = self.getCurrentGan()
        out_name = self.getJoseng(nCurrentGan)

        return nCurrentGan, out_name
    # //======================================================================
    # //  Name   : getColorGan
    # //  Desc   : 현재의 간과 선택한 색을 이용해 새로운 간을 구한다.
    # //  Input  : int in_color 	: 선택한 색(define된 색)
    # //			 int in_gan 	: 현재간의 array
    # //							  (갑:0,을:1,병:2,정:3,무:4,기:5,경:6,신:7,임:8,계:9)
    # //  Output : char *out_name : 추출한 간의 한자명
    # //			 int			: caGanTable의 해당 array
    # //======================================================================
    def getColorGan(self, in_color, in_gan):
        # int		nAry;
        tmp = ''

        tmp = self.caColorGanTable[in_color][in_gan]
        nAry = tmp
        out_name = self.caGanTable[nAry]

    # //	printf("\n(_color=%d, in_gan=%d, color_gan=%s, name=%s",
    # //		in_color, in_gan, tmp, caGanTable[nAry]);
        return nAry, out_name
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getColorJoseng
    # // Desc: 현재의 간과 선택한 색을 이용해 음악조성을 구한다.
    # // Input: int in_color : 선택한 색(define된 색)
    # //			 int in_gan 	: 현재간의 array
    # //  Output : char *out_name: 추출한 조성
    # // int		: 추한 십간(caGanTabl의 해당 array)
    # / /= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ===
    def getColorJoseng(self, in_color, in_gan):
        tmp = ''

        nCurrentGan, tmp = self.getColorGan(in_color, in_gan)
        out_name = self.getJoseng(nCurrentGan);

        return nCurrentGan, out_name

    def get_temperature(self, idx_list):
        with open(temperature_file_path, encoding='utf-8') as f:
            rdr = csv.reader(f)
            list = []
            gabja = [row for row in rdr]
            for count, idx in enumerate(idx_list):
                list.append(float(gabja[idx][1:][count]))
            sum_list = sum(list)
            return round(sum_list/len(list), 1)

    def get_humidity(self, idx_list):
        with open(humidity_file_path, encoding='utf-8') as f:
            rdr = csv.reader(f)
            list = []
            gabja = [row for row in rdr]
            for count, idx in enumerate(idx_list):
                list.append(float(gabja[idx][1:][count]))
            sum_list = sum(list)
            return round(sum_list/len(list), 1)

    def get_weather(self, now_si_ju_gan):
        case = random.choice([True, False])
        il_gan = self.getGanji()[2][0]
        il_gan_idx = self.caGanTable.index(il_gan)
        if case:
            result = self.weather_table_case1[now_si_ju_gan][il_gan_idx]
        else:
            result = self.weather_table_case2[now_si_ju_gan][il_gan_idx]
        return result

    def get_daily_weather(self):
        year = int(datetime.today().strftime('%Y'))
        month = int(datetime.today().strftime('%m'))
        day = int(datetime.today().strftime('%d'))
        min = 30
        mapper_list = ["자시", "축시", "인시", "묘시", "진시", "사시", "오시", "미시", "신시", "유시", "술시", "해시"]
        weather_mapper = {"맑음": "sun", "구름": "cloud", "흐림": "cloud-sun", "소나기": "rain", "쨍쨍": "sunset", "가랑눈": "cloud-snow", "번개": "cloud-lightning", "미풍": "wind",
         "함박눈": "snow", "안개": "cloud-fog", "무지개": "rainbow", "폭우": "umbrella", "달빛": "moon", "황사": "sand-wind", "미세먼지": "mise", "태풍": "typhoon"}

        il_gan_idx = self.caGanTable.index((self.getGanji()[2][0]))
        daily_list = [self.get_ganji(year=year, month=month, day=day, hour=hour, min=min)[3][0] for hour in range(0, 24, 2)]
        daily_weather_dict = {mapper_list[idx]: weather_mapper[self.weather_table_case1[si_ju_gan][il_gan_idx]] for idx, si_ju_gan in enumerate(daily_list)}

        return daily_weather_dict

    def get_season(self, dae_won_ji):
        print('@@@@@@ table_12 start @@@@@@')
        print('@@@@@@ get_me_il_gan @@@@@@ : ', self.get_me_il_gan())
        array_12 = self.table_12[self.get_me_il_gan()]
        print('@@@@@@ array_12 @@@@@@')
        print('@@@@@@ array_12 @@@@@@ : ', array_12)
        print('@@@@@@ dae_won_ji @@@@@@ : ', dae_won_ji)
        index = array_12.index(dae_won_ji)
        print('@@@@@@ table_woonsung start @@@@@@')
        woonsung_12 = self.table_woonsung[index]
        print('@@@@@@ index @@@@@@')
        season_dict = {
            "절": 11,
            "태": 12,
            "양": 1,
            "장생": 2,
            "목욕": 3,
            "관대": 4,
            "건록": 5,
            "제왕": 6,
            "쇠": 7,
            "병": 8,
            "사": 9,
            "묘": 10,
        }
        month = season_dict[woonsung_12]
        if month in [2, 3, 4]:
            season = "봄"
        elif month in [5, 6, 7]:
            season = "여름"
        elif month in [8, 9, 10]:
            season = "가을"
        elif month in [11, 12, 1]:
            season = "겨울"
        return month, season

    def get_10sin(self, type, idx):
        with open(str(base_file_path).format(type=type), encoding='utf-8') as f:
            rdr = csv.reader(f)
            gabja = [row for row in rdr]
            get_10sin_score = [float(0.0) if i == '' else float(i) for i in gabja[idx][1:]]
            ilgan = self.get_me_il_gan()
            header = self.get_10sin_header(ilgan)
            result = {header[i]: float(get_10sin_score[i]) for i in range(0, 10)}
        return result

    def get_me_il_gan(self):
        ganji = self.getGanji()
        return ganji[2][0]

    def get_me_il_ju(self):
        ganji = self.getGanji()
        return self.ko_GanjiTable[ganji[6]]

    def get_10sin_header(self, ilgan):
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

    def get_dae_won(self):
        age = (int(self.now_year) - int(self.me_year)) + 1
        dae_won_su, dae_won_list, is_tour = self.getLuck()
        dea_luck = int(dae_won_su)
        generations = [0 + dea_luck, 10 + dea_luck, 20 + dea_luck, 30 + dea_luck, 40 + dea_luck, 50 + dea_luck, 60 + dea_luck, 70 + dea_luck,
                       80 + dea_luck, 90 + dea_luck, 100+dea_luck, 110+dea_luck]
        if 0 + dea_luck <= age < 10 + dea_luck:
            generation = 0
        elif 10 + dea_luck <= age < 20 + dea_luck:
            generation = 1
        elif 20 + dea_luck <= age < 30 + dea_luck:
            generation = 2
        elif 30 + dea_luck <= age < 40 + dea_luck:
            generation = 3
        elif 40 + dea_luck <= age < 50 + dea_luck:
            generation = 4
        elif 50 + dea_luck <= age < 60 + dea_luck:
            generation = 5
        elif 60 + dea_luck <= age < 70 + dea_luck:
            generation = 6
        elif 70 + dea_luck <= age < 80 + dea_luck:
            generation = 7
        elif 80 + dea_luck <= age < 90 + dea_luck:
            generation = 8
        elif 90 + dea_luck <= age < 100 + dea_luck:
            generation = 9
        else:
            generation = 9
        dea_won = dae_won_list[generation]
        print('@@@@@@ dea_won @@@@@@ : ', dea_won)
        print('@@@@@@ dae_won_list @@@@@@ : ', dae_won_list)
        print('@@@@@@ get_season start @@@@@@')
        month, season = self.get_season(dea_won[1])
        print('@@@@@@ get_season @@@@@@')
        generations = generations[generation:] + generations[:generation]
        dict = {}

        for idx, generation in enumerate(generations):
            if int(month) > 12:
                month = 1
            dict[generation] = f"{month}월"
            month += 1
        now_dae_won = list(dict.values())[0]
        sorted_dict = {k: dict[k] for k in sorted(dict)}

        return {
            "dae_won": dea_won,
            "dae_won_su": dae_won_su,
            "way": "순행" if is_tour else "역행",
            "age": age,
            "won_flow": sorted_dict,
            "now_dae_won": now_dae_won,
        }

    def get_dae_won_flow(self):
        dae_won = self.get_dae_won()
        age = dae_won['age']
        now_year = datetime.today().strftime('%Y')
        dae_won_flow = dae_won['won_flow']
        age_list = list(dae_won_flow.keys())
        month_list = list(dae_won_flow.values())
        first_daewon_year = (int(now_year) - (age - age_list[0]))
        year_list = []
        for order in range(0, len(age_list)):
            year_list.append(first_daewon_year + order*10)

        dae_won_flow = [{
            "age": age_list[idx],
            "year": year_list[idx],
            "month": month_list[idx],

        } for idx in range(0, 12)]

        return dae_won_flow

    def suju_index_list(self):
        print('@@@@@@ Start @@@@@@')
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()
        print('@@@@@@ makeGanji @@@@@@')
        now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=self.now_year, in_smonth=self.now_month,
                                                                                       in_sday=self.now_day, in_shour=self.now_hour,
                                                                                       in_smin=self.now_min)
        print('@@@@@@ makeGanji2 @@@@@@')
        # now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=2021, in_smonth=12,
        #                                                                                    in_sday=22, in_shour=15,
        #                                                                                    in_smin=31)

        # 대운
        dae_won_dict = self.get_dae_won()
        print('@@@@@@ get_dae_won @@@@@@')
        dae_won_idx = self.caGanjiTable.index(dae_won_dict["dae_won"])
        # 연주, 월주, 일주, 시주
        # _10sin_year = self.get_10sin("year", yeon_ju_idx)
        # print("년주", sum(_10sin_year.values()))

        # _10sin_month = self.get_10sin("month", wol_ju_idx)
        # print("월주", sum(_10sin_month.values()))

        # _10sin_day = self.get_10sin("day", il_ju_idx)
        # print("일주", sum(_10sin_day.values()))

        # _10sin_time = self.get_10sin("time", si_ju_idx)
        # print("시주", sum(_10sin_time.values()))

        # _10sin_dae_won = self.get_10sin("big_luck", dae_won_idx)
        # print("대운", _10sin_dae_won)

        # _10sin_year_luck = self.get_10sin("year_luck", now_yeon_ju_idx)
        # print("세운", sum(_10sin_year_luck.values()))

        # _10sin_month_luck = self.get_10sin("month_luck", now_wol_ju_idx)
        # print("월운", sum(_10sin_month_luck.values()))

        # _10sin_day_luck = self.get_10sin("day_luck", now_il_ju_idx)
        # print("일운", sum(_10sin_day_luck.values()))

        # _10sin_time_luck = self.get_10sin("time_luck", now_si_ju_idx)
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
        return _10sin_idx_list

    def get_10sin_score(self):
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()

        now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=self.now_year, in_smonth=self.now_month,
                                                                                       in_sday=self.now_day, in_shour=self.now_hour,
                                                                                       in_smin=self.now_min)

        # now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=2021, in_smonth=12,
        #                                                                                in_sday=22, in_shour=15,
        #                                                                                in_smin=31)

        # 대운
        dae_won_dict = self.get_dae_won()
        dae_won_idx = self.caGanjiTable.index(dae_won_dict["dae_won"])

        # 연주, 월주, 일주, 시주
        _10sin_year = self.get_10sin("year", yeon_ju_idx)
        # print("년주", sum(_10sin_year.values()))

        _10sin_month = self.get_10sin("month", wol_ju_idx)
        # print("월주", sum(_10sin_month.values()))

        _10sin_day = self.get_10sin("day", il_ju_idx)
        # print("일주", sum(_10sin_day.values()))

        _10sin_time = self.get_10sin("time", si_ju_idx)
        # print("시주", sum(_10sin_time.values()))

        _10sin_dae_won = self.get_10sin("big_luck", dae_won_idx)
        # print("대운", _10sin_dae_won)

        _10sin_year_luck = self.get_10sin("year_luck", now_yeon_ju_idx)
        # print("세운", sum(_10sin_year_luck.values()))

        _10sin_month_luck = self.get_10sin("month_luck", now_wol_ju_idx)
        # print("월운", sum(_10sin_month_luck.values()))

        _10sin_day_luck = self.get_10sin("day_luck", now_il_ju_idx)
        # print("일운", sum(_10sin_day_luck.values()))

        _10sin_time_luck = self.get_10sin("time_luck", now_si_ju_idx)
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

        dicts = [_10sin_year, _10sin_month, _10sin_day, _10sin_time, _10sin_dae_won, _10sin_year_luck,
                 _10sin_month_luck, _10sin_day_luck, _10sin_time_luck]
        total_10sin_score = reduce(lambda a, b: a.update(b) or a, dicts, Counter())
        return total_10sin_score

    def get_10sin_score_100_percent(self):
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()

        now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=self.now_year, in_smonth=self.now_month,
                                                                                       in_sday=self.now_day, in_shour=self.now_hour,
                                                                                       in_smin=self.now_min)

        # now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=2021, in_smonth=12,
        #                                                                                    in_sday=22, in_shour=15,
        #                                                                                    in_smin=31)

        # 대운
        dae_won_dict = self.get_dae_won()
        dae_won_idx = self.caGanjiTable.index(dae_won_dict["dae_won"])

        # 연주, 월주, 일주, 시주
        _10sin_year = self.get_10sin("year", yeon_ju_idx)
        # print("년주", sum(_10sin_year.values()))

        _10sin_month = self.get_10sin("month", wol_ju_idx)
        # print("월주", sum(_10sin_month.values()))

        _10sin_day = self.get_10sin("day", il_ju_idx)
        # print("일주", sum(_10sin_day.values()))

        _10sin_time = self.get_10sin("time", si_ju_idx)
        # print("시주", sum(_10sin_time.values()))

        _10sin_dae_won = self.get_10sin("big_luck", dae_won_idx)
        # print("대운", _10sin_dae_won)

        _10sin_year_luck = self.get_10sin("year_luck", now_yeon_ju_idx)
        # print("세운", sum(_10sin_year_luck.values()))

        _10sin_month_luck = self.get_10sin("month_luck", now_wol_ju_idx)
        # print("월운", sum(_10sin_month_luck.values()))

        _10sin_day_luck = self.get_10sin("day_luck", now_il_ju_idx)
        # print("일운", sum(_10sin_day_luck.values()))

        _10sin_time_luck = self.get_10sin("time_luck", now_si_ju_idx)
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

        dicts = [_10sin_year, _10sin_month, _10sin_day, _10sin_time, _10sin_dae_won, _10sin_year_luck,
                 _10sin_month_luck, _10sin_day_luck, _10sin_time_luck]

        # saju_dict = [_10sin_year, _10sin_month, _10sin_day, _10sin_time]

        total_10sin_score = reduce(lambda a, b: a.update(b) or a, dicts, Counter())
        _10sin_score = dict(
            zip(total_10sin_score.keys(), map(lambda x: round((x[1] / 375) * 100, 1), total_10sin_score.items())))

        return _10sin_score

    def get_10sin_only_day_luck(self):
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()

        now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=self.now_year, in_smonth=self.now_month,
                                                                                       in_sday=self.now_day, in_shour=self.now_hour,
                                                                                       in_smin=self.now_min)
        # 연주, 월주, 일주, 시주, 일운
        _10sin_year = self.get_10sin("year", yeon_ju_idx)
        _10sin_month = self.get_10sin("month", wol_ju_idx)
        _10sin_day = self.get_10sin("day", il_ju_idx)
        _10sin_time = self.get_10sin("time", si_ju_idx)
        _10sin_day_luck = self.get_10sin("day_luck", now_il_ju_idx)

        dicts = [_10sin_year, _10sin_month, _10sin_day, _10sin_time, _10sin_day_luck]

        total_10sin_score = reduce(lambda a, b: a.update(b) or a, dicts, Counter())

        _10sin_score = dict(
            zip(total_10sin_score.keys(), map(lambda x: round((x[1] / 210) * 100, 1), total_10sin_score.items())))

        return _10sin_score

    def get12woonsung(self):
        il_gan = self.getGanji()[2][0]
        now_il_won_jiji = self.now_getGanji()[1][1]
        array_12 = self.table_12[il_gan]
        index = array_12.index(now_il_won_jiji)
        woonsung_12 = self.table_woonsung[index]
        return woonsung_12

    def music_set(self):
        il_gan_idx = self.caGanTable.index(self.getGanji()[2][0])
        if self.sex == 1 and il_gan_idx % 2 == 1:
            il_gan_idx -= 1
        return self.music_playlist_set[self.get12woonsung()][il_gan_idx]

    def fourth_place_by_luck(self, luck_name):
        woman_luck_dict = {
            "money": ["편재", "정재", "식신", "상관"],
            "love": ["편재", "정재", "편관", "정관", "상관"],
            "study": ["편관", "정관", "편인", "정인"],
            "health": ["편인", "정인", "비견", "겁재"]
        }
        man_luck_dict = {
            "money": ["편재", "정재", "편관", "정관", "식신", "상관"],
            "love": ["편재", "정재", "식신", "상관"],
            "study": ["편관", "정관", "편인", "정인"],
            "health": ["편인", "정인", "비견", "겁재"]
        }

        if self.sex == 1:
            _10_sin_list = man_luck_dict[luck_name]
        else:
            _10_sin_list = woman_luck_dict[luck_name]

        return _10_sin_list

    def get_music_10sin_score(self):
        li_gan_music_ji = self.jiji_10sin_table[self.getGanji()[2][0]]
        # print(li_gan_music_ji)
        mapping_ji_il_gan = dict(zip(li_gan_music_ji, self.caJiTable))
        # print(mapping_ji_il_gan)
        _10_sin_score = self.get_10sin_score()
        # print(_10_sin_score)
        _10_sin_music_score = {}
        for key, value in _10_sin_score.items():
            count = 1
            if not li_gan_music_ji.count(key) == 1:  # 반복 되는 십신
                count = li_gan_music_ji.count(key)
            _10_sin_music_score[key] = value / count
        return _10_sin_music_score

    def music_recommend_of_day(self, luck_name):
        if luck_name not in ['money', 'study', 'love', 'health']:
            raise ValueError
        li_gan_music_ji = self.jiji_10sin_table[self.getGanji()[2][0]]
        mapping_ji_il_gan = dict(zip(li_gan_music_ji, self.caJiTable))
        _10_sin_score = self.get_10sin_only_day_luck()
        _10_sin_music_score = {}
        for key, value in _10_sin_score.items():
            count = 1
            if key in self.fourth_place_by_luck(luck_name):
                if not li_gan_music_ji.count(key) == 1:  # 반복 되는 십신
                    count = li_gan_music_ji.count(key)
                _10_sin_music_score[key] = value/count

        sorted_10_sin_music_score = sorted(_10_sin_music_score.items(), key=lambda x: x[1])
        music_ji_ji = [mapping_ji_il_gan[key] for key, value in sorted_10_sin_music_score[:4]]
        music_recommend_dict = {key: self.josung_table[key] for key in music_ji_ji}

        # print(music_recommend_dict)
        set_1 = [(0, 0), (0, 0), (0, 1), (1, 0), (1, 0), (1, 1), (2, 0), (2, 0), (2, 1), (3, 0), (3, 0), (3, 1)]
        set_2 = [(0, 2), (0, 2), (0, 3), (1, 2), (1, 2), (1, 3), (2, 2), (2, 2), (2, 3), (3, 2), (3, 2), (3, 3)]
        set_3 = [(0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2), (0, 2), (0, 3), (0, 3), (0, 3)]
        set_4 = [(0, 2), (0, 2), (0, 2), (0, 3), (0, 3), (0, 3), (0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1)]

        if self.music_set() == 'Set 1':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_1]
        elif self.music_set() == 'Set 2':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_2]
        elif self.music_set() == 'Set 3':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_3]
        elif self.music_set() == 'Set 4':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_4]
        # print(music_recommend_list)
        return list(set(music_recommend_list))

    def music_recommend(self, luck_name):
        if luck_name not in ['money', 'study', 'love', 'health']:
            raise ValueError
        li_gan_music_ji = self.jiji_10sin_table[self.getGanji()[2][0]]
        # print(li_gan_music_ji)
        mapping_ji_il_gan = dict(zip(li_gan_music_ji, self.caJiTable))
        # print(mapping_ji_il_gan)
        _10_sin_score = self.get_10sin_score()
        # print(_10_sin_score)
        _10_sin_music_score = {}
        for key, value in _10_sin_score.items():
            count = 1
            if key in self.fourth_place_by_luck(luck_name):
                if not li_gan_music_ji.count(key) == 1:  # 반복 되는 십신
                    count = li_gan_music_ji.count(key)
                _10_sin_music_score[key] = value/count

        # print("_10_sin_music_score", _10_sin_music_score)
        sorted_10_sin_music_score = sorted(_10_sin_music_score.items(), key=lambda x: x[1])
        # print(sorted_10_sin_music_score)
        # print(sorted_10_sin_music_score[:4])

        music_ji_ji = [mapping_ji_il_gan[key] for key, value in sorted_10_sin_music_score[:4]]

        # print("music_ji_ji", music_ji_ji)

        music_recommend_dict = {key: self.josung_table[key] for key in music_ji_ji}
        # print("music_recommend_dict", music_recommend_dict)

        set_1 = [(0, 0), (0, 0), (0, 1), (1, 0), (1, 0), (1, 1), (2, 0), (2, 0), (2, 1), (3, 0), (3, 0), (3, 1)]
        set_2 = [(0, 2), (0, 2), (0, 3), (1, 2), (1, 2), (1, 3), (2, 2), (2, 2), (2, 3), (3, 2), (3, 2), (3, 3)]
        set_3 = [(0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2), (0, 2), (0, 3), (0, 3), (0, 3)]
        set_4 = [(0, 2), (0, 2), (0, 2), (0, 3), (0, 3), (0, 3), (0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1)]

        # print(self.music_set())
        """
        재물운, 학업운의 첫번째로 1순위의 십신의 십이 운성이
        학업운 : music_recommend_dict {'卯': 'Eb/D#, c, eb/d#, F#', '寅': 'D, b, d, F', '亥': 'B, ab/g#, b, D', '申': 'Ab/G#, f, ab/g#, B'}
        재물은 : music_recommend_dict {'卯': 'Eb/D#, c, eb/d#, F#', '午': 'F#, eb/d#, f#, A', '巳': 'F, d, f, Ab/G#', '寅': 'D, b, d, F'}
        같을 경우 set_4는 하루동안 일정함으로, 노래추천이 같아짐.
        """
        if self.music_set() == 'Set 1':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_1]
        elif self.music_set() == 'Set 2':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_2]
        elif self.music_set() == 'Set 3':
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_3]
        else:
            music_recommend_list = [list(music_recommend_dict.values())[priority].split(",")[josung].replace(" ", "") for priority, josung in set_4]

        return music_recommend_list

    def get_luck_score(self):
        # 재성( 편재, 정재 ) , 관성( 편관, 정관), 인성( 편인, 정인 ), 비겁( 비견, 겁재 ),
        _10sin_score = self.get_10sin_score_100_percent()
        reference_score = [9.5, 9.3, 9.5, 9.3, 9.5, 7.8, 14.7, 11.5, 9.5, 9.3]
        reference_score_dict = dict(zip(_10sin_score.keys(), reference_score))

        if self.sex == 1:
            reference_luck_score = {
                "애정운": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1 / 2) + (reference_score_dict["식신"] + reference_score_dict["상관"]) * (1 / 2),
                "재물운": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1 / 2) + (
                            reference_score_dict["식신"] + reference_score_dict["상관"]) * (1 / 2) + (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1 / 2),
                "학업운": (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1/2) + (reference_score_dict["편인"] + reference_score_dict["정인"]) * (1/2),
                "건강운": (reference_score_dict["비견"] + reference_score_dict["겁재"])
            }
        else:
            reference_luck_score = {
                "애정운": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1/2) + (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1/2) + (reference_score_dict["식신"] + reference_score_dict["상관"]) * (1/2),
                "재물운": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1/2) + (reference_score_dict["식신"] + reference_score_dict["상관"]) * (1/2),
                "학업운": (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1/2) + (reference_score_dict["편인"] + reference_score_dict["정인"]) * (1/2),
                "건강운": (reference_score_dict["비견"] + reference_score_dict["겁재"])
            }

        if self.sex == 1:
            luck_score = {
                "애정운": (_10sin_score["편재"] + _10sin_score["정재"]) * (1 / 2) + (_10sin_score["식신"] + _10sin_score["상관"]) * (1 / 2),
                "재물운": (_10sin_score["편재"] + _10sin_score["정재"]) * (1 / 2) + (
                            _10sin_score["식신"] + _10sin_score["상관"]) * (1 / 2) + (_10sin_score["편관"] + _10sin_score["정관"]) * (1 / 2),
                "학업운": (_10sin_score["편관"] + _10sin_score["정관"]) * (1/2) + (_10sin_score["편인"] + _10sin_score["정인"]) * (1/2),
                "건강운": (_10sin_score["비견"] + _10sin_score["겁재"])
            }
        else:
            luck_score = {
                "애정운": (_10sin_score["편재"] + _10sin_score["정재"]) * (1/2) + (_10sin_score["편관"] + _10sin_score["정관"]) * (1/2) + (_10sin_score["식신"] + _10sin_score["상관"]) * (1/2),
                "재물운": (_10sin_score["편재"] + _10sin_score["정재"]) * (1/2) + (_10sin_score["식신"] + _10sin_score["상관"]) * (1/2),
                "학업운": (_10sin_score["편관"] + _10sin_score["정관"]) * (1/2) + (_10sin_score["편인"] + _10sin_score["정인"]) * (1/2),
                "건강운": (_10sin_score["비견"] + _10sin_score["겁재"])
            }

        result = {
            "애정운": 50 + self.calculator(round(reference_luck_score["애정운"], 2), round(luck_score["애정운"], 2))
            if round(reference_luck_score["애정운"], 2) < round(luck_score["애정운"], 2)
            else 50 - self.calculator(round(reference_luck_score["애정운"], 2), round(luck_score["애정운"], 2)),
            "재물운": 50 + self.calculator(round(reference_luck_score["재물운"], 2), round(luck_score["재물운"], 2))
            if round(reference_luck_score["재물운"], 2) < round(luck_score["재물운"], 2)
            else 50 - self.calculator(round(reference_luck_score["재물운"], 2), round(luck_score["재물운"], 2)),
            "학업운": 50 + self.calculator(round(reference_luck_score["학업운"], 2), round(luck_score["학업운"], 2))
            if round(reference_luck_score["학업운"], 2) < round(luck_score["학업운"], 2)
            else 50 - self.calculator(round(reference_luck_score["학업운"], 2), round(luck_score["학업운"], 2)),
            "건강운": 50 + self.calculator(round(reference_luck_score["건강운"], 2), round(luck_score["건강운"], 2))
            if round(reference_luck_score["건강운"], 2) < round(luck_score["건강운"], 2)
            else 50 - self.calculator(round(reference_luck_score["건강운"], 2), round(luck_score["건강운"], 2)),

        }

        return result

    def saju_me_action(self):
        return {
            "temperature_avg": self.get_temperature(self.suju_index_list()),
            "humidity_avg": self.get_humidity(self.suju_index_list()),
            "weather": self.get_weather(self.now_getGanji()[3][0]),
            "daily_weather": self.get_daily_weather(),
            "saju_score": self.get_10sin_score_100_percent(),
            "luck_score": self.get_luck_score(),
            "oheang_score": self.getOheng_D(),
            "il_gan": self.get_me_il_gan(),
            "il_ju": self.get_me_il_ju(),
            "age": self.get_dae_won()['age'],
            "way": self.get_dae_won()['way'],
            "dae_won": self.get_dae_won()['dae_won'],
            "dae_won_su": self.get_dae_won()['dae_won_su'],
            "now_dae_won": self.get_dae_won()['now_dae_won'],
            "dae_won_flow": self.get_dae_won_flow()
        }

    def saju_me(self):
        return {
            "temperature_avg": self.get_temperature(self.suju_index_list()),
            "humidity_avg": self.get_humidity(self.suju_index_list()),
            "weather": self.get_weather(self.now_getGanji()[3][0]),
            "daily_weather": self.get_daily_weather(),
            "il_gan": self.get_me_il_gan(),
            # "age": self.get_dae_won()['age'],
            # "way": self.get_dae_won()['way'],
            # "dae_won": self.get_dae_won()['dae_won'],
            # "dae_won_su": self.get_dae_won()['dae_won_su'],
            "now_dae_won": self.get_dae_won()['now_dae_won'],
            # "dae_won_flow": self.get_dae_won_flow()
        }

    def saju_me_recommend(self):

        return {
            "건강운 음악 추천": set(self.music_recommend("health")),
            "애정운 음악 추천": set(self.music_recommend("love")),
            "재물운 음악 추천": set(self.music_recommend("money")),
            "학업운 음악 추천": set(self.music_recommend("study")),
        }

    @staticmethod
    def calculator(ref, x):
        return round((abs(ref - x) / ref) * 55)


def get12woonsung(gan, ji):
    table_woonsung = ['장생', '목욕', '관대', '건록', '제왕', '쇠', '병', '사', '묘', '절', '태', '양']
    table_12 = {
        '甲': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
        '乙': ['午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未'],
        '丙': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '丁': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
        '戊': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '己': ['酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌'],
        '庚': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
        '辛': ['子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅', '丑'],
        '壬': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'],
        '癸': ['卯', '寅', '丑', '子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰'],
    }

    array_12 = table_12[gan]
    index = array_12.index(ji)
    woonsung_12 = table_woonsung[index]
    print(woonsung_12)

    return woonsung_12


def get6chin(gan, oheang, oheang_rate):
    """
    '목 화 토 금 수' 를 천간에 따라서 맵핑해 둔거
    :param gan: str
    :param oheang: dict
    :param oheang_rate: dict
    :return: 육친, 육친비율
    """
    table_6chin = {
        '甲': ['비겁', '식상', '재성', '관성', '인성'],  # 갑
        '乙': ['비겁', '식상', '재성', '관성', '인성'],  # 을
        '丙': ['인성', '비겁', '식상', '재성', '관성'],  # 병
        '丁': ['인성', '비겁', '식상', '재성', '관성'],  # 정
        '戊': ['관성', '인성', '비겁', '식상', '재성'],  # 무
        '己': ['관성', '인성', '비겁', '식상', '재성'],  # 기
        '庚': ['재성', '관성', '인성', '비겁', '식상'],  # 경
        '辛': ['재성', '관성', '인성', '비겁', '식상'],  # 신
        '壬': ['식상', '재성', '관성', '인성', '비겁'],  # 임
        '癸': ['식상', '재성', '관성', '인성', '비겁'], }  # 계

    table_6 = table_6chin[gan]

    chin6 = {'인성': oheang[table_6.index('인성')],
             '비겁': oheang[table_6.index('비겁')],
             '식상': oheang[table_6.index('식상')],
             '재성': oheang[table_6.index('재성')],
             '관성': oheang[table_6.index('관성')]}

    chin6_rate = {'인성': oheang_rate[table_6.index('인성')],
                  '비겁': oheang_rate[table_6.index('비겁')],
                  '식상': oheang_rate[table_6.index('식상')],
                  '재성': oheang_rate[table_6.index('재성')],
                  '관성': oheang_rate[table_6.index('관성')]}

    print(table_6)

    return chin6, chin6_rate


def get_saju(in_year=1996, in_month=4, in_day=10, in_hour=1, in_min=20):
    saju = Saju(in_year=in_year, in_month=in_month, in_day=in_day, in_hour=in_hour, in_min=in_min)
    ganjiyear, ganjimonth, ganjiday, ganjihour, GanjiYear, GanjiMonth, GanjiDay, GanjiHour = saju.getGanji()

    return ganjiyear, ganjimonth, ganjiday, ganjihour


def proc(in_year=1986, in_month=10, in_day=10, in_hour=13, in_min=30):
    # yyyymmdd = datetime.datetime.today().strftime('%Y-%m-%d')
    # hhmmss = datetime.datetime.today().strftime('%H:%M:%S')

    yyyy = datetime.today().strftime('%Y')
    mm = datetime.today().strftime('%m')
    dd = datetime.today().strftime('%d')

    hh = datetime.today().strftime('%H')
    mm = datetime.today().strftime('%M')
    ss = datetime.today().strftime('%S')

    age = int(yyyy) - int(in_year)
    generation = int(age / 10)

    print(age, generation)

    sm = smsuic()

    saju = Saju(in_year=in_year, in_month=in_month, in_day=in_day, in_hour=in_hour, in_min=in_min)

    ganjiyear, ganjimonth, ganjiday, ganjihour, GanjiYear, GanjiMonth, GanjiDay, GanjiHour = saju.getGanji()

    gan = saju.getCurrentGan()

    print(gan[0], GanjiDay)

    jo = sm.getJoseng(gan[0], GanjiDay)
    print(jo)
    key = ''
    if jo == 'C':
        key = 'C Maj'
    elif jo == 'C#':
        key = 'C# Maj'
    elif jo == 'D':
        key = 'D Maj'
    elif jo == 'Eb':
        key = 'Eb Maj'
    elif jo == 'E':
        key = 'E Maj'
    elif jo == 'F':
        key = 'F Maj'
    elif jo == 'F#':
        key = 'F# Maj'
    elif jo == 'G':
        key = 'G Maj'
    elif jo == 'Ab':
        key = 'Ab Maj'
    elif jo == 'A':
        key = 'A Maj'
    elif jo == 'Bb':
        key = 'Bb Maj'
    elif jo == 'B':
        key = 'B Maj'
    if jo == 'c':
        key = 'c Min'
    elif jo == 'c#':
        key = 'c# Min'
    elif jo == 'd':
        key = 'd Min'
    elif jo == 'd#':
        key = 'd# Min'
    elif jo == 'eb':
        key = 'eb Min'
    elif jo == 'e':
        key = 'e Min'
    elif jo == 'f':
        key = 'f Min'
    elif jo == 'f#':
        key = 'f# Min'
    elif jo == 'g':
        key = 'g Min'
    elif jo == 'ab':
        key = 'ab Min'
    elif jo == 'a':
        key = 'a Min'
    elif jo == 'bb':
        key = 'bb Min'
    elif jo == 'b':
        key = 'b Min'

    # GanjiYear, GanjiMonth, GanjiDay, GanjiHour
    strong, wood, fire, ground, gold, water = saju.getOheng_A(m_GanjiYear=GanjiYear, m_GanjiMonth=GanjiMonth, m_GanjiDay=GanjiDay, m_GanjiHour=GanjiHour)

    print(strong, wood, fire, ground, gold, water)

    total = wood + fire + ground + gold + water
    wood = int(wood / total * 100)
    fire = int(fire / total * 100)
    ground = int(ground / total * 100)
    gold = int(gold / total * 100)
    water = int(water / total * 100)

    oheang = {'wood':wood, 'fire':fire, 'ground':ground, 'gold':gold, 'water':water}
    print(wood, fire, ground, gold, water)
    print(oheang)

    luck = saju.getLuck()
    dea_wonns = luck[1]
    dea_woon = dea_wonns[-1*generation]
    ganji = {'ganjiyear': ganjiyear, 'ganjimonth': ganjimonth, 'ganjiday': ganjiday, 'ganjihour': ganjihour,
             'jo': jo, 'key': key, 'oheang': oheang,
             'age': age, 'generation': generation, 'dea_woon': dea_woon, 'dea_wonns': dea_wonns,
             'luck': luck
             }

    return ganji


def proc_oheng(in_year=1986, in_month=10, in_day=10, in_hour=13, in_min=30, sex=1):
    saju = Saju(in_year=in_year, in_month=in_month, in_day=in_day, in_hour=in_hour, in_min=in_min)
    saju.makeGanji(in_syear=in_year, in_smonth=in_month, in_sday=in_day, in_shour=in_hour, in_smin=in_min)

    yyyy = int(datetime.today().strftime('%Y'))
    mm = int(datetime.today().strftime('%m'))
    dd = int(datetime.today().strftime('%d'))

    hh = int(datetime.today().strftime('%H'))
    mi = int(datetime.today().strftime('%M'))

    nsaju = Saju(in_year=yyyy, in_month=mm, in_day=dd, in_hour=hh, in_min=mi)
    nsaju.makeGanji(in_syear=yyyy, in_smonth=mm, in_sday=dd, in_shour=hh, in_smin=mi)

    age = (int(yyyy) - int(in_year)) + 1
    generation = int(age / 10)
    # print(age, generation)

    try:
        sex = int(sex)
    except:
        sex = 1

    luck = saju.getLuck()
    print(luck)
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

    print('dea_luck :', dea_luck)
    print(dea_wonns)
    print('dea_woon', dea_woon)

    ganji = saju.getGanji()
    print(ganji)
    nganji = nsaju.getGanji()
    print(nganji)

    saju_yyyy = ganji[0]
    saju_mm = ganji[1]
    saju_dd = ganji[2]
    saju_hh = ganji[3]
    woon_dea = dea_woon
    woon_yyyy = nganji[0]
    woon_mm = nganji[1]
    woon_dd = nganji[2]
    woon_hh = nganji[3]

    print('사주원국', saju_yyyy, saju_mm, saju_dd, saju_hh)
    print('대운', woon_dea)
    print('운세', woon_yyyy, woon_mm, woon_dd, woon_hh)

    hab = oheang_hab(
        saju_yyyy=saju_yyyy,
        saju_mm=saju_mm,
        saju_dd=saju_dd,
        saju_hh=saju_hh,
        woon_dea=woon_dea,
        woon_yyyy=woon_yyyy,
        woon_mm=woon_mm,
        woon_dd=woon_dd,
        woon_hh=woon_hh
    )
    print(hab)

    oheng = []
    gabja = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳',
             '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥',
             '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳',
             '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥',
             '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
             '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥',
             '庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳',
             '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥',
             '壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳',
             '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', ]
    print('******************* 오행 값 구하기 START.')

    _y = saju.getOheng_C('yyyy', saju.m_GanjiYear)
    oheng.append(_y)

    _m = saju.getOheng_C('mm', saju.m_GanjiMonth)
    oheng.append(_m)

    _d = saju.getOheng_C('dd', saju.m_GanjiDay)
    oheng.append(_d)

    _h = saju.getOheng_C('hh', saju.m_GanjiHour)
    oheng.append(_h)

    dea_idx = gabja.index(woon_dea)
    _b = saju.getOheng_C('dea', dea_idx)
    oheng.append(_b)

    _ny = saju.getOheng_C('nyyyy', nsaju.m_GanjiYear)
    oheng.append(_ny)

    wmm_idx = gabja.index(woon_mm)
    _nm = saju.getOheng_C('nmm', wmm_idx)
    oheng.append(_nm)

    _nd = saju.getOheng_C('ndd', nsaju.m_GanjiDay)
    oheng.append(_nd)

    _nh = saju.getOheng_C('nhh', nsaju.m_GanjiHour)
    oheng.append(_nh)
    print('******************* 오행 값 구하기 END.')
    print(oheng)

    obj = {'wood': 0, 'fire': 0, 'ground': 0, 'gold': 0, 'water': 0}
    for o in oheng:
        obj['wood'] = obj['wood'] + o[0]
        obj['fire'] = obj['fire'] + o[1]
        obj['ground'] = obj['ground'] + o[2]
        obj['gold'] = obj['gold'] + o[3]
        obj['water'] = obj['water'] + o[4]

    obj['wood'] = int(obj['wood'] * 100) / 100
    obj['fire'] = int(obj['fire'] * 100) / 100
    obj['ground'] = int(obj['ground'] * 100) / 100
    obj['gold'] = int(obj['gold'] * 100) / 100
    obj['water'] = int(obj['water'] * 100) / 100

    total = obj['wood'] + obj['fire'] + obj['ground'] + obj['gold'] + obj['water']
    print('오행 총합', total)

    try:
        obj['wood_rate'] = int(obj['wood'] / total * 10000) / 100
    except:
        obj['wood_rate'] = 0

    try:
        obj['fire_rate'] = int(obj['fire'] / total * 10000) / 100
    except:
        obj['fire_rate'] = 0

    try:
        obj['ground_rate'] = int(obj['ground'] / total * 10000) / 100
    except:
        obj['ground_rate'] = 0

    try:
        obj['gold_rate'] = int(obj['gold'] / total * 10000) / 100
    except:
        obj['gold_rate'] = 0

    try:
        obj['water_rate'] = int(obj['water'] / total * 10000) / 100
    except:
        obj['water_rate'] = 0

    print('오행 백분율 :', obj['wood_rate'], obj['fire_rate'], obj['ground_rate'], obj['gold_rate'], obj['water_rate'])

    dea_wonns.reverse()
    generations.reverse()

    obj['dea_woon_list'] = dea_wonns
    obj['generations'] = generations
    obj['dea_woon'] = dea_woon
    obj['age'] = age

    obj['_y'] = _y
    obj['_m'] = _m
    obj['_d'] = _d
    obj['_h'] = _h
    obj['_b'] = _b
    obj['_ny'] = _ny
    obj['_nm'] = _nm
    obj['_nd'] = _nd
    obj['_nh'] = _nh

    obj['woon_yyyy'] = woon_yyyy
    obj['woon_mm'] = woon_mm
    obj['woon_dd'] = woon_dd
    obj['woon_hh'] = woon_hh

    # 12운성
    ilgan = saju_dd[0]
    print('일간 :', ilgan)

    # 운성 사주 연
    ji_yy = saju_yyyy[1]
    woonsung_12_yy = get12woonsung(ilgan, ji_yy)
    # 운성 사주 월
    ji_mm = saju_mm[1]
    woonsung_12_mm = get12woonsung(ilgan, ji_mm)
    # 운성 사주 일
    ji_dd = saju_dd[1]
    woonsung_12_dd = get12woonsung(ilgan, ji_dd)
    # 운성 사주 시
    ji_hh = saju_hh[1]
    woonsung_12_hh = get12woonsung(ilgan, ji_hh)
    # 운성 대운
    ji_dea = woon_dea[1]
    woonsung_12_dea = get12woonsung(ilgan, ji_dea)
    # 운성 세운
    ji_ny = woon_yyyy[1]
    woonsung_12_ny = get12woonsung(ilgan, ji_ny)
    # 운성 월운
    ji_nm = woon_mm[1]
    woonsung_12_nb = get12woonsung(ilgan, ji_nm)
    # 운성 일운
    ji_nd = woon_dd[1]
    woonsung_12_nd = get12woonsung(ilgan, ji_nd)
    # 운성 시운
    ji_nh = woon_hh[1]
    woonsung_12_nh = get12woonsung(ilgan, ji_nh)

    woonsug_12 = [
        woonsung_12_yy,
        woonsung_12_mm,
        woonsung_12_dd,
        woonsung_12_hh,
        woonsung_12_dea,
        woonsung_12_ny,
        woonsung_12_nb,
        woonsung_12_nd,
        woonsung_12_nh
    ]
    print(f"십이운성 : {woonsug_12}")

    # 육친
    oh = [obj['wood'], obj['fire'], obj['ground'], obj['gold'], obj['water']]
    oh_rate = [obj['wood_rate'], obj['fire_rate'], obj['ground_rate'], obj['gold_rate'], obj['water_rate']]
    chin6, chin6_rate = get6chin(ilgan, oh, oh_rate)
    print('육친점 :', chin6)
    print('육친율 :', chin6_rate)
    obj['chin6'] = chin6
    obj['chin6_rate'] = chin6_rate

    obj['age'] = age
    obj['woonsug_12'] = woonsug_12
    return obj


if __name__ =='__main__':
    print(Saju(in_year=1994, in_month=8, in_day=1, in_hour=0, in_min=0, sex=1).saju_me())
    # print(Saju(in_year=1995, in_month=10, in_day=13, in_hour=19, in_min=0, sex=1).saju_me_action())
    # print(Saju(in_year=1996, in_month=6, in_day=20, in_hour=11, in_min=0, sex=2).getLuck())
    # print(Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1).getLuck_2())
    # print(Saju(in_year=1996, in_month=2, in_day=23, in_hour=5, in_min=47, sex=2).getLuck_2())
    # print(Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1).music_recommend('health'))
    # print(Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1).music_recommend_of_day('money'))
    # print(Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1).music_recommend('money'))
    # print(Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1).music_recommend_of_day('study'))
    # print(Saju(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0, sex=1).music_recommend('study'))
    # Saju(in_year=1996, in_month=4, in_day=18, in_hour=11, in_min=0, sex=1).get_total_10sin_score()
    # Saju(in_year=2002, in_month=9, in_day=4, in_hour=2, in_min=0, sex=1).get_total_10sin_score()
    # Saju(in_year=1994, in_month=8, in_day=1, in_hour=2, in_min=0, sex=1).get_total_10sin_score()
    # Saju(in_year=1993, in_month=7, in_day=3, in_hour=13, in_min=27, sex=1).get_total_10sin_score()
    # Saju(in_year=1994, in_month=7, in_day=4, in_hour=11, in_min=35, sex=2).get_total_10sin_score()
    # proc_oheng(in_year=1992, in_month=8, in_day=30, in_hour=23, in_min=0)
    # get12woonsung('甲', '子')
