import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html

def Class_Search(q):
    return WebDriverWait(driver, 10).until(
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

# 클릭하기 (클릭은 필요 없을 수 있음, 주석 처리)
# search_box.click()

# 값 입력하기
search_box.send_keys("인사이드 아웃 2")

# 키보드 입력하기
search_box.send_keys(Keys.ENTER)

# 영화 제목 찾기 (XPath 사용)
title = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="area_text_title"]/strong[@class="_text"]'))
).text

# 개봉년도 찾기 (XPath 사용)
release_date = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="sub_title"]/span[@class="txt" and contains(text(), "2024")]'))
).text

# 상영시간 찾기 (XPath 사용)
runtime_full_text = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="detail_info"]//div[@class="info_group"][1]//dd'))
).text

# 상영시간만 추출 (정규 표현식 사용)
runtime_match = re.search(r'\d+분', runtime_full_text)
runtime = runtime_match.group(0) if runtime_match else 'N/A'

# 누적 관객 수 찾기 (XPath 사용)
audience_full_text = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="custom_info_list type_flex"]//div[@class="item_box"]//div[@class="item_info"]//span[@class="normal_text"]'))
).text

# 순위 / 부분을 제거하고 누적 관객 수만 추출
audience = audience_full_text.split('/')[1].strip()

# 감독 정보가 있는 요소 대기
casting_section_director = WebDriverWait(driver, 10).until(
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
names_main = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="title_box"]/strong[@class="name type_ell_2 _html_ellipsis"]/a[@class="_text"]'))
)

roles_main = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="title_box"]/span[@class="sub_text type_ell_2 _html_ellipsis"]/a[@class="_text"]'))
)

images_main = WebDriverWait(driver, 10).until(
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
rating_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@class="lego_rating_box_see"]'))
)

rating_button.click()

"""
div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="cm_content_wrap"
div class="cm_content_area _cm_content_area_rating"
div class="cm_pure_box lego_rating_slide_outer"
div class="cm_tap_area _tab_wrap"
div class="_content_chart" data-tab="audience"
div class="_content_chart" data-tab="netizen"
div class="_content" data-tab="audience"
div class="lego_review_write _comment_wrap"
<div class="lego_review_list _scroller"> <ul class="area_card_outer _item_wrapper" style="display: block;">
			<li class="area_card _item" data-rating-id="19692511" data-movie-code="235499" data-rating-point-type="after" data-report-service-available="true" data-report-service-type="AfterPoint" data-report-writer-id="fnrd****" data-report-encrypted-id="mHe1892SHJNS7EuNbS7khHKrm2I9/CXP43OmsbkZQtc=" data-report-title="“어른이 된다는게 이런건가봐 기쁨이 줄어드는거“ " data-report-nid="19692511" data-report-time="20240612 12:07">
			  <div class="area_title_box">
    <div class="lego_movie_pure_star">
      <div class="area_icon_box">
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
      </div>
      <div class="area_text_box"><span class="blind">별점(10점 만점 중)</span>10</div>
    </div>
			  </div>
			  
			  
			  
			  <div class="area_review_content">
			    <div class="area_text_expand _ellipsis" style="max-height:7.2rem;" data-ellipsis-managed="0" data-ellipsis-omitted="false" data-ellipsis-row="1">
			        <span class="lego_badge_movie_visit">관람객</span>
			      <span class="desc _text">“어른이 된다는게 이런건가봐 기쁨이 줄어드는거“ </span>
			      <button onclick="tCR('a=nco_x0a*A.tabreviewmore&amp;r=1&amp;i=1800009D_000001F1BC64');" type="button" class="story_more _tail" style="display:none;"><span class="blind">펼쳐보기</span></button>
			    </div>
			  </div>
			  <dl class="cm_upload_info">
			    <dt class="blind">작성자</dt>
			    <dd class="this_text_stress _btn_writer" data-writer-id="fnrd****">fnrd****</dd>
			    <dt class="blind">작성일</dt>
			    <dd class="this_text_normal">2024.06.12. 12:07</dd>
			    
				    <dt class="blind">신고여부</dt>
				    <dd class="this_text_normal"><a nocr="" onclick="goOtherTCR(this, 'a=nco_x0a*A.tabdialoguereport&amp;r=1&amp;i=');return false;" href="#" class="this_play_btn _btn_report">신고</a></dd>
			  </dl>
			  <div class="cm_sympathy_area">
			    <button onclick="tCR('a=nco_x0a*A.tabempathy&amp;r=1&amp;i=1800009D_000001F1BC64');" type="button" class="area_button_upvote  _btn_upvote">
			      <span class="this_text_number _count_num">6,567</span>
			    </button>
			    <button onclick="tCR('a=nco_x0a*A.tabnonempathy&amp;r=1&amp;i=1800009D_000001F1BC64');" type="button" class="area_button_downvote  _btn_downvote">
			      <span class="this_text_number _count_num">210</span>
			    </button>
			  </div>
			</li>
</ul>


div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="cm_content_wrap"
div class="cm_content_area _cm_content_area_rating"
div class="cm_pure_box lego_rating_slide_outer"
div class="cm_tap_area _tab_wrap"
div class="_content_chart" data-tab="audience"
div class="_content_chart" data-tab="netizen"
div class="_content" data-tab="audience"
div class="lego_review_write _comment_wrap"
<div class="lego_review_list _scroller"> <ul class="area_card_outer _item_wrapper" style="display: block;">
<li class="area_card _item" data-rating-id="19693442" data-movie-code="235499" data-rating-point-type="after" data-report-service-available="true" data-report-service-type="AfterPoint" data-report-writer-id="sim9****" data-report-encrypted-id="hn1N5dSRYy26ReEW0x3ktFEH+HrgbQfnsKIg8Kh37XY=" data-report-title="디즈니 애니들의 대표적인 그런.. 딱 기억에 남는 ost가 빠진게 아쉽지만? 그 외에 영상미, 스토리, 감동.. 그저 인사이드아웃2는 진짜 기억에 오래 남을 영화였어요.. 이게 진짜 어른애니메이션인가싶네요 :)방금 나왔는데 금방 또 보고 싶어지네요.적극 추천합니다!! 사랑합니다 픽사, 디즈니! " data-report-nid="19693442" data-report-time="20240612 21:43">
			  <div class="area_title_box">
    <div class="lego_movie_pure_star">
      <div class="area_icon_box">
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
        <div class="area_card">
          <span class="play_star  state_fill"></span>
          <span class="play_star  state_fill"></span>
        </div>
      </div>
      <div class="area_text_box"><span class="blind">별점(10점 만점 중)</span>10</div>
    </div>
			  </div>
			  
			  
			  
			  <div class="area_review_content">
			    <div class="area_text_expand _ellipsis" style="max-height:7.2rem;" data-ellipsis-managed="135" data-ellipsis-omitted="true" data-ellipsis-row="3">
			        <span class="lego_badge_movie_visit">관람객</span>
			      <span class="desc _text">디즈니 애니들의 대표적인 그런.. 딱 기억에 남는 ost가 빠진게 아쉽지만? 그 외에 영상미, 스토리, 감동.. 그저 인사이드아웃2는 진짜 기억에 오래 남을 영화였어요.. 이게 진짜 어른애니메이션인가싶네요 :)방금 나왔는데 금방 또 보고 싶어지네요.적극 ...</span>
			      <button onclick="tCR('a=nco_x0a*A.tabreviewmore&amp;r=1&amp;i=1800009D_000001F1BC64');" type="button" class="story_more _tail" style=""><span class="blind">펼쳐보기</span></button>
			    </div>
			  </div>
			  <dl class="cm_upload_info">
			    <dt class="blind">작성자</dt>
			    <dd class="this_text_stress _btn_writer" data-writer-id="sim9****">sim9****</dd>
			    <dt class="blind">작성일</dt>
			    <dd class="this_text_normal">2024.06.12. 21:43</dd>
			    
				    <dt class="blind">신고여부</dt>
				    <dd class="this_text_normal"><a nocr="" onclick="goOtherTCR(this, 'a=nco_x0a*A.tabdialoguereport&amp;r=1&amp;i=');return false;" href="#" class="this_play_btn _btn_report">신고</a></dd>
			  </dl>
			  <div class="cm_sympathy_area">
			    <button onclick="tCR('a=nco_x0a*A.tabempathy&amp;r=1&amp;i=1800009D_000001F1BC64');" type="button" class="area_button_upvote  _btn_upvote">
			      <span class="this_text_number _count_num">15</span>
			    </button>
			    <button onclick="tCR('a=nco_x0a*A.tabnonempathy&amp;r=1&amp;i=1800009D_000001F1BC64');" type="button" class="area_button_downvote  _btn_downvote">
			      <span class="this_text_number _count_num">3</span>
			    </button>
			  </div>
			</li>
</ul>
"""
# 스크롤을 내리면서 댓글 데이터를 수집
comments = []

def scroll_and_collect_comments():
    try:
        # 현재 페이지의 댓글 데이터 수집
        comment_elements = driver.find_elements(By.XPATH, '//ul[@class="area_card_outer _item_wrapper"]/li[@class="area_card _item"]')
        for element in comment_elements:
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
        print(f"Error while collecting comments: {e}")

# 초기 댓글 데이터 수집
scroll_and_collect_comments()

# 더 많은 댓글이 로드될 때까지 스크롤
scroll_div = driver.find_element(By.XPATH, '//div[@class="lego_review_list _scroller"]')
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_div)
while True:
    # 스크롤을 맨 아래로 내리기
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return arguments[0].scrollHeight", scroll_div) > last_height
    )
    
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