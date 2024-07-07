import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  # headless 모드 설정
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

def get_element_text_by_xpath(driver, xpath, delay=10):
    try:
        element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_age_rating(movie_name):
    url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화 {movie_name}"
    driver.get(url)

    # 기본정보 탭 클릭
    기본정보_xpath = '//*[@class="type_scroll _scroller _scroll _main_tab"]/div/ul[@class="tab_list"]/li[@class="tab _tab _item"][2]/a/span[@class="menu"]'
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 기본정보_xpath))
        ).click()

        # 등급 정보 가져오기
        rating_xpath = '//*[@class="cm_content_area _cm_content_area_info"]/div[@class="cm_info_box"]/div[@class="detail_info"]/dl[@class="info txt_4"]/div[2]/dd'
        등급 = get_element_text_by_xpath(driver, rating_xpath)
        return 등급
    except Exception as e:
        print(f"An error occurred while fetching age rating for {movie_name}: {e}")
        return None

def save_progress(movie_list, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(movie_list, f, ensure_ascii=False, indent=4)

progress_file = '영화정보리스트_업데이트.json'

# 이전 진행 상황을 불러오기
if os.path.exists(progress_file):
    with open(progress_file, 'r', encoding='utf-8') as f:
        movie_list = json.load(f)
else:
    # JSON 파일 읽기
    with open('영화정보리스트.json', 'r', encoding='utf-8') as f:
        movie_list = json.load(f)

# 이미 처리된 영화 제외
processed_titles = {movie['영화명'] for movie in movie_list if '등급' in movie}
movies_to_process = [movie for movie in movie_list if movie['영화명'] not in processed_titles]

# 영화 목록 순회하며 연령 제한 정보 추가
for movie in movies_to_process:
    retries = 3
    while retries > 0:
        try:
            print(f"Fetching age rating for movie: {movie['영화명']}")
            movie['등급'] = fetch_age_rating(movie['영화명'])
            if movie['등급'] is not None:
                break
        except Exception as e:
            print(f"An error occurred while processing {movie['영화명']}: {e}")
            time.sleep(5)  # 잠시 대기 후 재시도
        retries -= 1

    # 중간 저장
    save_progress(movie_list, progress_file)

# 최종 저장
final_file = '영화정보데이터셋.json'
save_progress(movie_list, final_file)

driver.quit()
