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

def extract_image_features(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features.cpu().numpy().flatten()

def extract_text_features(plot, genre, all_genres):
    plot_features = tfidf.transform([plot]).toarray().flatten()
    genre_features = np.zeros(len(all_genres))
    genre_features[all_genres.index(genre)] = 1
    return np.concatenate([plot_features, genre_features])

def compare_images(poster_folder, top_n=10):
    total_images = 572
    all_features = {}

    for i in tqdm(range(total_images), desc="이미지 특징 추출 중"):
        filename = f"poster_{i}.jpg"
        image_path = os.path.join(poster_folder, filename)
        if os.path.exists(image_path):
            features = extract_image_features(image_path)
            all_features[filename] = features
        else:
            print(f"경고: {filename}를 찾을 수 없습니다")

    image_similarities = {}

    for i in tqdm(range(total_images), desc="이미지 비교 중"):
        filename1 = f"poster_{i}.jpg"
        if filename1 not in all_features:
            continue
        
        image_similarities[filename1] = []
        for filename2, features2 in all_features.items():
            if filename1 == filename2:
                continue
            
            similarity = np.dot(all_features[filename1], features2) / (np.linalg.norm(all_features[filename1]) * np.linalg.norm(features2))
            image_similarities[filename1].append({"파일명": filename2, "유사도": float(similarity)})
        
        image_similarities[filename1].sort(key=lambda x: x["유사도"], reverse=True)
        image_similarities[filename1] = image_similarities[filename1][:top_n]

    return image_similarities

def compare_movies(movie_data, top_n=10):
    all_genres = list(set(movie['장르'] for movie in movie_data))
    all_plots = [movie['줄거리'] for movie in movie_data]
    tfidf.fit(all_plots)

    all_features = {}

    for i, movie in tqdm(enumerate(movie_data), desc="영화 특징 추출 중"):
        features = extract_text_features(movie['줄거리'], movie['장르'], all_genres)
        all_features[i] = features

    movie_similarities = {}

    for i in tqdm(range(len(movie_data)), desc="영화 비교 중"):
        movie_similarities[i] = []
        for j, features2 in all_features.items():
            if i == j:
                continue
            
            similarity = np.dot(all_features[i], features2) / (np.linalg.norm(all_features[i]) * np.linalg.norm(features2))
            movie_similarities[i].append({"영화 인덱스": j, "유사도": float(similarity)})
        
        movie_similarities[i].sort(key=lambda x: x["유사도"], reverse=True)
        movie_similarities[i] = movie_similarities[i][:top_n]

    return movie_similarities

# 영화 데이터 로드
with open('긍부정영화정보리스트.json', 'r', encoding='utf-8') as f:
    movie_data = json.load(f)

# 사용 예
poster_folder = 'posters'
top_n = 10

# 이미지 기반 유사 포스터 추천
image_similarities = compare_images(poster_folder, top_n)

# 줄거리 및 장르 기반 유사 영화 추천
movie_similarities = compare_movies(movie_data, top_n)

# 결과 저장
with open('이미지_유사도_결과.json', 'w', encoding='utf-8') as f:
    json.dump(image_similarities, f, ensure_ascii=False, indent=2)

with open('영화_유사도_결과.json', 'w', encoding='utf-8') as f:
    json.dump(movie_similarities, f, ensure_ascii=False, indent=2)

# 결과 출력 (예시)
print("이미지 기반 유사 포스터:")
for filename, similar_images in list(image_similarities.items())[:5]:
    print(f"\n{filename} 와 가장 유사한 상위 {top_n}개 이미지:")
    for image in similar_images[:3]:
        print(f"  {image['파일명']}: 유사도 {image['유사도']:.4f}")

print("\n줄거리 및 장르 기반 유사 영화:")
for idx, similar_movies in list(movie_similarities.items())[:5]:
    print(f"\n영화 {movie_data[idx]['영화명']} 와 가장 유사한 상위 {top_n}개 영화:")
    for movie in similar_movies[:3]:
        similar_movie = movie_data[movie['영화 인덱스']]
        print(f"  {similar_movie['영화명']}: 유사도 {movie['유사도']:.4f}")