from konlpy.tag import Okt
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

# KoBERT 모델과 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
model = BertModel.from_pretrained('monologg/kobert')

# 한국어 형태소 분석기
okt = Okt()

def preprocess_korean(text):
    # 형태소 분석 수행
    morphs = okt.morphs(text)
    return ' '.join(morphs)

def get_kobert_embedding(text):
    # 전처리
    preprocessed_text = preprocess_korean(text)
    
    # 토큰화 및 BERT 입력 형식으로 변환
    inputs = tokenizer(preprocessed_text, return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    
    # KoBERT 모델을 통해 임베딩 생성
    with torch.no_grad():
        outputs = model(**inputs)
    
    # [CLS] 토큰의 최종 은닉 상태를 문장 임베딩으로 사용
    return outputs.last_hidden_state[:, 0, :].numpy()

# 영화 줄거리에 적용
movie1_plot = "영웅이 외계인의 침공으로부터 세계를 구한다."
movie2_plot = "외계인이 지구를 공격하고 인류가 반격한다."

embedding1 = get_kobert_embedding(movie1_plot)
embedding2 = get_kobert_embedding(movie2_plot)

# 코사인 유사도 계산
similarity = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

print(f"두 영화의 줄거리 유사도: {similarity[0][0]}")

"""
pip install open_clip_torch
pip install -U scikit-learn
pip install sentencepiece
pip install kobert-transformers

"""