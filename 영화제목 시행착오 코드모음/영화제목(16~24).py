import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# WebDriver 설정
driver = webdriver.Chrome(options=chrome_options)

# 연도 범위 및 URL 템플릿 정의
years = range(2016, 2025)
url_template = "https://ko.wikipedia.org/wiki/{}년_대한민국의_영화_목록"

# 영화 목록을 저장할 딕셔너리
movies = {}

for year in years:
    url = url_template.format(year)
    driver.get(url)
    
    try:
        # 페이지가 로드될 때까지 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-parser-output ul li")))
        
        # 영화 제목 추출 (페이지 내용의 <li> 태그 내에 있다고 가정)
        movie_elements = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output ul li")
        movie_list = [element.text for element in movie_elements if element.text]
        
        movies[year] = movie_list
    
    except TimeoutException:
        print(f"TimeoutException: {year}년 페이지를 로드하는 데 실패했습니다.")

# WebDriver 종료
driver.quit()

# 결과 출력 (연도별 첫 5개의 영화 제목만 출력)
for year in movies:
    print(f"{year}년:")
    for movie in movies[year][:5]:
        print(f"- {movie}")
    print()
