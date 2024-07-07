import json

# 영화리스트.json 파일 읽기
with open('영화리스트.json', 'r', encoding='utf-8') as f:
    successful_movies = json.load(f)

# 성공한 영화 제목 목록 추출
successful_titles = {movie['영화명'] for movie in successful_movies}

# 2016-2024_6_Korean_Movie_List_824_Movies.json 파일 읽기
with open('2016-2024_6_Korean_Movie_List_824_Movies.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 데이터 상태 확인
print(f"성공한 영화 제목 목록: {successful_titles}")

# 성공한 영화 제목에 따라 데이터 필터링
filtered_data = {
    year: {
        month: [
            movie for movie in data[year][month] 
            if movie['Title'] in successful_titles
        ]
        for month in data[year]
    }
    for year in data
}

# 필터링되지 않은 영화 목록과 비교 내용
unfiltered_data = {
    year: {
        month: [
            (movie, movie['Title'] in successful_titles) for movie in data[year][month] 
            if movie['Title'] not in successful_titles
        ]
        for month in data[year]
    }
    for year in data
}

# 빈 달 제거
filtered_data = {
    year: {month: filtered_data[year][month] for month in filtered_data[year] if filtered_data[year][month]}
    for year in filtered_data
}

unfiltered_data = {
    year: {month: unfiltered_data[year][month] for month in unfiltered_data[year] if unfiltered_data[year][month]}
    for year in unfiltered_data
}

# 빈 해 제거
filtered_data = {year: filtered_data[year] for year in filtered_data if filtered_data[year]}
unfiltered_data = {year: unfiltered_data[year] for year in unfiltered_data if unfiltered_data[year]}

# 최소년도와 최대년도 계산
years = list(filtered_data.keys())
min_year = min(years)
max_year = max(years)

# 영화 갯수 계산
movie_count = sum(len(filtered_data[year][month]) for year in filtered_data for month in filtered_data[year])

# 파일 이름 생성
output_path = f'{min_year}-{max_year}_Korean_Movie_List_{movie_count}_Movies.json'

# 필터링된 데이터를 새로운 JSON 파일로 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print(f"필터링된 데이터를 {output_path} 파일로 저장했습니다.")

# 필터링된 영화 목록 출력
print("필터링된 영화 목록:")
for year in filtered_data:
    for month in filtered_data[year]:
        for movie in filtered_data[year][month]:
            print(f"L|제목: {movie['Title']}, 감독: {movie['Director']}")

# 필터링되지 않은 영화 목록 출력 및 비교 내용
print("\n필터링되지 않은 영화 목록 및 비교 내용:")
for year in unfiltered_data:
    for month in unfiltered_data[year]:
        for movie, is_successful in unfiltered_data[year][month]:
            if not is_successful:
                # 비교 내용을 출력
                title_matches = [t for t in successful_titles if t == movie['Title']]
                comparison_result = f"제목 매칭: {title_matches}"
                print(f"R|제목: {movie['Title']}, 감독: {movie['Director']} - 비교 내용: {comparison_result}")
