import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 한국어 불용어 리스트 정의
korean_stopwords = [
    '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', 
    '자', '에', '와', '한', '하다', '것', '그', '되', '수', '이', '있', '하', '않', 
    '없', '나', '사람', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', 
    '말', '일', '때문', '그', '다음', '그것', '두', '더', '좀', '잘', '별', '있', '것', 
    '그', '중', '에서', '자기', '알', '등', '싶', '듯', '잘', '걍', '와', '한', '하'
]

# 영화 데이터 로드
movies = pd.read_json('영화정보데이터셋.json')

# 줄거리와 장르를 결합한 콘텐츠 필드 생성
movies['콘텐츠'] = movies['줄거리'] + ' ' + movies['장르']

# NaN 값을 빈 문자열로 대체
movies['콘텐츠'] = movies['콘텐츠'].fillna('')

# TF-IDF 벡터화
tfidf = TfidfVectorizer(stop_words=korean_stopwords)
tfidf_matrix = tfidf.fit_transform(movies['콘텐츠'])

# 유사도 계산
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# 영화 제목과 인덱스를 매핑
indices = pd.Series(movies.index, index=movies['영화명']).drop_duplicates()

# 영화 추천 함수
def get_recommendations(title, cosine_sim=cosine_sim):
    # 선택한 영화의 인덱스를 얻음
    idx = indices[title]
    
    # 모든 영화와의 유사도 점수 얻음
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # 유사도 점수에 따라 영화들을 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # 가장 유사한 10개의 영화 선택
    sim_scores = sim_scores[1:11]
    
    # 가장 유사한 영화들의 인덱스 얻음
    movie_indices = [i[0] for i in sim_scores]
    
    # 유사한 영화들의 제목 반환
    return movies['영화명'].iloc[movie_indices]

# 예시: 특정 영화와 유사한 영화 추천
print(get_recommendations('남과 여'))
