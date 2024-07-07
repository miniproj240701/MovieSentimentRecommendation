from gensim.models import FastText
from konlpy.tag import Okt

# 형태소 분석기
okt = Okt()

# 예시 문장
sentences = ["나는 인공지능을 좋아해", "FastText는 정말 좋은 기법이야", "젠심은 유용한 라이브러리야"]

# 문장 토큰화
tokenized_sentences = [okt.morphs(sentence) for sentence in sentences]

# FastText 모델 학습
model = FastText(tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)

# 단어 벡터 얻기
word_vector = model.wv['인공지능']

# 두 단어 간 유사도 계산
similarity = model.wv.similarity('인공지능', '좋아해')
print(f'Similarity between "인공지능" and "좋아해": {similarity}')
