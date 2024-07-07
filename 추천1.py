import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import torch
from torchvision import models, transforms
from konlpy.tag import Okt
import random
import os
from gensim.models import Word2Vec
from datetime import datetime

# JSON 파일 로드 함수
def load_movie_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 이미지 처리를 위한 모델 및 전처리 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=True).to(device)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 한국어 형태소 분석기
okt = Okt()

def preprocess_text(text):
    return okt.morphs(text)

def get_image_features(image_path):
    image = Image.open(image_path).convert('RGB')
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        features = model(image_tensor)
    return features.cpu().numpy().flatten()

def calculate_similarity(vec1, vec2):
    return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]

def train_word2vec(movie_data):
    sentences = [preprocess_text(movie['줄거리']) for movie in movie_data]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    return model

def get_sentence_vector(word2vec_model, sentence):
    words = preprocess_text(sentence)
    word_vectors = [word2vec_model.wv[word] for word in words if word in word2vec_model.wv]
    if not word_vectors:
        return np.zeros(word2vec_model.vector_size)
    return np.mean(word_vectors, axis=0)

def calculate_year_similarity(year1, year2):
    return 1 - abs(year1 - year2) / 100  # Normalize by assuming max difference of 100 years

def recommend_by_genre(selected_genre, movie_data, top_n=10):
    candidates = [movie for movie in movie_data if selected_genre == movie['장르']]
    if len(candidates) < top_n:
        candidates = movie_data  # 후보가 부족하면 전체 영화로 확장
    
    # 장르 일치도로 정렬
    candidates.sort(key=lambda x: 1 if selected_genre == x['장르'] else 0, reverse=True)
    
    # 상위 영화 중 랜덤 선택
    top_movies = candidates[:min(len(candidates), top_n*2)]
    recommended = random.sample(top_movies, min(len(top_movies), top_n))
    
    return recommended

def recommend_similar_movies(reference_movie, movie_data, word2vec_model, top_n=5):
    current_year = datetime.now().year
    
    ref_plot_vector = get_sentence_vector(word2vec_model, reference_movie['줄거리'])
    ref_image_vector = get_image_features(f"posters/poster_{movie_data.index(reference_movie)}.jpg")
    ref_year = int(reference_movie['개봉년도'])
    ref_rating = float(reference_movie['평점'])
    
    for i, movie in enumerate(movie_data):
        if movie['영화명'] != reference_movie['영화명']:
            # 줄거리 유사도
            plot_vector = get_sentence_vector(word2vec_model, movie['줄거리'])
            plot_similarity = calculate_similarity(ref_plot_vector, plot_vector)
            
            # 이미지 유사도
            image_vector = get_image_features(f"posters/poster_{i}.jpg")
            image_similarity = calculate_similarity(ref_image_vector, image_vector)
            
            # 장르 유사도
            genre_similarity = 1 if movie['장르'] == reference_movie['장르'] else 0
            
            # 개봉 연도 유사도
            year_similarity = calculate_year_similarity(ref_year, int(movie['개봉년도']))
            
            # 평점 차이
            rating_diff = abs(ref_rating - float(movie['평점'])) / 10  # Normalize by max rating of 10
            
            # 최종 유사도 점수 계산
            movie['similarity_score'] = (
                0.3 * plot_similarity +
                0.2 * image_similarity +
                0.2 * genre_similarity +
                0.2 * year_similarity +
                0.1 * (1 - rating_diff)  # 높은 점수 차이는 낮은 유사도를 의미
            )
    
    # 유사도 점수로 정렬
    sorted_movies = sorted(movie_data, key=lambda x: x.get('similarity_score', 0), reverse=True)
    
    return sorted_movies[:top_n]

# 메인 실행 부분
if __name__ == "__main__":
    # JSON 파일 로드
    movie_data = load_movie_data('영화정보데이터셋.json')

    # Word2Vec 모델 학습
    word2vec_model = train_word2vec(movie_data)

    # 1단계: 장르 선택
    selected_genre = '코미디'
    genre_recommendations = recommend_by_genre(selected_genre, movie_data)

    print("장르 기반 추천:")
    for movie in genre_recommendations:
        print(f"제목: {movie['영화명']}, 장르: {movie['장르']}")

    # 2단계: 영화 선택 및 유사 영화 추천
    reference_movie = genre_recommendations[0]  # 사용자가 선택한 영화라고 가정
    similar_movies = recommend_similar_movies(reference_movie, movie_data, word2vec_model)

    print("\n유사 영화 추천:")
    for movie in similar_movies:
        print(f"제목: {movie['영화명']}")
        print(f"장르: {movie['장르']}")
        print(f"개봉년도: {movie['개봉년도']}")
        print(f"평점: {movie['평점']}")
        print(f"줄거리: {movie['줄거리'][:50]}...")
        print(f"유사도 점수: {movie.get('similarity_score', 0):.2f}")
        print()