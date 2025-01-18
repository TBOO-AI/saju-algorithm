import math
import csv
import random
import os
from collections import Counter
from datetime import datetime
from functools import reduce

module_dir = os.path.dirname(__file__)
base_file_path = os.path.join(module_dir, '../../saju_data/10sin_{type}.csv')
temperature_file_path = os.path.join(module_dir, '../../saju_data/saju_temperature.csv')
humidity_file_path = os.path.join(module_dir, '../../saju_data/saju_humidity.csv')

class Saju():
    def __init__(self, in_year=0, in_month=0, in_day=0, in_hour=0, in_min=0, sex=1):
        self.PREV_24TERMS = 0
        self.MID_24TERMS = 1
        self.NEXT_24TERMS = 2

        self.me_year = in_year
        self.me_month = in_month
        self.me_day = in_day
        self.me_hour = in_hour
        self.me_min = in_min
        self.sex = sex

        self.m_unityear = 1996
        self.m_unitmonth = 2
        self.m_unitday = 4
        self.m_unithour = 22
        self.m_unitmin = 8

        self.now_year = int(datetime.today().strftime('%Y'))  
        self.now_month = int(datetime.today().strftime('%m'))  
        self.now_day = int(datetime.today().strftime('%d'))   
        self.now_hour = int(datetime.today().strftime('%H'))   
        self.now_min = int(datetime.today().strftime('%M'))   

        self.m_GanjiYear = -1    
        self.m_GanjiMonth = -1   
        self.m_GanjiDay = -1     
        self.m_GanjiHour = -1    

        self.naMonthTable = [0, 21355, 42843, 64498, 86335, 108366, 130578, 152958,
                             175471, 198077, 220728, 243370, 265955, 288432, 310767, 332928,
                             354903, 376685, 398290, 419736, 441060, 462295, 483493, 504693, 525949]

        self.ca24TermsTable = ["입춘", "우수", "경칩", "춘분", "청명", "곡우",
                               "입하", "소만", "망종", "하지", "소서", "대서",
                               "입추", "처서", "백로", "추분", "한로", "상강",
                               "입동", "소설", "대설", "동지", "소한", "대한", "입춘"]  

        self.caGanTable = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]  

        self.caJiTable = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]  

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
                        
                        "1212122322121", "1212121221220", "1121121222120", "2112132122122", "2112112121220",
                        "2121211212120", "2212321121212", "2122121121210", "2122121212120", "1232122121212",
                        
                        "1212121221220", "1121123221222", "1121121212220", "1212112121220", "2121231212121",
                        "2221211212120", "1221212121210", "2123221212121", "2121212212120", "1211212232212",
                        
                        "1211212122210", "2121121212220", "1212132112212", "2212112112210", "2212211212120",
                        "1221412121212", "1212122121210", "2112212122120", "1231212122212", "1211212122210",
                        
                        "2121123122122", "2121121122120", "2212112112120", "2212231212112", "2122121212120",
                        "1212122121210", "2132122122121", "2112121222120", "1211212322122", "1211211221220",
                        
                        "2121121121220", "2122132112122", "1221212121120", "2121221212110", "2122321221212",
                        "1121212212210", "2112121221220", "1231211221222", "1211211212220", "1221123121221",
                        
                        "2221121121210", "2221212112120", "1221241212112", "1212212212120", "1121212212210",
                        "2114121212221", "2112112122210", "2211211412212", "2211211212120", "2212121121210",
                        
                        "2212214112121", "2122122121120", "1212122122120", "1121412122122", "1121121222120",
                        "2112112122120", "2231211212122", "2121211212120", "2212121321212", "2122121121210",
                        
                        "2122121212120", "1212142121212", "1211221221220", "1121121221220", "2114112121222",
                        "1212112121220", "2121211232122", "1221211212120", "1221212121210", "2121223212121",
                        
                        "2121212212120", "1211212212210", "2121321212221", "2121121212220", "1212112112210",
                        "2223211211221", "2212211212120", "1221212321212", "1212122121210", "2112212122120",
                        
                        "1211232122212", "1211212122210", "2121121122210", "2212312112212", "2212112112120",
                        "2212121232112", "2122121212110", "2212122121210", "2112124122121", "2112121221220",
                        
                        "1211211221220", "2121321122122", "2121121121220", "2122112112322", "1221212112120",
                        "1221221212110", "2122123221212", "1121212212210", "2112121221220", "1211231212222",
                        
                        "1211211212220", "1221121121220", "1223212112121", "2221212112120", "1221221232112",
                        "1212212122120", "1121212212210", "2112132212221", "2112112122210", "2211211212210",
                        
                        "2221321121212", "2212121121210", "2212212112120", "1232212122112", "1212122122120",
                        "1121212322122", "1121121222120", "2112112122120", "2211231212122", "2121211212120",
                        
                        "2122121121210", "2124212112121", "2122121212120", "1212121223212", "1211212221220",
                        "1121121221220", "2112132121222", "1212112121220", "2121211212120", "2122321121212",
                        
                        "1221212121210", "2121221212120", "1232121221212", "1211212212210", "2121123212221",
                        "2121121212220", "1212112112220", "1221231211221", "2212211211220", "1212212121210",
                        
                        "2123212212121", "2112122122120", "1211212322212", "1211212122210", "2121121122120",
                        "2212114112122", "2212112112120", "2212121211210", "2212232121211", "2122122121210",
                        
                        "2112122122120", "1231212122212", "1211211221220"]

        self.naDayPerMonthTable = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        '''
         조후용신표: 일간과 월지의 조합, 
         갑: 0, 을: 1, 병: 2, 정: 3, 무: 4, 기: 5, 경: 6, 신: 7, 임: 8, 계: 9
        '''
        self.caJohuTable = ["332669996666",  
                            "222299992992",  
                            "888888888800",  
                            "000600800000",  
                            "222200892200",  
                            "222029992202",  
                            "324308833303",  
                            "225888888888",  
                            "426468974004",  
                            "227627663776"]  

        ''' 현재상태표: 일간과
        현재일시의
        조합(일간, 가로: 시, 세로: 일),
        // 갑: 0, 을: 1, 병: 2, 정: 3, 무: 4, 기: 5, 경: 6, 신: 7, 임: 8, 계: 9
        '''
        self.caCurrentGanTable = [
            
            ["0123329800", "1223238911", "0245452301", "0145452310", "2345328901",
             "2323329810", "2323989801", "8923010189", "0101010101", "0101019801"],
            
            ["0123329800", "1123238911", "0123454501", "0123454501", "2345456701",
             "2345456701", "8923898901", "8923898910", "0101010101", "0101010101"],
            
            ["0123459801", "1123238911", "2323454501", "3323454510", "2345456701",
             "2345456710", "6745456701", "7645456701", "2345450101", "2345450101"],
            
            ["0123329800", "0123238911", "2345454501", "2345454510", "2345456701",
             "2345456710", "2345456701", "3245456701", "0101450101", "0101450101"],
            
            ["3223236723", "1223236723", "2345454501", "2345454510", "2345328901",
             "2323329810", "6645459801", "7774576789", "3245676789", "2345676789"],
            
            ["2223456745", "2223456745", "2345454545", "2223454545", "6745456789",
             "2223679867", "6789676689", "6745456789", "2345676767", "2345676767"],
            
            ["8945668966", "8945238989", "4545458989", "4545458989", "6645456766",
             "6645456711", "8988666701", "9833456789", "0189666701", "0189666701"],
            
            ["8945018989", "8945778989", "6745456789", "8945456789", "6745456776",
             "6745456776", "8989456789", "8989456789", "0189776789", "0189776789"],
            
            ["0123018800", "0123018911", "2223778901", "3301758910", "0167776767",
             "0167776710", "8889776789", "8889776789", "0101016789", "0101016789"],
            
            ["0123018900", "1123018911", "0123678801", "0123678801", "0167678901",
             "0167678910", "2223676789", "3323676789", "0101016789", "0101016789"]]

        ''' 
        현재상태간과 색과의 조합, 
        갑: 0, 을: 1, 병: 2, 정: 3, 무: 4, 기: 5, 경: 6, 신: 7, 임: 8, 계: 9
        '''
        self.caColorGanTable = ["8901678989",  
                                "8945676789",  
                                "0110019801",  
                                "0110019823",  
                                "3223452301",  
                                "2323454501",  
                                "3232454501",  
                                "2323454501",  
                                "3232454545",  
                                "1010458901",  
                                "8810018989",  
                                "0123678901"]  

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
            
            '乙': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
            '丙': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
            
            '丁': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午',  '未'],
            '戊': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
            
            '己': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午',  '未'],
            '庚': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'],
            
            '辛': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
            '壬': ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'],
            
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

    def getMinByTimes(self, in_fromyear, in_frommonth, in_fromday, in_fromhour, in_frommin, in_toyear, in_tomonth, in_today, in_tohour, in_tomin):
        lDayCnt = self.getDayByDays(in_fromyear, in_frommonth, in_fromday, in_toyear, in_tomonth, in_today)
        lTotalCnt = lDayCnt * 24 * 60 + (in_fromhour - in_tohour) * 60 + (in_frommin - in_tomin)

        return lTotalCnt
    
    def getDate2Min(self, in_mincnt, in_year, in_month, in_day, in_hour, in_min):
        out_year = int(in_year - (in_mincnt / 525949))
        out_month = 0

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
    
    def makeGanji(self, in_syear=None, in_smonth=None, in_sday=None, in_shour=None, in_smin=None):
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
        so24 = int(lMinCnt / 525949)  

        if lMinCnt >= 0:
            so24 = so24 + 1

        out_GanjiYear = -1 * (so24 % 60)
        out_GanjiYear = out_GanjiYear + 12

        if out_GanjiYear < 0:
           out_GanjiYear = out_GanjiYear + 60
        if out_GanjiYear > 59:
           out_GanjiYear = out_GanjiYear - 60 

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
           out_GanjiMonth = out_GanjiMonth - 60  

        out_GanjiDay = lDayCnt % 60
        out_GanjiDay = -1 * out_GanjiDay
        out_GanjiDay = out_GanjiDay + 7

        if out_GanjiDay < 0:
           out_GanjiDay = out_GanjiDay + 60
        if out_GanjiDay > 59:
           out_GanjiDay = out_GanjiDay - 60  

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
        out_GanjiHour = t  

        self.m_GanjiYear = math.ceil(out_GanjiYear)
        self.m_GanjiMonth = math.ceil(out_GanjiMonth)
        self.m_GanjiDay = math.ceil(out_GanjiDay)
        self.m_GanjiHour = math.ceil(out_GanjiHour)

        return self.m_GanjiYear, self.m_GanjiMonth, self.m_GanjiDay, self.m_GanjiHour

    def getGanji(self, year=None, month=None, day=None, hour=None, min=None):
        if all(param is None for param in [year, month, day, hour, min]):
            self.makeGanji()
        else:
            self.makeGanji(in_syear=int(year), in_smonth=int(month), 
                          in_sday=int(day), in_shour=int(hour), in_smin=int(min))
            
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

        j = i * 2 + in_type
        tmin = int(lMinCnt + (monthmin100 - self.naMonthTable[j]))
        y, mo, d, h, mi = self.getDate2Min(tmin, self.m_unityear, self.m_unitmonth, self.m_unitday, self.m_unithour, self.m_unitmin)
        

        return n24terms, out_terms24, int(y), int(mo), int(d), int(h), int(mi)
    
    def getOheng(self):
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()
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

    def getLuck(self):
        self.makeGanji()

        out_name = []
        
        nyunGan = self.m_GanjiYear % 10

        if nyunGan % 2 == 0:  
            bPlus = True
            intPlus = 1
        else:  
            bPlus = False
            intPlus = 0

        if intPlus + self.sex == 2:  
            bAscending = True
        else:  
            bAscending = False

        PREV_24TERMS, terms24_1, prev_year, prev_month, prev_day, prev_hour, prev_min = self.get24terms(self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min, self.PREV_24TERMS)
        MID_24TERMS, terms24_2, mid_year, mid_month, mid_day, mid_hour, mid_min = self.get24terms(self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min, self.MID_24TERMS)
        NEXT_24TERMS, terms24_3, next_year, next_month, next_day, next_hour, next_min = self.get24terms(self.me_year, self.me_month, self.me_day, self.me_hour, self.me_min, self.NEXT_24TERMS)
        sDate = int(self.me_year * 10000 + self.me_month * 100 + self.me_day)
        prevDate = int(prev_year * 10000 + prev_month * 100 + prev_day)
        midDate = int(mid_year * 10000 + mid_month * 100 + mid_day)

        if bAscending:  
            if sDate > prevDate:  
                nDays = self.getDayByDays(next_year, next_month, next_day, self.me_year, self.me_month, self.me_day)
            elif sDate < prevDate:  
                nDays = self.getDayByDays(prev_year, prev_month, prev_day, self.me_year, self.me_month, self.me_day)
        else:  
            if sDate > prevDate:  
                nDays = self.getDayByDays(self.me_year, self.me_month, self.me_day, prev_year, prev_month, prev_day)
            elif sDate < prevDate:  
                
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
        daily_list = [self.getGanji(year=year, month=month, day=day, hour=hour, min=min)[3][0] for hour in range(0, 24, 2)]
        daily_weather_dict = {mapper_list[idx]: weather_mapper[self.weather_table_case1[si_ju_gan][il_gan_idx]] for idx, si_ju_gan in enumerate(daily_list)}

        return daily_weather_dict

    def get_season(self, dae_won_ji):
        array_12 = self.table_12[self.get_me_il_gan()]
        index = array_12.index(dae_won_ji)
        woonsung_12 = self.table_woonsung[index]
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
        month, season = self.get_season(dea_won[1])
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
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()
        now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=self.now_year, in_smonth=self.now_month,
                                                                                       in_sday=self.now_day, in_shour=self.now_hour,
                                                                                       in_smin=self.now_min)
        dae_won_dict = self.get_dae_won()
        dae_won_idx = self.caGanjiTable.index(dae_won_dict["dae_won"])

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

        
        dae_won_dict = self.get_dae_won()
        dae_won_idx = self.caGanjiTable.index(dae_won_dict["dae_won"])

        
        _10sin_year = self.get_10sin("year", yeon_ju_idx)

        _10sin_month = self.get_10sin("month", wol_ju_idx)

        _10sin_day = self.get_10sin("day", il_ju_idx)

        _10sin_time = self.get_10sin("time", si_ju_idx)

        _10sin_dae_won = self.get_10sin("big_luck", dae_won_idx)

        _10sin_year_luck = self.get_10sin("year_luck", now_yeon_ju_idx)

        _10sin_month_luck = self.get_10sin("month_luck", now_wol_ju_idx)

        _10sin_day_luck = self.get_10sin("day_luck", now_il_ju_idx)

        _10sin_time_luck = self.get_10sin("time_luck", now_si_ju_idx)

        dicts = [_10sin_year, _10sin_month, _10sin_day, _10sin_time, _10sin_dae_won, _10sin_year_luck,
                 _10sin_month_luck, _10sin_day_luck, _10sin_time_luck]
        total_10sin_score = reduce(lambda a, b: a.update(b) or a, dicts, Counter())
        return total_10sin_score

    def get_10sin_score_100_percent(self):
        yeon_ju_idx, wol_ju_idx, il_ju_idx, si_ju_idx = self.makeGanji()

        now_yeon_ju_idx, now_wol_ju_idx, now_il_ju_idx, now_si_ju_idx = self.makeGanji(in_syear=self.now_year, in_smonth=self.now_month,
                                                                                       in_sday=self.now_day, in_shour=self.now_hour,
                                                                                       in_smin=self.now_min)

        
        dae_won_dict = self.get_dae_won()
        dae_won_idx = self.caGanjiTable.index(dae_won_dict["dae_won"])

        
        _10sin_year = self.get_10sin("year", yeon_ju_idx)

        _10sin_month = self.get_10sin("month", wol_ju_idx)

        _10sin_day = self.get_10sin("day", il_ju_idx)

        _10sin_time = self.get_10sin("time", si_ju_idx)

        _10sin_dae_won = self.get_10sin("big_luck", dae_won_idx)

        _10sin_year_luck = self.get_10sin("year_luck", now_yeon_ju_idx)

        _10sin_month_luck = self.get_10sin("month_luck", now_wol_ju_idx)

        _10sin_day_luck = self.get_10sin("day_luck", now_il_ju_idx)

        _10sin_time_luck = self.get_10sin("time_luck", now_si_ju_idx)

        dicts = [_10sin_year, _10sin_month, _10sin_day, _10sin_time, _10sin_dae_won, _10sin_year_luck,
                 _10sin_month_luck, _10sin_day_luck, _10sin_time_luck]


        total_10sin_score = reduce(lambda a, b: a.update(b) or a, dicts, Counter())
        _10sin_score = dict(
            zip(total_10sin_score.keys(), map(lambda x: round((x[1] / 375) * 100, 1), total_10sin_score.items())))

        return _10sin_score
    
    def get_luck_score(self):
        
        _10sin_score = self.get_10sin_score_100_percent()
        reference_score = [9.5, 9.3, 9.5, 9.3, 9.5, 7.8, 14.7, 11.5, 9.5, 9.3]
        reference_score_dict = dict(zip(_10sin_score.keys(), reference_score))

        if self.sex == 1:
            reference_luck_score = {
                "love": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1 / 2) + (reference_score_dict["식신"] + reference_score_dict["상관"]) * (1 / 2),
                "wealth": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1 / 2) + (
                            reference_score_dict["식신"] + reference_score_dict["상관"]) * (1 / 2) + (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1 / 2),
                "study": (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1/2) + (reference_score_dict["편인"] + reference_score_dict["정인"]) * (1/2),
                "health": (reference_score_dict["비견"] + reference_score_dict["겁재"])
            }
        else:
            reference_luck_score = {
                "love": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1/2) + (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1/2) + (reference_score_dict["식신"] + reference_score_dict["상관"]) * (1/2),
                "wealth": (reference_score_dict["편재"] + reference_score_dict["정재"]) * (1/2) + (reference_score_dict["식신"] + reference_score_dict["상관"]) * (1/2),
                "study": (reference_score_dict["편관"] + reference_score_dict["정관"]) * (1/2) + (reference_score_dict["편인"] + reference_score_dict["정인"]) * (1/2),
                "health": (reference_score_dict["비견"] + reference_score_dict["겁재"])
            }

        if self.sex == 1:
            luck_score = {
                "love": (_10sin_score["편재"] + _10sin_score["정재"]) * (1 / 2) + (_10sin_score["식신"] + _10sin_score["상관"]) * (1 / 2),
                "wealth": (_10sin_score["편재"] + _10sin_score["정재"]) * (1 / 2) + (
                            _10sin_score["식신"] + _10sin_score["상관"]) * (1 / 2) + (_10sin_score["편관"] + _10sin_score["정관"]) * (1 / 2),
                "study": (_10sin_score["편관"] + _10sin_score["정관"]) * (1/2) + (_10sin_score["편인"] + _10sin_score["정인"]) * (1/2),
                "health": (_10sin_score["비견"] + _10sin_score["겁재"])
            }
        else:
            luck_score = {
                "love": (_10sin_score["편재"] + _10sin_score["정재"]) * (1/2) + (_10sin_score["편관"] + _10sin_score["정관"]) * (1/2) + (_10sin_score["식신"] + _10sin_score["상관"]) * (1/2),
                "wealth": (_10sin_score["편재"] + _10sin_score["정재"]) * (1/2) + (_10sin_score["식신"] + _10sin_score["상관"]) * (1/2),
                "study": (_10sin_score["편관"] + _10sin_score["정관"]) * (1/2) + (_10sin_score["편인"] + _10sin_score["정인"]) * (1/2),
                "health": (_10sin_score["비견"] + _10sin_score["겁재"])
            }

        result = {
            "love": 50 + self.calculator(round(reference_luck_score["love"], 2), round(luck_score["love"], 2))
            if round(reference_luck_score["love"], 2) < round(luck_score["love"], 2)
            else 50 - self.calculator(round(reference_luck_score["love"], 2), round(luck_score["love"], 2)),
            "wealth": 50 + self.calculator(round(reference_luck_score["wealth"], 2), round(luck_score["wealth"], 2))
            if round(reference_luck_score["wealth"], 2) < round(luck_score["wealth"], 2)
            else 50 - self.calculator(round(reference_luck_score["wealth"], 2), round(luck_score["wealth"], 2)),
            "study": 50 + self.calculator(round(reference_luck_score["study"], 2), round(luck_score["study"], 2))
            if round(reference_luck_score["study"], 2) < round(luck_score["study"], 2)
            else 50 - self.calculator(round(reference_luck_score["study"], 2), round(luck_score["study"], 2)),
            "health": 50 + self.calculator(round(reference_luck_score["health"], 2), round(luck_score["health"], 2))
            if round(reference_luck_score["health"], 2) < round(luck_score["health"], 2)
            else 50 - self.calculator(round(reference_luck_score["health"], 2), round(luck_score["health"], 2)),
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
            "oheang_score": self.getOheng(),
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
            "now_dae_won": self.get_dae_won()['now_dae_won'],
        }

    @staticmethod
    def calculator(ref, x):
        return round((abs(ref - x) / ref) * 55)


if __name__ =='__main__':
    print(Saju(in_year=1994, in_month=8, in_day=1, in_hour=0, in_min=0, sex=1).saju_me())