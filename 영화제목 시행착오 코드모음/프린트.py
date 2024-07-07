import re

# 샘플 데이터
data = """
7일
〈잡아야 산다〉
감독 오인천
코미디, 액션

14일
〈프랑스 영화처럼〉
감독 신연식
드라마
"""

# 정규 표현식으로 각 영화 블록 추출
movie_blocks = re.split(r"\n(?=\d+일)", data.strip())

# 각 블록에 대해 정보 추출
for block in movie_blocks:
    day_match = re.search(r"(\d+일)", block)
    title_match = re.search(r"〈(.+?)〉", block)
    director_match = re.search(r"감독 (.+?)(?:\n|$)", block)
    genre_match = re.search(r"감독 [^\n]+\n([^\n]+)", block)

    if day_match and title_match and director_match and genre_match:
        print(f"Day: {day_match.group(1)}, Title: {title_match.group(1)}, Director: {director_match.group(1)}, Genre: {genre_match.group(1)}")
    else:
        print("Missing information in block:", block)
