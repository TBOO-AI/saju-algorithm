import pandas as pd

# Load the uploaded CSV file
file_path = "./TBOO 데이터셋.xlsx - 오행-사주.csv"
data = pd.read_csv(file_path)

desc_character_dict = []
id_counter = 1

for _, row in data.iterrows():
    desc_character_dict.append({
        "id": id_counter,
        "character": row["캐릭터"].split("-")[1],  # Extract character type
        "most_oheang": row["최고 비율 오행"],
        "content_ko": row["내용"],
        "content_en": row["내용 영어"]
    })
    id_counter += 1

desc_character_dict
