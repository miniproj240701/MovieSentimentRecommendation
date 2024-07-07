import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time

# 실패한 영화 목록 불러오기
with open('failure_movies_final.json', 'r', encoding='utf-8') as json_file:
    failure_movies = json.load(json_file)

# 성공한 영화 목록 불러오기
if os.path.exists('success_movies_final.json'):
    with open('success_movies_final.json', 'r', encoding='utf-8') as json_file:
        success_movies = json.load(json_file)
else:
    success_movies = []

# Chrome 드라이버 설정
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)

def search_movie(title):
    try:
        search_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'query')))
        search_box.clear()
        search_box.send_keys(f"영화 {title}")
        search_box.send_keys(Keys.ENTER)
        title_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="area_text_title"]/strong[@class="_text"]'))
        )
        return title_element.text
    except TimeoutException:
        return None

initial_success_count = len(success_movies)  # 초기 성공 영화 목록의 길이 저장

# 실패한 영화 재시도
for movie in failure_movies:
    title = movie['Title']
    found_title = search_movie(title)
    if found_title:
        success_movies.append(movie)
        print(f"영화 '{title}' 검색 성공")
    else:
        print(f"영화 '{title}' 검색 실패")

# 성공한 영화가 추가되었는지 확인 후 진행 상황 저장
if len(success_movies) > initial_success_count:
    with open('success_movies_final.json', 'w', encoding='utf-8') as json_file:
        json.dump(success_movies, json_file, ensure_ascii=False, indent=4)
    print(f"총 {len(success_movies)}개의 영화가 성공적으로 크롤링되었습니다.")
else:
    print("새로운 성공한 영화가 없어 파일을 업데이트하지 않습니다.")

# WebDriver 종료
driver.quit()

# 최종 결과 출력
print(f"총 {len(failure_movies)}개의 영화가 크롤링에 실패했습니다.")
for movie in failure_movies:
    print(movie['Title'])
