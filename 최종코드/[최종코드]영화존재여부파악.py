import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

delay = 5  # 타임아웃 시간을 5초로 설정
max_retries = 3  # 재시도 횟수

def find_element_by_name(q, retries=0):
    try:
        return WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.NAME, q))
        )
    except TimeoutException as e:
        if retries < max_retries:
            time.sleep(2)  # 잠시 대기 후 재시도
            return find_element_by_name(q, retries + 1)
        else:
            raise e

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--log-level=3")  # 로그 레벨을 높여 경고 메시지 억제

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

# 네이버 페이지 열기
driver.get(url='https://www.naver.com')

# JSON 파일 불러오기
with open('2016-2024_Korean_Movie_List_912_Movies.json', 'r', encoding='utf-8') as file:
    movie_data = json.load(file)

# 이전에 저장된 성공한 영화 목록 불러오기
if os.path.exists('success_movies.json'):
    with open('success_movies.json', 'r', encoding='utf-8') as json_file:
        success_movies = json.load(json_file)
else:
    success_movies = []

# 이전에 저장된 실패한 영화 목록 불러오기
if os.path.exists('failure_movies.json'):
    with open('failure_movies.json', 'r', encoding='utf-8') as json_file:
        failure_movies = json.load(json_file)
else:
    failure_movies = []

def save_progress(success, failure):
    with open('success_movies.json', 'w', encoding='utf-8') as json_file:
        json.dump(success, json_file, ensure_ascii=False, indent=4)
    with open('failure_movies.json', 'w', encoding='utf-8') as json_file:
        json.dump(failure, json_file, ensure_ascii=False, indent=4)

def search_movie(title):
    search_box = find_element_by_name('query')
    search_box.clear()
    search_box.send_keys(title)
    search_box.send_keys(Keys.ENTER)
    try:
        # 영화 제목 찾기 (XPath 사용)
        title_element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="area_text_title"]/strong[@class="_text"]'))
        )
        return title_element.text
    except TimeoutException:
        return None

# 각 영화 제목 검색 및 확인
for year, months in movie_data.items():
    for month, movies in months.items():
        for movie in movies:
            if movie in success_movies or movie in failure_movies:
                continue  # 이미 크롤링 시도한 영화는 건너뜀
            title = movie['Title']
            search_query = f"영화 {title}"
            
            found_title = search_movie(search_query)
            if not found_title:
                found_title = search_movie(title)
            
            if not found_title:  # 타임아웃이 발생한 경우 한 번 더 시도
                found_title = search_movie(search_query)
                if not found_title:
                    found_title = search_movie(title)
            
            if found_title:
                # 영화 제목 있는지 여부 확인
                movie_exists = False
                for y, m in movie_data.items():
                    for mo, movs in m.items():
                        for mov in movs:
                            if mov['Title'] == found_title:
                                movie_exists = True
                                break
                        if movie_exists:
                            break
                    if movie_exists:
                        break

                if movie_exists:
                    print(f"영화 '{found_title}'가 목록에 있습니다.")
                    success_movies.append(movie)  # 성공한 영화 추가
                else:
                    print(f"영화 '{found_title}'가 목록에 없습니다.")
                    failure_movies.append(movie)  # 실패한 영화 추가
            else:
                print(f"TimeoutException: 영화 '{title}'를 검색하는 데 실패했습니다.")
                failure_movies.append(movie)
            
            save_progress(success_movies, failure_movies)  # 중간 저장

# WebDriver 종료
driver.quit()

# 최종 성공한 영화 목록 JSON 파일로 저장
with open('success_movies_final.json', 'w', encoding='utf-8') as json_file:
    json.dump(success_movies, json_file, ensure_ascii=False, indent=4)

# 최종 실패한 영화 목록 JSON 파일로 저장
with open('failure_movies_final.json', 'w', encoding='utf-8') as json_file:
    json.dump(failure_movies, json_file, ensure_ascii=False, indent=4)

# 성공한 영화 목록 출력
print(f"총 {len(success_movies)}개의 영화가 성공적으로 크롤링되었습니다.")
for movie in success_movies:
    print(movie)

# 실패한 영화 목록 출력
print(f"총 {len(failure_movies)}개의 영화가 크롤링에 실패했습니다.")
for movie in failure_movies:
    print(movie)
