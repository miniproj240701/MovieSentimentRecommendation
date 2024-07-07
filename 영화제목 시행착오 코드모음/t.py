import re
from konlpy.tag import Okt

okt = Okt()
stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

def get_meaningful_words(text):
    morphs = okt.pos(text, stem=True)  # stem=True를 추가하여 어간 추출
    meaningful_words = []
    for word, pos in morphs:
        if pos in ['Noun', 'Adjective', 'Verb']:
            if word not in stopwords and len(word) > 1:
                meaningful_words.append(word)
    return meaningful_words

# 예시 텍스트
text = "이 영화는 정말 재미있고 감동적이었습니다. 배우들의 연기도 훌륭했어요."

meaningful_words = get_meaningful_words(text)
print(meaningful_words)