import requests, re, os, json, time
from io import BytesIO
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  # headless 모드 설정
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

delay = 10

def safe_click(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(1)
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print(f"Click failed: {e}")

def get_element_by_xpath(driver, xpath, delay=10):
    try:
        element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_element_text_by_xpath(driver, xpath, delay=5):
    try:
        element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_number(audience_str):
    multipliers = {
        '천': 1000,
        '만': 10000,
    }
    audience_str = audience_str.replace(',', '').replace(' ', '')
    match = re.match(r'([\d\.]+)([천만]?)명?', audience_str)
    if match:
        number, unit = match.groups()
        number = float(number.replace(',', ''))
        if unit in multipliers:
            number *= multipliers[unit]
        return int(number)
    return 0

def 메뉴_xpath(index):
    if index:
        return f'//*[@class="type_scroll _scroller _scroll _main_tab"]/div/ul[@class="tab_list"]/li[@class="tab _tab _item"][{index}]/a/span[@class="menu"]'
    return None

def fetch_movie_info(movie_name):
    url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화 {movie_name}"
    driver.get(url)

    movie_info = {}

    title_xpath = '//*[@class="title_area type_keep _title_area"]/h2[@class="title _title_ellipsis"]/span[@class="area_text_title"]/strong[@class="_text"]'
    _title = '//*[@class="area_text_title"]/strong[@class="_text"]'
    영화명 = get_element_text_by_xpath(driver, _title)
    movie_info["영화명"] = 영화명

    year_xpath = '//*[@class="sub_title"]/span[@class="txt"][3]'
    year = get_element_text_by_xpath(driver, year_xpath)
    movie_info["개봉년도"] = year

    개요_xp = '//*[@class="cm_content_area _cm_content_area_info"]/div[@class="cm_info_box"]/div[@class="detail_info"]/dl[@class="info txt_3"]'
    개요_xpath = f'{개요_xp}/div[1]/dd'
    개요_element = get_element_by_xpath(driver, 개요_xpath)

    평점_xpath = f'{개요_xp}/div[3]/dt'
    평점 = get_element_text_by_xpath(driver, 평점_xpath)
    별점_xpath = f'{개요_xp}/div[3]/dd'
    별점 = get_element_text_by_xpath(driver, 별점_xpath)
    movie_info["평점"] = 별점

    관객_xpath = f'{개요_xp}/div[4]/dt'
    관객 = get_element_text_by_xpath(driver, 관객_xpath)
    관객수_xpath = f'{개요_xp}/div[4]/dd'
    관객수 = get_element_text_by_xpath(driver, 관객수_xpath)
    movie_info["관객수"] = convert_to_number(관객수)

    if 개요_element:
        개요_html = 개요_element.get_attribute('outerHTML')
        soup = BeautifulSoup(개요_html, 'html.parser')
        개요_texts = [text.strip() for text in soup.stripped_strings]

        if len(개요_texts) >= 3:
            장르 = 개요_texts[0]
            상영시간 = 개요_texts[-1]
        else:
            장르 = "장르 정보를 찾을 수 없습니다."
            상영시간 = "상영시간 정보를 찾을 수 없습니다."

        movie_info["장르"] = 장르
        movie_info["상영시간"] = 상영시간
    else:
        print("개요 정보를 찾을 수 없습니다.")

    역할_xpath = '//*[@class="cm_info_box scroll_img_vertical_95_127"]/div[@class="middle_title"]/h3'
    역할 = get_element_text_by_xpath(driver, 역할_xpath)

    directors_actors_html = driver.find_element(By.CSS_SELECTOR, ".cm_info_box.scroll_img_vertical_95_127").get_attribute('outerHTML')
    soup = BeautifulSoup(directors_actors_html, 'html.parser')
    cast_list = soup.find_all('li', class_='_item')
    casts = []
    for cast in cast_list:
        name = cast.find('strong', class_='name').text.strip()
        role = cast.find('span', class_='sub_text').text.strip()
        img_url = cast.find('img').get('src')
        casts.append({"이름": name, "역할": role, "이미지": img_url})
    movie_info["출연진"] = casts

    전체_xpath = 메뉴_xpath(1)
    기본정보_xpath = 메뉴_xpath(2)
    감독출연_xpath = 메뉴_xpath(3)
    관람평_xpath = 메뉴_xpath(4)
    무비클립_xpath = 메뉴_xpath(5)
    포토_xpath = 메뉴_xpath(6)
    리뷰_xpath = 메뉴_xpath(7)
    명대사_xpath = 메뉴_xpath(8)

    tab_xpaths = {
        "전체": 전체_xpath,
        "기본정보": 기본정보_xpath,
        "감독출연": 감독출연_xpath,
        "관람평": 관람평_xpath,
        "무비클립": 무비클립_xpath,
        "포토": 포토_xpath,
        "리뷰": 리뷰_xpath,
        "명대사": 명대사_xpath
    }

    def click_tab_by_text(driver, tab_text):
        xpath = tab_xpaths.get(tab_text)
        if xpath:
            safe_click(driver, xpath)
        else:
            print(f"'{tab_text}'에 해당하는 탭이 없습니다.")

    전체 = get_element_text_by_xpath(driver, 전체_xpath)
    기본정보 = get_element_text_by_xpath(driver, 기본정보_xpath)
    감독출연 = get_element_text_by_xpath(driver, 감독출연_xpath)
    관람평 = get_element_text_by_xpath(driver, 관람평_xpath)
    무비클립 = get_element_text_by_xpath(driver, 무비클립_xpath)
    포토 = get_element_text_by_xpath(driver, 포토_xpath)
    리뷰 = get_element_text_by_xpath(driver, 리뷰_xpath)
    명대사 = get_element_text_by_xpath(driver, 명대사_xpath)

    click_tab_by_text(driver, "기본정보")

    소개_xp = '//*[@class="cm_content_area _cm_content_area_synopsis"]/div[@class="cm_pure_box"]'
    소개_xpath = f'{소개_xp}/div[@class="middle_title"]/h3[@class="title"]'
    소개 = get_element_text_by_xpath(driver, 소개_xpath)

    줄거리_xpath = f'{소개_xp}/div[@class="intro_box _content "]/p[@class="text _content_text"]'
    줄거리 = get_element_text_by_xpath(driver, 줄거리_xpath)
    movie_info["줄거리"] = 줄거리

    click_tab_by_text(driver, "포토")

    포스터_xpath = '//*[@class="area_card _image_base_poster"]/div[@class="area_card "]/h3[@class="title_numbering"]/strong[@class="this_text_title"]'
    포스터 = get_element_text_by_xpath(driver, 포스터_xpath)

    포스터이미지_xpath = '//*[@class="area_card _image_base_poster"]/div[@class="area_card "]/div[@class="movie_photo_list _list"]/div[@class="_justifiedLayoutWrapper"]/ul[@class="grid_box _adjust"]/li[1]/a/img'
    img_element = get_element_by_xpath(driver, 포스터이미지_xpath)

    style_attribute = img_element.get_attribute('style')
    if img_element:
        img_url = img_element.get_attribute('src')
        movie_info["포스터"] = img_url

    click_tab_by_text(driver, "관람평")

    실관람객탭_xpath = '//*[@class="cm_tap_area _tab_wrap"]/div[@class="type_scroll"]/div/ul/li[1]'
    실관람객탭 = get_element_by_xpath(driver, 실관람객탭_xpath)
    if 실관람객탭:
        실관람객탭.click()
        time.sleep(2)

    리뷰_리스트_xpath = '//*[@class="lego_review_list _scroller"]/ul/li'
    리뷰_elements = driver.find_elements(By.XPATH, 리뷰_리스트_xpath)

    리뷰_list = []
    for i, 리뷰_element in enumerate(리뷰_elements, start=1):
        driver.execute_script("arguments[0].scrollIntoView(true);", 리뷰_element)
        time.sleep(1)

        if 리뷰_element:
            try:
                펼쳐보기_button = 리뷰_element.find_element(By.XPATH, './/button[@class="story_more _tail"]')
                if 펼쳐보기_button.is_displayed():
                    driver.execute_script("arguments[0].click();", 펼쳐보기_button)
                    time.sleep(1)
            except Exception as e:
                print(f"Error clicking '펼쳐보기' button: {e}")

            리뷰_html = 리뷰_element.get_attribute('outerHTML')
            soup = BeautifulSoup(리뷰_html, 'html.parser')

            spoiler_element = soup.find('span', class_='lego_text_spoiler _review_spoiler_text')
            if spoiler_element:
                continue

            작성자 = soup.find('dd', class_='this_text_stress _btn_writer').text.strip()
            작성일 = soup.find('dd', class_='this_text_normal').text.strip()
            별점 = soup.find('div', class_='area_text_box').text.strip().replace('별점(10점 만점 중)', '')
            리뷰내용 = soup.find('span', class_='desc _text')
            if 리뷰내용:
                리뷰내용 = 리뷰내용.text.strip()
            else:
                리뷰내용 = ""
            공감수 = soup.find('button', class_='area_button_upvote _btn_upvote').find('span', class_='this_text_number _count_num').text.strip()
            비공감수 = soup.find('button', class_='area_button_downvote _btn_downvote').find('span', class_='this_text_number _count_num').text.strip()

            리뷰 = {
                "작성자": 작성자,
                "작성일": 작성일,
                "별점": 별점,
                "리뷰내용": 리뷰내용,
                "공감수": 공감수,
                "비공감수": 비공감수
            }

            리뷰_list.append(리뷰)
        else:
            print("리뷰 정보를 찾을 수 없습니다.")

    movie_info["리뷰"] = 리뷰_list
    return movie_info

def save_progress(movie_info_list, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(movie_info_list, f, ensure_ascii=False, indent=4)

all_movie_info = []
progress_file = '영화리스트_progress.json'

# 이전 진행 상황을 불러오기
if os.path.exists(progress_file):
    with open(progress_file, 'r', encoding='utf-8') as f:
        all_movie_info = json.load(f)

# JSON 파일 읽기
with open('2016-2024_6_Korean_Movie_List_824_Movies.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 영화 제목 추출
movies = [movie['Title'] for year in data for month in data[year] for movie in data[year][month]]

# 이미 처리된 영화 제외
processed_titles = {movie['영화명'] for movie in all_movie_info}
movies_to_process = [movie for movie in movies if movie not in processed_titles]

# 영화 목록 순회하며 정보 수집
for movie in movies_to_process:
    try:
        print(f"Fetching info for movie: {movie}")
        url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화 {movie}"
        driver.get(url)
        
        tabs_xpath = '//*[@class="type_scroll _scroller _scroll _main_tab"]/div/ul[@class="tab_list"]/li[@class="tab _tab _item"]/a/span[@class="menu"]'
        tabs = driver.find_elements(By.XPATH, tabs_xpath)
        if not tabs:
            print(f"Menu format not found for movie: {movie}")
            continue  # 메뉴 포맷이 맞지 않으면 다음 영화로 넘어감
        
        movie_info = fetch_movie_info(movie)
        if movie_info:
            all_movie_info.append(movie_info)
        
        # 중간 저장
        save_progress(all_movie_info, progress_file)
    except Exception as e:
        print(f"An error occurred while processing {movie}: {e}")

# 최종 저장
with open('영화리스트.json', 'w', encoding='utf-8') as f:
    json.dump(all_movie_info, f, ensure_ascii=False, indent=4)

driver.quit()
