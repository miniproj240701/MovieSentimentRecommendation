from gensim.models import Word2Vec
from konlpy.tag import Okt
import re

# 형태소 분석기
okt = Okt()

# 사용자 정의 토크나이저
def custom_tokenize(sentence, custom_vocab):
    tokens = []
    start = 0
    while start < len(sentence):
        matched = False
        for word in custom_vocab:
            if sentence[start:start+len(word)] == word:
                tokens.append(word)
                start += len(word)
                matched = True
                break
        if not matched:
            tokens.append(sentence[start])
            start += 1
    return tokens

# 사용자 정의 단어 목록
custom_vocab = ['인공지능', '워드투벡', '젠심', '좋아해', '감정', '기술', '라이브러리', '기법', 'NLP', '애플리케이션', '모델']

# 예시 문장
sentences = [
    "나는 인공지능을 좋아해",
    "워드투벡은 정말 좋은 기법이야",
    "젠심은 유용한 라이브러리야",
    "인공지능은 많은 가능성을 가지고 있어",
    "워드투벡을 사용하면 단어의 의미를 파악할 수 있어",
    "젠심 라이브러리를 사용하여 모델을 쉽게 구축할 수 있어",
    "인공지능 기술은 빠르게 발전하고 있어",
    "좋아해라는 감정은 사람마다 다르게 표현돼",
    "기계학습은 인공지능의 한 분야야",
    "인공지능은 다양한 산업에서 사용되고 있어",
    "좋아해라는 말은 감정을 표현하는 중요한 방법이야",
    "워드투벡 모델은 단어 간의 유사도를 계산할 수 있어",
    "젠심은 NLP 작업에 많이 사용돼",
    "인공지능을 활용한 애플리케이션이 많아지고 있어",
    "좋아해라는 단어는 긍정적인 의미를 담고 있어",
    "인공지능의 발전은 우리의 생활을 크게 변화시킬 것이다",
    "워드투벡은 자연어 처리에 매우 유용하다",
    "젠심은 다양한 기능을 제공하는 라이브러리다",
    "인공지능을 사용하여 더 나은 세상을 만들 수 있다",
    "좋아해라는 감정은 인간의 본능적인 감정이다",
    # 추가 문장
    "인공지능은 인류의 미래를 밝힐 것이다",
    "워드투벡은 자연어 처리를 위한 강력한 도구이다",
    "젠심 라이브러리는 다양한 언어 처리 기능을 제공한다",
    "인공지능은 의료, 금융, 교육 등 다양한 분야에서 혁신을 일으키고 있다",
    "좋아해라는 감정은 사랑의 표현 중 하나이다",
    "기술의 발전은 우리의 삶을 편리하게 만든다",
    "인공지능과 머신러닝은 긴밀하게 연결되어 있다",
    "워드투벡은 텍스트 데이터를 벡터로 변환하는데 유용하다",
    "젠심은 사용하기 쉬운 인터페이스를 제공한다",
    "좋아해라는 말은 일상에서 자주 사용된다"
]

# 공백 및 특수문자 제거
sentences = [re.sub(r'\s+', ' ', sentence) for sentence in sentences]
sentences = [re.sub(r'[^가-힣a-zA-Z0-9\s]', '', sentence) for sentence in sentences]

# 문장 토크나이즈
tokenized_sentences = [custom_tokenize(sentence, custom_vocab) for sentence in sentences]
print(f'Tokenized sentences: {tokenized_sentences}')

# Word2Vec 모델 학습
model = Word2Vec(tokenized_sentences, vector_size=100, window=3, min_count=1, workers=4)

# 학습된 단어들 확인
print(f'Vocabulary: {model.wv.index_to_key}')

# 단어 벡터 얻기
try:
    word_vector = model.wv['인공지능']
    print(f'Vector for "인공지능": {word_vector}')
except KeyError as e:
    print(f"KeyError: {e}")

# 두 단어 간 유사도 계산
try:
    similarity = model.wv.similarity('인공지능', '좋아해')
    print(f'Similarity between "인공지능" and "좋아해": {similarity}')
except KeyError as e:
    print(f"KeyError: {e}")

# 모델 평가를 위한 단어 유사도 확인
similar_words = model.wv.most_similar('인공지능', topn=5)
print(f'Most similar words to "인공지능": {similar_words}')
