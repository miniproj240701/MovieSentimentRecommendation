import torch
import torch.nn as nn
import re
from konlpy.tag import Okt
import numpy as np
import pickle
import json
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 모델 구조 정의
class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SentimentLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        lstm_out = lstm_out[:, -1, :]
        out = self.fc(lstm_out)
        return self.sigmoid(out)

# 단어 사전 로드
with open('word_to_index.pkl', 'rb') as f:
    word_to_index = pickle.load(f)

vocab_size = len(word_to_index) + 1
embedding_dim = 100
hidden_dim = 128
output_dim = 1

# GPU 사용 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 모델 로드
model = SentimentLSTM(vocab_size, embedding_dim, hidden_dim, output_dim)
model.load_state_dict(torch.load('final_best_model.pth', map_location=device))
model = model.to(device)
model.eval()  # 평가 모드로 전환

# 전처리 함수 정의
okt = Okt()
stopwords = [
    '이', '그', '저', '것', '수', '등', '들', '및', '에', '의', '가', '을', '를', '은', '는',
    '이다', '하다', '되다', '있다', '없다', '나', '너', '저', '우리', '당신',
    '매우', '아주', '정말', '진짜', '거의', '또', '더',
    '그리고', '또는', '하지만', '그러나',
    '무엇', '어디', '언제', '누구', '어떻게', '왜',
    '가다', '오다', '주다', '받다',
    '많다', '적다', '크다', '작다',
    '지금', '오늘', '내일', '어제',
    '때문', '위해', '대해', '통해',
    '계속', "그냥", "전혀", "부분", "일단", '요즘', '무슨',
    '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한',
    # 명사 관련 추가 불용어
    '때', '거', '데', '듯', '로', '명', '개', '년', '월', '일', '분', '초',
    '리', '께', '말', '주', '건', '제', '번', '통', '후', '경', '뿐'

    # 영화 리뷰 특화 불용어
    '영화', '작품', '관람', '감상', '개봉', '상영', '내용', '제목'
    '평점', '별점', '점수', '평가', "소설", "배역", "드라마"
    '시간', '분', '초', "알바", '댓글알바', "니코니코니", "원작", "웹툰", "영화로", '대한', '직접'
    '배우', '감독', '제작', '개봉', '극장', '영화인', "네이버", '스크린', '어이', '이건', '이야기', '얼마나', '대부분', '보고'
]

def tokenize(text):
    tokens = okt.morphs(text, stem=True)
    tokens = [word for word in tokens if not word in stopwords]
    return tokens

def tokens_to_sequences(tokens):
    return [word_to_index.get(token, 0) for token in tokens]

def pad_sequences(sequences, maxlen=30):
    padded = np.zeros((len(sequences), maxlen), dtype=int)
    for i, seq in enumerate(sequences):
        if len(seq) > 0:
            if len(seq) > maxlen:
                padded[i] = np.array(seq[:maxlen])
            else:
                padded[i, -len(seq):] = np.array(seq)
    return padded

def preprocess_input(text):
    text = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)
    tokens = tokenize(text)
    sequence = tokens_to_sequences(tokens)
    padded_sequence = pad_sequences([sequence])
    return torch.LongTensor(padded_sequence).to(device)

# 예측 함수 정의
def predict_sentiment(text, model):
    input_tensor = preprocess_input(text)
    with torch.no_grad():
        output = model(input_tensor)
        positive_prob = output.squeeze().item()
        negative_prob = 1 - positive_prob
        return positive_prob, negative_prob

# 영화 정보 파일 읽기
with open('영화정보데이터셋.json', 'r', encoding='utf-8') as f:
    movie_data = json.load(f)

# 예측 결과 및 실제 레이블 저장
y_true = []
y_pred = []

# 각 영화의 리뷰에 대한 감정 예측 및 결과 저장
for movie in movie_data:
    for review in movie['리뷰']:
        if review['리뷰내용'].strip():  # 리뷰 내용이 공백이 아닌 경우에만 처리
            positive_prob, negative_prob = predict_sentiment(review['리뷰내용'], model)
            if positive_prob > negative_prob:
                predicted_sentiment = 1
                review['감정'] = '긍정'
                review['확률'] = round(positive_prob, 4)
            else:
                predicted_sentiment = 0
                review['감정'] = '부정'
                review['확률'] = round(negative_prob, 4)
            y_pred.append(predicted_sentiment)
            y_true.append(1 if int(review['별점']) > 5 else 0)  # 별점 5 이상을 긍정, 5 이하를 부정으로 간주
        else:
            review['감정'] = '없음'
            review['확률'] = 0.0

# 성능 매트릭스 계산
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# 결과를 JSON 파일로 저장
output_path = '긍부정영화정보리스트.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(movie_data, f, ensure_ascii=False, indent=4)

print(f"감정 분석 결과가 {output_path} 파일에 저장되었습니다.")

# JSON 파일 불러오기
with open('긍부정영화정보리스트.json', 'r', encoding='utf-8') as file:
    movie_data = json.load(file)

# 각 영화별로 긍정과 부정 리뷰의 비율 계산
for movie in movie_data:
    positive_count = 0
    negative_count = 0
    total_reviews = 0  # 유효한 리뷰 개수 카운트
    total_positive_weight = 0
    total_negative_weight = 0

    for review in movie['리뷰']:
        if review['리뷰내용'].strip() and '감정' in review:  # 리뷰 내용이 존재하고 감정 분석 결과가 있는 경우만 처리
            total_reviews += 1
            positive_weight = int(review['공감수'].replace(',', '')) if '공감수' in review else 1
            negative_weight = int(review['비공감수'].replace(',', '')) if '비공감수' in review else 1
            if review['감정'] == '긍정':
                positive_count += 1
                total_positive_weight += positive_weight
            elif review['감정'] == '부정':
                negative_count += 1
                total_negative_weight += negative_weight

    # 리뷰가 없는 경우를 처리
    if total_reviews == 0:
        movie['긍정비율'] = 0
        movie['부정비율'] = 0
    else:
        total_weight = total_positive_weight + total_negative_weight
        movie['긍정비율'] = round((total_positive_weight / total_weight) * 100) if total_weight > 0 else 0  # 비율을 퍼센트로 계산
        movie['부정비율'] = round((total_negative_weight / total_weight) * 100) if total_weight > 0 else 0  # 비율을 퍼센트로 계산

# 형태소 분석기 초기화
okt = Okt()

def get_meaningful_nouns(text):
    # 형태소 분석
    morphs = okt.pos(text, stem=True)  # stem=True를 사용하여 어간 추출
    
    # 명사만 선택
    meaningful_nouns = [word for word, pos in morphs if pos == 'Noun']
    
    # 불용어 제거 및 길이가 2 이상인 단어만 선택
    meaningful_nouns = [word for word in meaningful_nouns if word not in stopwords and len(word) > 1]
    
    return meaningful_nouns

# 각 영화별로 긍정/부정 리뷰의 명사 추출 및 저장
for movie in movie_data:
    positive_words = []
    negative_words = []

    for review in movie['리뷰']:
        if review['리뷰내용'].strip() and '감정' in review:
            nouns = get_meaningful_nouns(review['리뷰내용'])
            if review['감정'] == '긍정':
                positive_words.extend(nouns)
            elif review['감정'] == '부정':
                negative_words.extend(nouns)

    # 상위 100개 단어 선택
    top_positive_words = list(set(positive_words))[:100]
    top_negative_words = list(set(negative_words))[:100]

    # 워드 클라우드 데이터 추가
    movie['긍정워드클라우드'] = top_positive_words
    movie['부정워드클라우드'] = top_negative_words

# 수정된 데이터를 같은 파일에 다시 저장
with open('긍부정영화정보리스트.json', 'w', encoding='utf-8') as file:
    json.dump(movie_data, file, ensure_ascii=False, indent=4)

print("영화별 긍정 및 부정 리뷰 분포와 워드 클라우드 데이터가 파일에 저장되었습니다.")
