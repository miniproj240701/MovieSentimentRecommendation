import json

# JSON 파일 읽기
with open('2016-2024_6_Korean_Movie_List_824_Movies.json', 'r', encoding='utf-8') as f:
    data_2016_2024 = json.load(f)

with open('영화리스트.json', 'r', encoding='utf-8') as f:
    successful_movies = json.load(f)

# 전체 영화 제목 추출 및 전처리
movies_all = [
    movie['Title'].strip().lower()
    for year in data_2016_2024
    for month in data_2016_2024[year]
    for movie in data_2016_2024[year][month]
]

# 영화리스트.json에서 영화 제목 추출 및 전처리
movies_successful = [movie['영화명'].strip().lower() for movie in successful_movies]

# 중복된 제목 제거
unique_movies_all = list(set(movies_all))
unique_movies_successful = list(set(movies_successful))

# 동일한 영화 제목 찾기
common_movies = set(unique_movies_all).intersection(set(unique_movies_successful))

# 영화리스트에 남은(2016-2024 JSON에 없는) 영화 제목 찾기
remaining_movies = set(unique_movies_successful) - set(unique_movies_all)

# 추출한 제목 비교 및 출력
print(f"2016-2024 JSON 파일의 총 영화 수: {len(unique_movies_all)}")
print(f"영화리스트 JSON 파일의 총 영화 수: {len(unique_movies_successful)}")
print(f"동일한 영화 제목의 총 갯수: ✔ {len(common_movies)}")
print(f"영화리스트 JSON 파일에 포함되지 않은 영화 제목의 총 갯수: ✘ {len(remaining_movies)}")

if len(remaining_movies) > 0:
    print("\n영화리스트 JSON 파일에 포함되지 않은 영화 제목 목록:")
    for title in remaining_movies:
        print(f"✘ {title}")
else:
    print("\n모든 영화 제목이 2016-2024 JSON 파일에 포함되어 있습니다.")

# 영화리스트 JSON에 있지만 2016-2024 JSON에 없는 영화 출력
print("\n2016-2024 JSON 파일에 포함되지 않은 영화 제목 목록:")
for title in remaining_movies:
    print(f"✘ {title}")

# 중복 확인을 위한 리스트 출력
duplicate_titles_all = [title for title in movies_all if movies_all.count(title) > 1]
duplicate_titles_successful = [title for title in movies_successful if movies_successful.count(title) > 1]

if duplicate_titles_all:
    print("\n2016-2024 JSON 파일의 중복된 영화 제목 목록:")
    for title in set(duplicate_titles_all):
        print(f"✘ {title}")

if duplicate_titles_successful:
    print("\n영화리스트 JSON 파일의 중복된 영화 제목 목록:")
    for title in set(duplicate_titles_successful):
        print(f"✘ {title}")

# 원래 영화 제목 목록으로 복원하여 출력
original_remaining_movies = [movie['영화명'] for movie in successful_movies if movie['영화명'].strip().lower() in remaining_movies]

print("\n원래 영화리스트 JSON 파일에 포함되지 않은 영화 제목 목록:")
for title in original_remaining_movies:
    print(f"✘ {title}")
