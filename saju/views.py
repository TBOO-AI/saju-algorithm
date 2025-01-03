# example/views.py
from datetime import datetime
from django.http import JsonResponse  # 상단에 import 추가
import os
import csv
from django.http import HttpResponse
from saju.saju_algorithm.saju_core.saju import Saju


module_dir = os.path.dirname(__file__)
oheang_saju_file_path = os.path.join(module_dir, 'saju_data/oheang_saju.csv')
il_ju_saju_file_path = os.path.join(module_dir, 'saju_data/il_ju_saju.csv')

CHARACTER_DICT = [
    { "id": 1, "element": "수", "name_ko": "모빈", "name_en" : "MoVin", "for_me": 2, "to_me": 3, "il_gan": ["임", "계"]},
    { "id": 2, "element": "금", "name_ko": "저스팃", "name_en" : "JUSTit", "for_me": 3, "to_me": 4, "il_gan": ["경", "신"]},
    { "id": 3, "element": "토", "name_ko": "무디", "name_en" : "Moodey", "for_me": 4, "to_me": 5, "il_gan": ["무", "기"]},
    { "id": 4, "element": "화", "name_ko": "딘", "name_en" : "Diin", "for_me": 5, "to_me": 1, "il_gan": ["병", "정"]},
    { "id": 5, "element": "목", "name_ko": "유피", "name_en" : "YuPEE", "for_me": 1, "to_me": 2, "il_gan": ["갑", "을"]},
]



def index(request):

    saju = Saju(in_year=int(1995), in_month=int(2), in_day=int(25), in_hour=int(10),
         in_min=int(0),
         sex=int(1))

    my_saju = saju.saju_me()
    print(my_saju)

    return JsonResponse(my_saju)


def character(request):

    # 날짜, 시간, 성별 데이터 받기
    birth_date = request.GET.get('birth_date')  # "1995-02-25" 형식
    birth_time = request.GET.get('birth_time')  # "10:00" 형식
    gender = request.GET.get('gender')  # "male" 또는 "female"

     # 필수 값 검사
    if not all([birth_date, birth_time, gender]):
        return JsonResponse({
            "error": "필수 파라미터가 누락되었습니다. (birth_date, birth_time, gender)"
        }, status=400)

    # 성별 값 검사
    if gender.lower() not in ['male', 'female']:
        return JsonResponse({
            "error": "성별은 'male' 또는 'female'이어야 합니다."
        }, status=400)
    
    try:
        # 날짜와 시간 파싱
        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return JsonResponse({
            "error": "날짜/시간 형식이 올바르지 않습니다. (YYYY-MM-DD HH:MM)"
        }, status=400)
    
    # 성별 변환 (male=1, female=2)
    sex = 1 if gender.lower() == 'male' else 2

    saju_dict = Saju(
        in_year=birth_datetime.year,
        in_month=birth_datetime.month,
        in_day=birth_datetime.day,
        in_hour=birth_datetime.hour,
        in_min=birth_datetime.minute,
        sex=sex
    ).saju_me_action()

    print(saju_dict)
    il_gan_dict = {"甲": "갑", "乙": "을", "丙": "병", "丁": "정", "戊": "무", "己": "기", "庚": "경", "辛": "신", "壬": "임",
                   "癸": "계"}

    oheang_rate = saju_dict["oheang_score"]
    most_oheang = [k for k, v in saju_dict["oheang_score"].items() if max(saju_dict["oheang_score"].values()) == v]
    il_gan = saju_dict["il_gan"]
    il_ju = saju_dict["il_ju"]
    print("il_ju", il_ju)
    character = next(
        (char for char in CHARACTER_DICT 
        if il_gan_dict[il_gan] in char["il_gan"]),
        None
    )

    if character is None:
        return JsonResponse({"error": "일치하는 캐릭터를 찾을 수 없습니다."}, status=404)
    
    # 캐릭터 사주를 가져온다.
    with open(oheang_saju_file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        filtered_saju = next(
            (row for row in rows 
            if int(row['character']) == character["id"] and row['most_oheang'] == most_oheang[0]),
            None
        )

    # 캐릭터 사주를 가져온다.
    with open(il_ju_saju_file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        filtered_il_ju = next(
            (row for row in rows 
            if row['il_ju'] == il_ju),
            None
        )
    
    if filtered_saju is None:
        return JsonResponse({"error": "일치하는 사주 데이터를 찾을 수 없습니다."}, status=404)
    

    return JsonResponse({"character": character, "saju": filtered_saju, "il_ju": filtered_il_ju, "oheang_rate": oheang_rate})


