import json
from gensim import corpora
from gensim.models import LdaModel
from konlpy.tag import Okt
import re

# JSON 파일 로드
with open('영화정보데이터셋.json', 'r', encoding='utf-8') as f:
    movie_data = json.load(f)

# Okt 형태소 분석기 초기화
okt = Okt()

# 불용어 리스트 (예시, 필요에 따라 확장)
stop_words = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

def preprocess_text(text):
    # 특수 문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    # 형태소 분석 및 불용어 제거
    tokens = [word for word in okt.nouns(text) if word not in stop_words and len(word) > 1]
    return tokens

# 줄거리 전처리
tokenized_plots = [preprocess_text(movie['줄거리']) for movie in movie_data]

# 사전 생성
dictionary = corpora.Dictionary(tokenized_plots)

# Corpus 생성
corpus = [dictionary.doc2bow(text) for text in tokenized_plots]

# LDA 모델 학습
num_topics = 5  # 주제 개수, 필요에 따라 조정
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=100,
                     update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

# 학습된 주제 출력
print("학습된 주제:")
for idx, topic in lda_model.print_topics(-1):
    print(f"주제 {idx}: {topic}")

# 각 영화의 주제 분포 확인 (예시로 첫 5개 영화만)
print("\n각 영화의 주제 분포 (상위 5개 영화):")
for i, movie in enumerate(movie_data[:5]):
    print(f"\n영화: {movie['영화명']}")
    bow = dictionary.doc2bow(tokenized_plots[i])
    movie_topics = lda_model.get_document_topics(bow)
    for topic_id, prob in movie_topics:
        print(f"주제 {topic_id}: {prob:.4f}")