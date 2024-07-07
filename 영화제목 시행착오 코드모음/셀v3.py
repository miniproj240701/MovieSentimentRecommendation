import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

delay = 5  # 타임아웃 시간을 5초로 설정

def Class_Search(q):
    return WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, q))
    )

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

# 네이버 페이지 열기
driver.get(url='https://www.naver.com')

# 검색 입력 박스를 클래스 이름으로 찾기
search_box = Class_Search('search_input')

# 값 입력하기
search_box.send_keys("인사이드 아웃 2")

# 키보드 입력하기
search_box.send_keys(Keys.ENTER)

# 영화 제목 찾기 (XPath 사용)
title = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="area_text_title"]/strong[@class="_text"]'))
).text

# 개봉년도 찾기 (XPath 사용)
release_date = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="sub_title"]/span[@class="txt" and contains(text(), "2024")]'))
).text

# 상영시간 찾기 (XPath 사용)
runtime_full_text = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="detail_info"]//div[@class="info_group"][1]//dd'))
).text

# 상영시간만 추출 (정규 표현식 사용)
runtime_match = re.search(r'\d+분', runtime_full_text)
runtime = runtime_match.group(0) if runtime_match else 'N/A'

# 누적 관객 수 찾기 (XPath 사용)
audience_full_text = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="custom_info_list type_flex"]//div[@class="item_box"]//div[@class="item_info"]//span[@class="normal_text"]'))
).text

# 순위 / 부분을 제거하고 누적 관객 수만 추출
audience = audience_full_text.split('/')[1].strip()

# 감독 정보가 있는 요소 대기
casting_section_director = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="cm_content_area _cm_content_area_casting"]'))
)

# 이름, 역할, 이미지 URL 추출 (감독)
names_director = casting_section_director.find_elements(By.XPATH, './/strong[@class="name type_ell_2 _html_ellipsis"]//span[@class="_text"]')
roles_director = casting_section_director.find_elements(By.XPATH, './/span[@class="sub_text type_ell_2 _html_ellipsis"]//span[@class="_text"]')
images_director = casting_section_director.find_elements(By.XPATH, './/div[@class="thumb"]//img')

# 감독 정보 리스트 생성
cast_list = []
for name, role, image in zip(names_director, roles_director, images_director):
    cast_list.append({
        'name': name.text,
        'role': role.text,
        'image': image.get_attribute('src')
    })

# 주연 정보 추출 (XPath 사용)
names_main = WebDriverWait(driver, delay).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="title_box"]/strong[@class="name type_ell_2 _html_ellipsis"]/a[@class="_text"]'))
)

roles_main = WebDriverWait(driver, delay).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="title_box"]/span[@class="sub_text type_ell_2 _html_ellipsis"]/a[@class="_text"]'))
)

images_main = WebDriverWait(driver, delay).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="area_card"]/a[@class="area_link_box"]/div[@class="thumb"]/img'))
)

# 주연 정보 리스트 생성
for name, role, image in zip(names_main, roles_main, images_main):
    cast_list.append({
        'name': name.text,
        'role': role.text,
        'image': image.get_attribute('src')
    })

# 관람평 옆의 버튼 클릭 (XPath 사용)
rating_button = WebDriverWait(driver, delay).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@class="lego_rating_box_see"]'))
)

rating_button.click()

# 스크롤을 내리면서 댓글 데이터를 수집
comments = []

def scroll_and_collect_comments():
    try:
        # 현재 페이지의 댓글 데이터 수집
        comment_elements = driver.find_elements(By.XPATH, '//ul[@class="area_card_outer _item_wrapper"]/li[@class="area_card _item"]')
        for element in comment_elements:
            try:
                rating = len(element.find_elements(By.XPATH, './/span[@class="play_star  state_fill"]'))
                content = element.find_element(By.XPATH, './/div[@class="area_review_content"]/div[@class="area_text_expand _ellipsis"]//span[@class="desc _text"]').text
                author = element.find_element(By.XPATH, './/dl[@class="cm_upload_info"]/dd[@class="this_text_stress _btn_writer"]').text
                date = element.find_element(By.XPATH, './/dl[@class="cm_upload_info"]/dd[@class="this_text_normal"]').text

                # upvotes와 downvotes 요소가 존재하는지 확인
                try:
                    upvotes = element.find_element(By.XPATH, './/button[@class="area_button_upvote  _btn_upvote"]/span[@class="this_text_number _count_num"]').text
                except:
                    upvotes = '0'

                try:
                    downvotes = element.find_element(By.XPATH, './/button[@class="area_button_downvote  _btn_downvote"]/span[@class="this_text_number _count_num"]').text
                except:
                    downvotes = '0'

                comments.append({
                    'rating': rating,
                    'content': content,
                    'author': author,
                    'date': date,
                    'upvotes': upvotes,
                    'downvotes': downvotes
                })
            except Exception as e:
                print(f"Error while collecting a comment: {e}")
    except Exception as e:
        print(f"Error while collecting comments: {e}")

# 초기 댓글 데이터 수집
scroll_and_collect_comments()

# 더 많은 댓글이 로드될 때까지 스크롤
scroll_div = driver.find_element(By.XPATH, '//div[@class="lego_review_list _scroller"]')
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_div)
while True:
    # 스크롤을 맨 아래로 내리기
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)
    try:
        WebDriverWait(driver, delay, poll_frequency=0.1).until(
            lambda driver: driver.execute_script("return arguments[0].scrollHeight", scroll_div) > last_height
        )
    except TimeoutException:
        print("No more comments to load or timeout reached.")
        break

    # 새로운 댓글 데이터 수집
    scroll_and_collect_comments()
    
    # 더 많은 댓글이 로드되었는지 확인
    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_div)
    if new_height == last_height:
        break
    last_height = new_height

lst = {
    'title': title,
    'release_date': release_date,
    'runtime': runtime,
    'audience': audience,
    'cast': cast_list,  # 감독/출연 정보 리스트
    'comments': comments  # 댓글 데이터 리스트
}

print(lst)
