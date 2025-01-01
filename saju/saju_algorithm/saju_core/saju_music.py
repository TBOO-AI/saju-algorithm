from datetime import datetime


class SajuMusic():
    def __init__(self):
        self.m_mday = 0

        self.caJosengTable = [
            ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"],
            ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]]

        self.naGanJiTable = [2, 3, 5, 6, -1, -1, 8, 9, 11, 0]

    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # // Name: getJoseng
    # // Desc: 일간과 현재일시를 이용하여 현재의 간을 구한다.
    # // Input: int in_gan : 현재간의 array
    # //							  (갑:0 ,을:1 ,병:2 ,정:3 ,무:4 ,기:5 ,경:6 ,신:7 ,임:8 ,계:9)
    # //  Output : char *out_name: 추출한 음악 조성 명
    # //= == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    def getJoseng(self, in_gan, m_GanjiDay):
        nJi = 0

        # 간이 무, 기인 경우
        if in_gan == 4 or in_gan == 5:
            if in_gan == 4:
                # 무면 메이저
                nMajorMinor = 0
            else:
                # 기면 마이너
                nMajorMinor = 1

            # 현재시간 일자
            day = datetime.today().strftime('%m%d')

            if '0204' <= day <= '0504':
                # 양력 2 월 4 일부터 5 월 4 일까지 - -진
                nJi = 4
            elif '0505' <= day <= '0806':
                # 양력 5월 5일부터 8월 6일까지--미
                nJi = 7
            elif '0807' <= day <= '1008':
                # 양력 8월 7일부터 10월8일까지--술
                nJi = 10
            else:
                # 양력 10월9일부터 2월 3일까지--축
                nJi = 1
        else:
            ilGan = m_GanjiDay % 10  # 일간을 구한다.
            # "甲", "丙", "戊", "庚", "壬": 양끼리 조합 또는
            # "乙", "丁", "己", "辛", "癸": 음끼리 조합이면 메이저
            if ((ilGan % 2 == 0) and (in_gan % 2 == 0)) or ((ilGan % 2 == 1) and (in_gan % 2 == 1)):
                nMajorMinor = 0
            else:
                nMajorMinor = 1

            nJi = self.naGanJiTable[in_gan]

        out_name = self.caJosengTable[nMajorMinor][nJi]
        # print(in_gan, nMajorMinor, nJi, out_name)

        return out_name
