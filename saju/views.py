
from datetime import datetime
from django.http import JsonResponse
import os
import csv
from saju.saju_algorithm.saju import Saju
from saju.saju_algorithm.saju_calendar import SajuCalendar


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

def saju(request):
    birth_date = request.GET.get('birth_date')
    birth_time = request.GET.get('birth_time')
    gender = request.GET.get('gender')

    if not all([birth_date, birth_time, gender]):
        return JsonResponse({
            "error": "Required parameters are missing. (birth_date, birth_time, gender)"
        }, status=400)

    if gender.lower() not in ['male', 'female']:
        return JsonResponse({
            "error": "Gender must be either 'male' or 'female'."
        }, status=400)
    
    try:

        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return JsonResponse({
            "error": "Invalid date/time format. (YYYY-MM-DD HH:MM)"
        }, status=400)
    
    sex = 1 if gender.lower() == 'male' else 2

    saju_dict = Saju(
        in_year=birth_datetime.year,
        in_month=birth_datetime.month,
        in_day=birth_datetime.day,
        in_hour=birth_datetime.hour,
        in_min=birth_datetime.minute,
        sex=sex
    ).saju_me_action()

    il_gan_dict = {"甲": "갑", "乙": "을", "丙": "병", "丁": "정", "戊": "무", "己": "기", "庚": "경", "辛": "신", "壬": "임",
                   "癸": "계"}

    oheang_rate = saju_dict["oheang_score"]
    most_oheang = [k for k, v in saju_dict["oheang_score"].items() if max(saju_dict["oheang_score"].values()) == v]
    il_gan = saju_dict["il_gan"]
    il_ju = saju_dict["il_ju"]

    print(saju_dict)
    print(saju_dict['way'])
    print(saju_dict['dae_won'])

    character = next(
        (char for char in CHARACTER_DICT 
        if il_gan_dict[il_gan] in char["il_gan"]),
        None
    )

    if character is None:
        return JsonResponse({"error": "No matching character found."}, status=404)
    
    with open(oheang_saju_file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        filtered_saju = next(
            (row for row in rows 
            if int(row['character']) == character["id"] and row['most_oheang'] == most_oheang[0]),
            None
        )

    with open(il_ju_saju_file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        filtered_il_ju = next(
            (row for row in rows 
            if row['il_ju'] == il_ju),
            None
        )
    
    if filtered_saju is None:
        return JsonResponse({"error": "No matching Saju data found."}, status=404)
    

    return JsonResponse({
        "status": "success",
        "data": {
            "character": character,
            "saju": filtered_saju, 
            "il_ju": filtered_il_ju, 
            "oheang_rate": oheang_rate,
            "now_dae_won": saju_dict['dae_won'],
            "dae_won_flow": saju_dict['dae_won_flow'],
            "luck_score": saju_dict["luck_score"], 
            "saju_score": saju_dict["saju_score"], 
            "dae_won_su": saju_dict["dae_won_su"]
        }
    })


def saju_calendar(request):
    print("saju_calendar")
    birth_date = request.GET.get('birth_date')
    birth_time = request.GET.get('birth_time')
    gender = request.GET.get('gender')

    if not all([birth_date, birth_time, gender]):
        return JsonResponse({
            "error": "Required parameters are missing. (birth_date, birth_time, gender)"
        }, status=400)

    if gender.lower() not in ['male', 'female']:
        return JsonResponse({
            "error": "Gender must be either 'male' or 'female'."
        }, status=400)

    try:

        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return JsonResponse({
            "error": "Invalid date/time format. (YYYY-MM-DD HH:MM)"
        }, status=400)

    sex = 1 if gender.lower() == 'male' else 2

    saju_dict = SajuCalendar(
        in_year=birth_datetime.year,
        in_month=birth_datetime.month,
        in_day=birth_datetime.day,
        in_hour=birth_datetime.hour,
        in_min=birth_datetime.minute,
        sex=sex
    ).get()

    print(saju_dict)
    return JsonResponse({
        "status": "success",
        "data": saju_dict
    })