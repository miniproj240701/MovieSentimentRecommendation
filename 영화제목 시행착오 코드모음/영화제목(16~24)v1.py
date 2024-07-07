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

# 연도별로 영화 목록을 저장할 딕셔너리
all_years_movies = {}

for year in range(2016, 2025):  # 2016년부터 2024년까지 반복
    url_template = f"https://ko.wikipedia.org/wiki/{year}년_대한민국의_영화_목록"
    driver.get(url_template)
    movies_by_month = {}

    def 테이블(tables):
        for table in tables:
            rows = table.find_elements(By.XPATH, ".//tbody//tr")
            current_month = None
            current_day = None
            for row in rows:
                headers = row.find_elements(By.TAG_NAME, "th")
                cells = row.find_elements(By.TAG_NAME, "td")

                if headers and '월' in headers[0].text:
                    month_info = headers[0].text.split("\n")
                    if month_info:
                        current_month = month_info[0].replace('월', '').strip()
                        if current_month not in movies_by_month:
                            movies_by_month[current_month] = []

                if cells and len(cells) > 1:
                    if year < 2022:
                        i = 0
                        for cell in cells:
                            text = cell.text.strip()
                            i += 1
                            # print(f"{i} | {text}")
                            
                            day_match = re.search(r"(\d+일)", text)
                            if day_match:
                                current_day = day_match.group(1)
                                continue
                            
                            title_match = re.search(r"〈(.+?)〉", text)
                            if title_match:
                                title = title_match.group(1)
                                if i + 1 < len(cells):
                                    director_line = cells[i+1].text.strip()
                                else:
                                    director_line = ""
                                
                                if i + 2 < len(cells):
                                    genre_line = cells[i+2].text.strip()
                                else:
                                    genre_line = ""
                                
                                i += 2
                                director_match = re.search(r"감독 (.+)", director_line)
                                genre_match = re.findall(r"[\w/]+", genre_line)
                                
                                director = director_match.group(1) if director_match else '[정보 없음]'
                                genre = ', '.join(genre_match) if genre_match else '[정보 없음]'
                                
                                movie = {'Day': current_day, 'Title': title, 'Director': director, 'Genre': genre}
                                if not any(m['Day'] == movie['Day'] and m['Title'] == movie['Title'] for m in movies_by_month[current_month]):
                                    movies_by_month[current_month].append(movie)
                    else:
                        i = 0
                        title = ""
                        director = ""
                        genre = ""
                        for cell in cells:
                            text = cell.text.strip()
                            i += 1
                            # print(f"{i} | {text}")
                            
                            if i == 1:
                                current_day = text  
                            elif i == 2:
                                title = text
                            elif i == 4:
                                director = text
                            elif i == 6:
                                genre = text

                            if title and director and genre:
                                movie = {'Day': current_day, 'Title': title, 'Director': director, 'Genre': genre}
                                if not any(m['Day'] == movie['Day'] and m['Title'] == movie['Title'] for m in movies_by_month.get(current_month, [])): 
                                    movies_by_month[current_month].append(movie)   
        return movies_by_month

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-parser-output")))
        first_half_tables = driver.find_elements(By.XPATH, "//span[@id='상반기']/parent::h3/following-sibling::table")
        second_half_tables = driver.find_elements(By.XPATH, "//span[@id='하반기']/parent::h3/following-sibling::table")
        
        테이블(first_half_tables)
        테이블(second_half_tables)
        all_years_movies[year] = movies_by_month
    
    except TimeoutException:
        print(f"TimeoutException: {year}년 페이지를 로드하는 데 실패했습니다.")

# WebDriver 종료
driver.quit()

# 추출된 영화 정보 출력
for year, data in all_years_movies.items():
    print(f"{year}년:")
    for month, movies in data.items():
        print(f"  {month}월:")
        for movie in movies:
            print(f"    무비: {movie}")
