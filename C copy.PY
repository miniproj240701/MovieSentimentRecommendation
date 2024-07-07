import torch
from PIL import Image
import open_clip
import os
from tqdm import tqdm
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# CLIP 모델 및 전처리기 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
model = model.to(device)

# 텍스트 벡터화를 위한 TF-IDF 벡터라이저 초기화
tfidf = TfidfVectorizer()

def extract_features(image_path, plot, genre):
    # 이미지 특징 추출
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    
    # 줄거리 특징 추출
    plot_features = tfidf.transform([plot]).toarray().flatten()
    
    # 장르를 원-핫 인코딩
    genre_features = np.zeros(len(all_genres))
    genre_features[all_genres.index(genre)] = 1
    
    # 특징 결합
    combined_features = np.concatenate([image_features.cpu().numpy().flatten(), plot_features, genre_features])
    
    return combined_features

def compare_all_images(poster_folder, movie_data, top_n=10):
    total_images = len(movie_data)
    all_features = {}

    # 모든 줄거리로 TF-IDF 모델 학습
    all_plots = [movie['줄거리'] for movie in movie_data]
    tfidf.fit(all_plots)

    for i, movie in tqdm(enumerate(movie_data), desc="특징 추출 중", total=total_images):
        filename = f"poster_{i}.jpg"
        image_path = os.path.join(poster_folder, filename)
        if os.path.exists(image_path):
            features = extract_features(image_path, movie['줄거리'], movie['장르'])
            all_features[filename] = features
        else:
            print(f"경고: {filename}를 찾을 수 없습니다")

    similarities = {}

    for i, movie in tqdm(enumerate(movie_data), desc="이미지 비교 중", total=total_images):
        filename1 = f"poster_{i}.jpg"
        if filename1 not in all_features:
            continue
        
        similarities[filename1] = []
        for filename2, features2 in all_features.items():
            if filename1 == filename2:
                continue
            
            similarity = np.dot(all_features[filename1], features2) / (np.linalg.norm(all_features[filename1]) * np.linalg.norm(features2))
            similarities[filename1].append({"파일명": filename2, "유사도": float(similarity)})
        
        similarities[filename1].sort(key=lambda x: x["유사도"], reverse=True)
        similarities[filename1] = similarities[filename1][:top_n]

        # 중간 결과 저장
        if i % 10 == 0:
            with open('유사도_중간결과.json', 'w', encoding='utf-8') as f:
                json.dump(similarities, f, ensure_ascii=False, indent=2)

    # 최종 결과 저장
    with open('유사도_최종결과.json', 'w', encoding='utf-8') as f:
        json.dump(similarities, f, ensure_ascii=False, indent=2)

    return similarities

# 영화 데이터 로드
with open('영화정보리스트.json', 'r', encoding='utf-8') as f:
    movie_data = json.load(f)

# 모든 장르 추출
all_genres = list(set(movie['장르'] for movie in movie_data))

# 사용 예
poster_folder = 'posters'
top_n = 10

if os.path.exists('유사도_최종결과.json'):
    print("이전 결과를 불러오는 중...")
    with open('유사도_최종결과.json', 'r', encoding='utf-8') as f:
        all_similarities = json.load(f)
else:
    print("유사도 계산 중...")
    all_similarities = compare_all_images(poster_folder, movie_data, top_n)

# 결과 출력
for filename, similar_images in all_similarities.items():
    movie_index = int(filename.split('_')[1].split('.')[0])
    print(f"\n'{movie_data[movie_index]['영화명']}'와 가장 유사한 상위 {top_n}개 영화:")
    for image in similar_images:
        similar_movie_index = int(image['파일명'].split('_')[1].split('.')[0])
        print(f"  '{movie_data[similar_movie_index]['영화명']}': {image['유사도']:.4f}")
