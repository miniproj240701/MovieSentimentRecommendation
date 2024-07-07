import json

# 전체 영화 목록 불러오기
with open('2016-2024_Korean_Movie_List_912_Movies.json', 'r', encoding='utf-8') as file:
    full_movie_data = json.load(file)

# 실패한 영화 목록 불러오기
with open('failure_movies_final.json', 'r', encoding='utf-8') as file:
    failed_movies = json.load(file)

# 실패한 영화 제목 집합 생성
failed_titles = set(movie['Title'] for movie in failed_movies)

# 실패한 영화를 제외하고 새로운 영화 목록 생성
filtered_movies = {}
movie_count = 0  # 영화 수를 세기 위한 변수
for year, months in full_movie_data.items():
    if year not in filtered_movies:
        filtered_movies[year] = {}
    for month, movies in months.items():
        filtered_list = [movie for movie in movies if movie['Title'] not in failed_titles]
        filtered_movies[year][month] = filtered_list
        movie_count += len(filtered_list)  # 필터링된 목록의 영화 수를 추가

# 필터링된 영화 목록을 새 파일에 저장
filtered_file_name = f"2016-2024_Korean_Movie_List_{movie_count}_Movies.json"
with open(filtered_file_name, 'w', encoding='utf-8') as file:
    json.dump(filtered_movies, file, ensure_ascii=False, indent=4)

print(f"필터링된 영화 목록이 '{filtered_file_name}' 파일에 저장되었습니다.")
