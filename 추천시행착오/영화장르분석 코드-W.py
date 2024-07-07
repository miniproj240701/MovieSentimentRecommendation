from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 한국어 영화 장르 키워드 데이터
genre_list = ['SF', '가족', '공포', '느와르', '다큐멘터리', '드라마', '로맨스', 
              '모험', '뮤지컬', '미스터리', '범죄', '블랙코미디', '서사', '서스펜스', 
              '스릴러', '애니메이션', '액션', '전쟁', '코미디', '판타지']

# Word2Vec 모델 학습
genre_corpus = [[genre] for genre in genre_list]
model = Word2Vec(genre_corpus, min_count=1, vector_size=100, window=5, workers=4)

# 장르 키워드 임베딩 및 유사도 계산
genre_embeddings = [model.wv[genre] for genre in genre_list]
similarity_matrix = cosine_similarity(genre_embeddings, genre_embeddings)

# 결과 출력
for i, genre in enumerate(genre_list):
    print(f"{genre}: {', '.join(f'{genre_list[j]}: {similarity_matrix[i][j]:.3f}' for j in range(len(genre_list)) if j != i)}")