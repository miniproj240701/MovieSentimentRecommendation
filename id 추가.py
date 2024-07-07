import json

# 영화 정보 데이터셋 파일 불러오기
with open('영화정보데이터셋.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 영화 데이터가 리스트 형태인 경우 id 인덱스 추가
if isinstance(data, list):
    updated_data = []
    for idx, movie in enumerate(data):
        movie_with_id = {"id": idx + 1}
        movie_with_id.update(movie)
        updated_data.append(movie_with_id)
else:
    # 단일 영화 데이터인 경우 id를 1로 설정
    movie_with_id = {"id": 1}
    movie_with_id.update(data)
    updated_data = movie_with_id

# 업데이트된 데이터셋을 다시 JSON 파일로 저장
with open('영화정보데이터셋_with_id.json', 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, ensure_ascii=False, indent=4)

# 업데이트된 데이터셋 확인
print(json.dumps(updated_data, ensure_ascii=False, indent=4))
