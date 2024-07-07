import json

# 영화리스트.json 파일 읽기
with open('영화리스트.json', 'r', encoding='utf-8') as f:
    successful_movies = json.load(f)

# 2016-2024_6_Korean_Movie_List_824_Movies.json 파일 읽기
with open('2016-2024_6_Korean_Movie_List_824_Movies.json', 'r', encoding='utf-8') as f:
    data_2016_2024 = json.load(f)

# 성공한 영화 제목 목록 추출
successful_titles = [movie['영화명'] for movie in successful_movies]

# 2016-2024 데이터에서 연도를 기반으로 성공한 영화 제목과 매칭하여 연도를 채워 넣기
for movie in successful_movies:
    if not movie['개봉년도']:
        for year in data_2016_2024:
            for month in data_2016_2024[year]:
                for item in data_2016_2024[year][month]:
                    if item['Title'] == movie['영화명']:
                        movie['개봉년도'] = year
                        break

# 2016-2023 기간 동안의 성공한 영화 필터링
filtered_data = {
    year: {month: [movie for movie in data_2016_2024[year][month] if movie['Title'] in successful_titles]
           for month in data_2016_2024[year]}
    for year in data_2016_2024 if int(year) >= 2016 and int(year) <= 2023
}

# 빈 달 제거
filtered_data = {
    year: {month: filtered_data[year][month] for month in filtered_data[year] if filtered_data[year][month]}
    for year in filtered_data
}

# 빈 해 제거
filtered_data = {year: filtered_data[year] for year in filtered_data if filtered_data[year]}

# 파일 이름 생성
output_path_1 = '2016-2023_Korean_Movie_List_574_Movies.json'

# 필터링된 데이터를 새로운 JSON 파일로 저장
with open(output_path_1, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# 중복된 영화 제목 제거 및 리뷰 내용이 공백인 항목 제거
unique_successful_movies = []
seen_titles = set()
for movie in successful_movies:
    if movie['영화명'] not in seen_titles:
        # 리뷰 내용이 공백인 항목 제거
        movie["리뷰"] = [review for review in movie["리뷰"] if review["리뷰내용"].strip()]
        unique_successful_movies.append(movie)
        seen_titles.add(movie['영화명'])

# 파일 이름 생성
output_path_2 = '영화정보리스트.json'

# 고유한 성공한 영화 목록을 새로운 JSON 파일로 저장
with open(output_path_2, 'w', encoding='utf-8') as f:
    json.dump(unique_successful_movies, f, ensure_ascii=False, indent=4)

print(f"필터링된 데이터를 {output_path_1} 파일로 저장했습니다.")
print(f"고유한 성공한 영화 목록을 {output_path_2} 파일로 저장했습니다.")

# 저장된 파일 불러오기
with open('2016-2023_Korean_Movie_List_574_Movies.json', 'r', encoding='utf-8') as f:
    filtered_movies_2016_2023 = json.load(f)

with open('영화정보리스트.json', 'r', encoding='utf-8') as f:
    unique_successful_movies = json.load(f)

# 필터링된 영화 제목 추출
filtered_titles_2016_2023 = [
    movie['Title']
    for year in filtered_movies_2016_2023
    for month in filtered_movies_2016_2023[year]
    for movie in filtered_movies_2016_2023[year][month]
]

# 고유한 성공한 영화 제목 추출
unique_successful_titles = [movie['영화명'] for movie in unique_successful_movies]

# 제목 일치 여부 확인
common_titles = set(filtered_titles_2016_2023).intersection(set(unique_successful_titles))
missing_in_filtered = set(unique_successful_titles) - set(filtered_titles_2016_2023)
missing_in_successful = set(filtered_titles_2016_2023) - set(unique_successful_titles)

print(f"2016-2023 JSON 파일의 총 영화 수: {len(filtered_titles_2016_2023)}")
print(f"고유한 성공한 영화 목록의 총 영화 수: {len(unique_successful_titles)}")
print(f"동일한 영화 제목의 총 갯수: ✔ {len(common_titles)}")

if missing_in_filtered:
    print(f"2016-2023 JSON 파일에 포함되지 않은 영화 제목의 총 갯수: ✘ {len(missing_in_filtered)}")
    print("\n2016-2023 JSON 파일에 포함되지 않은 영화 제목 목록:")
    for title in missing_in_filtered:
        print(f"✘ {title}")
else:
    print("모든 고유한 성공한 영화 제목이 2016-2023 JSON 파일에 포함되어 있습니다.")

if missing_in_successful:
    print(f"고유한 성공한 목록에 포함되지 않은 영화 제목의 총 갯수: ✘ {len(missing_in_successful)}")
    print("\n고유한 성공한 목록에 포함되지 않은 영화 제목 목록:")
    for title in missing_in_successful:
        print(f"✘ {title}")
else:
    print("모든 2016-2023 JSON 파일의 영화 제목이 고유한 성공한 목록에 포함되어 있습니다.")
