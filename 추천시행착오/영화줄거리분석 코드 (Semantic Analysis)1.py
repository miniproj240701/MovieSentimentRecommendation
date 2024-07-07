from konlpy.tag import Okt
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# KoBERT 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("skt/kobert-base-v1")
model = AutoModel.from_pretrained("skt/kobert-base-v1")

# 한국어 형태소 분석기
okt = Okt()

def preprocess_korean(text):
    # 형태소 분석 수행
    morphs = okt.morphs(text)
    return ' '.join(morphs)

def get_kobert_embedding(text):
    # 전처리
    preprocessed_text = preprocess_korean(text)
    print(f"Preprocessed text: {preprocessed_text}")
    
    # 토큰화 및 BERT 입력 형식으로 변환
    inputs = tokenizer(preprocessed_text, return_tensors="pt", padding="max_length", truncation=True, max_length=512)
    
    # 토큰화된 입력 확인 및 인덱스 범위 검증
    input_ids = inputs["input_ids"]
    print(f"Token IDs: {input_ids}")
    if torch.any(input_ids >= model.config.vocab_size):
        raise ValueError("입력 텍스트에 모델의 단어 사전 범위를 벗어나는 토큰이 포함되어 있습니다.")
    
    # KoBERT 모델을 통해 임베딩 생성
    with torch.no_grad():
        outputs = model(input_ids=input_ids)
    
    # [CLS] 토큰의 최종 은닉 상태를 문장 임베딩으로 사용
    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    print(f"CLS embedding: {cls_embedding}")
    return cls_embedding

# 영화 줄거리에 적용
movie1_plot = "영웅이 외계인의 침공으로부터 세계를 구한다."
movie2_plot = "외계인이 지구를 공격하고 인류가 반격한다."

embedding1 = get_kobert_embedding(movie1_plot)
embedding2 = get_kobert_embedding(movie2_plot)

# 코사인 유사도 계산
similarity = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

print(f"두 영화의 줄거리 유사도: {similarity[0][0]}")
