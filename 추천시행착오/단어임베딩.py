from transformers import BertTokenizer, BertModel
import numpy as np

# 사전 학습된 KorBERT 모델 로드
tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
model = BertModel.from_pretrained('monologg/kobert')

# 영화 장르 문장 임베딩
genre_list = ['SF', '가족', '공포', '느와르', '다큐멘터리', '드라마', '멜로/로맨스', 
              '모험', '뮤지컬', '미스터리', '범죄', '블랙코미디', '서사', '서스펜스', 
              '스릴러', '애니메이션', '액션', '전쟁', '코미디', '판타지']

genre_embeddings = []
for genre in genre_list:
    genre_text = f"이 영화는 {genre} 장르입니다."
    inputs = tokenizer(genre_text, return_tensors="pt")
    outputs = model(**inputs)
    genre_embedding = outputs.pooler_output.detach().numpy()
    genre_embeddings.append(genre_embedding)

genre_embeddings = np.array(genre_embeddings)

# 코사인 유사도 계산
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(genre_embeddings, genre_embeddings)

# 결과 출력
for i, genre in enumerate(genre_list):
    print(f"{genre}: {', '.join(f'{genre_list[j]}: {similarity_matrix[i][j]:.3f}' for j in range(len(genre_list)) if j != i)}")