import json

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

# 영화 제목 리스트를 정렬
filtered_titles_2016_2023_sorted = sorted(filtered_titles_2016_2023)
unique_successful_titles_sorted = sorted(unique_successful_titles)

# 제목이 일치하지 않는 항목 찾기
# for i in range(min(len(filtered_titles_2016_2023_sorted), len(unique_successful_titles_sorted))):
#     if filtered_titles_2016_2023_sorted[i] != unique_successful_titles_sorted[i]:
#         print(f"차이 나는 제목: {filtered_titles_2016_2023_sorted[i]} vs {unique_successful_titles_sorted[i]}")

# 나머지 항목 출력
if len(filtered_titles_2016_2023_sorted) > len(unique_successful_titles_sorted):
    print("추가된 제목들:", filtered_titles_2016_2023_sorted[len(unique_successful_titles_sorted):])
elif len(unique_successful_titles_sorted) > len(filtered_titles_2016_2023_sorted):
    print("추가된 제목들:", unique_successful_titles_sorted[len(filtered_titles_2016_2023_sorted):])
