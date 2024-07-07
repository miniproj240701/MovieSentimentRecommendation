from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Chrome WebDriver 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

# URL 설정
url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2010150&qvt=0&query=%ED%94%84%EB%9E%91%EC%8A%A4%20%EC%98%81%ED%99%94%EC%B2%98%EB%9F%BC%20%EA%B4%80%EB%9E%8C%ED%8F%89"
driver.get(url)

# 페이지가 로드될 때까지 잠시 대기
time.sleep(5)

# BeautifulSoup을 사용해 HTML 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 더 많은 댓글이 로드될 때까지 스크롤
scroll_div = driver.find_element(By.XPATH, '//div[@class="lego_review_list _scroller"]')
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_div)

try:
    # 리뷰 영역 추출
    review_list = soup.select('ul.area_card_outer._item_wrapper li.area_card._item')

    # 데이터 추출 및 출력
    for review in review_list:
        try:
            # 펼쳐보기 버튼이 있으면 클릭
            try:
                more_button = review.select_one('.//button[@class="story_more _tail"]')
                if more_button and more_button.is_displayed():
                    more_button.click()
            except:
                pass
            
            # 별점 계산
            stars = review.select('div.lego_movie_pure_star span.play_star')
            rating = sum(1 for star in stars if 'state_fill' in star['class'])
            
            comment_elem = review.select_one('div.area_review_content span.desc._text')
            date_elem = review.select_one('dd.this_text_normal')

            # upvotes와 downvotes 요소가 존재하는지 확인
            try: 
                upvotes = review.select_one('button.area_button_upvote span.this_text_number._count_num').text.strip()
            except: 
                upvotes = '0'

            try:  
                downvotes = review.select_one('button.area_button_downvote span.this_text_number._count_num').text.strip()
            except: 
                downvotes = '0'
            
            comment = comment_elem.text.strip() if comment_elem else 'N/A'
            date = date_elem.text.strip() if date_elem else 'N/A'
            
            # 스크롤을 맨 아래로 내리기
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="area_card_outer _item_wrapper"]/li[@class="area_card _item"][last()]'))
            )
            print(f"Rating: {rating}")
            print(f"Comment: {comment}")
            print(f"Date: {date}")
            print(f"Upvotes: {upvotes}")
            print(f"Downvotes: {downvotes}")
            print("-" * 50)
        except Exception as e:
            print(f"Error while collecting a comment: {e}")
except Exception as e:
    print(f"Error while collecting comments: {e}")
    
# 웹드라이버 종료
driver.quit()
