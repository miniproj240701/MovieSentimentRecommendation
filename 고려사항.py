def calculate_similarity(movie1, movie2):
    # CLIP 이미지 유사도
    image_similarity = calculate_clip_similarity(movie1['포스터'], movie2['포스터'])
    
    # 장르 유사도
    genre_similarity = 1 if movie1['장르'] == movie2['장르'] else 0
    
    # 개봉년도 유사도
    year_similarity = 1 - abs(int(movie1['개봉년도']) - int(movie2['개봉년도'])) / 100
    
    # 평점 유사도
    rating_similarity = 1 - abs(float(movie1['평점']) - float(movie2['평점'])) / 10
    
    # 텍스트 유사도 (줄거리)
    text_similarity = calculate_text_similarity(movie1['줄거리'], movie2['줄거리'])
    
    # 감정 분석 유사도
    emotion_similarity = 1 - abs(movie1['긍정비율'] - movie2['긍정비율']) / 100
    
    # 가중치 적용
    total_similarity = (
        0.4 * image_similarity +
        0.1 * genre_similarity +
        0.1 * year_similarity +
        0.1 * rating_similarity +
        0.2 * text_similarity +
        0.1 * emotion_similarity
    )
    
    return total_similarity