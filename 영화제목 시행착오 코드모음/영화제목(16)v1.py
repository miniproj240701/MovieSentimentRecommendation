import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--log-level=3")  # 로그 레벨을 높여 경고 메시지 억제

# WebDriver 설정
driver = webdriver.Chrome(options=chrome_options)

# 연도 및 URL 템플릿 정의
year = 2016
url_template = f"https://ko.wikipedia.org/wiki/{year}년_대한민국의_영화_목록"

# 영화 목록을 저장할 딕셔너리
movies_by_month = {}

# 주어진 URL로 접속
driver.get(url_template)

try:
    # 페이지가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-parser-output")))
    print("Page loaded successfully.")

    # 모든 테이블을 가져오기
    tables = driver.find_elements(By.XPATH, "//span[@id='상반기']/parent::h3/following-sibling::table")

    for table in tables:
        rows = table.find_elements(By.XPATH, ".//tbody//tr")
        current_month = None
        current_day = None
        for row in rows:
            headers = row.find_elements(By.TAG_NAME, "th")
            cells = row.find_elements(By.TAG_NAME, "td")

            # 월 정보 가져오기
            if headers and '월' in headers[0].text:
                month_info = headers[0].text.split("\n")
                if month_info:
                    current_month = month_info[0].replace('월', '').strip()
                    if current_month not in movies_by_month:
                        movies_by_month[current_month] = {}

            # 일 정보 가져오기
            if cells and len(cells) > 1:
                current_day = None  # 현재 처리 중인 날짜를 저장할 변수
                movies = []  # 영화 정보를 저장할 리스트
                i = 0  # cells 리스트의 인덱스를 관리할 변수
                
                # 영화 정보 가져오기
                for cell in cells:
                    text = cell.text.strip()
                    i += 1  # 다음 셀로 이동
                    # print(f"{i} | {text}")
                    day_match = re.search(r"(\d+일)", text)
                    if day_match:
                        current_day = day_match.group(1)  # 새로운 날짜가 나타나면 업데이트
                        continue  # 날짜 라인을 처리했으니 다음 라인으로 넘어감
                    
                    title_match = re.search(r"〈(.+?)〉", text)
                    if title_match:
                        title = title_match.group(1)
                        # 감독과 장르는 제목이 나온 바로 다음 줄에 위치한다고 가정
                        if i + 1 < len(cells):
                            director_line = cells[i+1].text.strip()
                        else:
                            director_line = ""
                        
                        if i + 2 < len(cells):
                            genre_line = cells[i+2].text.strip()
                        else:
                            genre_line = ""
                        
                        i += 2  # 다음 다음 셀로 이동 (감독과 장르를 이미 처리했으므로)

                        director_match = re.search(r"감독 (.+)", director_line)
                        genre_match = re.findall(r"[\w/]+", genre_line)  # 장르 정보만 추출
                        
                        director = director_match.group(1) if director_match else '[정보 없음]'
                        genre = ', '.join(genre_match) if genre_match else '[정보 없음]'
                        
                        movies.append({
                            'Day': current_day,
                            'Title': title,
                            'Director': director,
                            'Genre': genre
                        })
                        
                # 추출된 영화 정보 출력
                for movie in movies:
                    print(f"무비: {movie}")
    
except TimeoutException:
    print(f"TimeoutException: {year}년 페이지를 로드하는 데 실패했습니다.")

# WebDriver 종료
driver.quit()
