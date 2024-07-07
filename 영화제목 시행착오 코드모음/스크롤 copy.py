from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import json
import time

delay = 10  # 타임아웃 시간을 10초로 설정

# Chrome WebDriver 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

# URL 설정
url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2010150&qvt=0&query=%ED%94%84%EB%9E%91%EC%8A%A4%20%EC%98%81%ED%99%94%EC%B2%98%EB%9F%BC%20%EA%B4%80%EB%9E%8C%ED%8F%89"
driver.get(url)

# 페이지가 로드될 때까지 잠시 대기
WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//ul[@class="area_card_outer _item_wrapper"]/li[@class="area_card _item"]'))
)

# 댓글 데이터 수집
comments = []

try:
    # 현재 페이지의 댓글 데이터 수집
    review_list = driver.find_elements(By.XPATH, '//ul[@class="area_card_outer _item_wrapper"]/li[@class="area_card _item"]')
    for review in review_list:
        try:
            # 펼쳐보기 버튼이 있으면 클릭
            try:
                # more_button = review.find_element(By.XPATH, './/button[@class="story_more _tail"]')
                more_button = review.find_element(By.XPATH, '//div[@class="lego_review_list _scroller"]')
                if more_button.is_displayed():
                    more_button.click()
            except:
                pass

            # 별점 계산
            stars = review.find_elements(By.XPATH, './/span[@class="play_star state_fill"]')
            rating = len(stars)

            comment = review.find_element(By.XPATH, './/div[@class="area_review_content"]/div[@class="area_text_expand _ellipsis"]//span[@class="desc _text"]').text
            date = review.find_element(By.XPATH, './/dl[@class="cm_upload_info"]/dd[@class="this_text_normal"]').text
            author = review.find_element(By.XPATH, './/dl[@class="cm_upload_info"]/dd[@class="this_text_stress _btn_writer"]').text

            # upvotes와 downvotes 요소가 존재하는지 확인
            try:
                upvotes = review.find_element(By.XPATH, './/button[@class="area_button_upvote _btn_upvote"]/span[@class="this_text_number _count_num"]').text
            except:
                upvotes = '0'

            try:
                downvotes = review.find_element(By.XPATH, './/button[@class="area_button_downvote _btn_downvote"]/span[@class="this_text_number _count_num"]').text
            except:
                downvotes = '0'
            
            # 댓글 내용이 공백이 아니고, 스포일러를 포함하지 않는 경우에만 추가
            if comment.strip() and '스포일러' not in comment:
                comments.append({
                    'rating': rating,
                    'content': comment,
                    'author': author,
                    'date': date,
                    'upvotes': upvotes,
                    'downvotes': downvotes
                })
        except Exception as e:
            print(f"Error while collecting a comment: {e}")
except Exception as e:
    print(f"Error while collecting comments: {e}")

# 결과 출력
for comment in comments:
    print(f"Rating: {comment['rating']}")
    print(f"Comment: {comment['content']}")
    print(f"Date: {comment['date']}")
    print(f"Upvotes: {comment['upvotes']}")
    print(f"Downvotes: {comment['downvotes']}")
    print("-" * 50)

# JSON 파일로 저장
with open('movie_comments.json', 'w', encoding='utf-8') as f:
    json.dump({'comments': comments}, f, ensure_ascii=False, indent=4)

print("Data has been saved to movie_comments.json")
driver.quit()
