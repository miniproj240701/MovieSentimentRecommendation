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

# 값 입력하기
search_box.send_keys("인사이드 아웃 2")

# 키보드 입력하기
search_box.send_keys(Keys.ENTER)


"""
div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="title_area type_keep _title_area"
h2 class="title _title_ellipsis"
span class="area_text_title"
strong class="_text" 인사이드 아웃 2
"""

# 영화 제목 찾기 (XPath 사용)
title = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="area_text_title"]/strong[@class="_text"]'))
).text

"""
div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="title_area type_keep _title_area"
div class="sub_title"
span class="txt" 영화
span class="cm_bar"
span class="txt" Inside Out 2
span class="cm_bar"
span class="txt" 2024
"""

# 개봉년도 찾기 (XPath 사용)
release_date = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="sub_title"]/span[@class="txt" and contains(text(), "2024")]'))
).text

"""
div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="cm_content_wrap"
div class="cm_top_video _cm_content_area_video _button_scroller_fixed_top_video"
div class="cm_content_area _cm_content_area_info"
div class="cm_info_box"
div class="detail_info"
<a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.poster&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bkEw&amp;pkid=68&amp;os=32619620&amp;qvt=0&amp;query=%EC%9D%B8%EC%82%AC%EC%9D%B4%EB%93%9C%20%EC%95%84%EC%9B%83%202%20%ED%8F%AC%ED%86%A0" class="thumb _item"> <img src="https://search.pstatic.net/common?type=o&amp;size=176x264&amp;quality=85&amp;direct=true&amp;src=https%3A%2F%2Fs.pstatic.net%2Fmovie.phinf%2F20240612_151%2F1718180074487NH0V5_JPEG%2Fmovie_image.jpg%3Ftype%3Dw640_2" width="88" height="132" alt="인사이드 아웃 2" class="_img"> </a>
<div class="info ">
<div class="info_group"> <dt><span class="cm_bar"></span>개요</dt> <dd>애니메이션<span class="cm_bar_info"></span>미국<span class="cm_bar_info"></span>96분</dd> </div>
<div class="info_group"> <dt><span class="cm_bar"></span>개봉</dt> <dd>2024.06.12.</dd> </div>
</div>
"""

# 상영시간 찾기 (XPath 사용)
runtime_full_text = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="detail_info"]//div[@class="info_group"][1]//dd'))
).text

# 상영시간만 추출 (정규 표현식 사용)
runtime_match = re.search(r'\d+분', runtime_full_text)
runtime = runtime_match.group(0) if runtime_match else 'N/A'
"""
div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="cm_content_wrap"
div class="cm_top_video _cm_content_area_video _button_scroller_fixed_top_video"
div class="cm_content_area _cm_content_area_info"
div class="cm_info_box"
div class="detail_info"
div class="custom_info_wrap"
div class="custom_info_area"
div class="custom_info_list type_flex"
div class="item_area"
<div class="item_box"> <strong class="item_title">순위 <span class="ico_dot"></span> 누적 관객수</strong> <div class="item_info"> <span class="normal_text"><em>1</em>위 / <em>572</em>만명</span> </div> </div>
"""
# 누적 관객 수 찾기 (XPath 사용)
audience_full_text = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@class="custom_info_list type_flex"]//div[@class="item_box"]//div[@class="item_info"]//span[@class="normal_text"]'))
).text

# 순위 / 부분을 제거하고 누적 관객 수만 추출
audience = audience_full_text.split('/')[1].strip()

"""
div class="sc_new cs_common_module case_empasis color_14 _au_movie_content_wrap"
div class="cm_top_wrap _sticky _custom_select _header"
div class="cm_content_wrap"
div class="cm_top_video _cm_content_area_video _button_scroller_fixed_top_video"
div class="cm_content_area _cm_content_area_info"
div class="cm_content_area _cm_content_area_casting"
div class="cm_info_box scroll_img_vertical_95_127"
h3 class="middle_title" 감독/출연
div class="scroll_box _button_scroller_fixed"
<div class="list_info _scroller" style="user-select: none; -webkit-user-drag: none; touch-action: auto;"> <div> <ul class="list"> <li class="_item"> <div class="area_card"> <div class="thumb"> <img src="https://ssl.pstatic.net/sstatic/keypage/outside/scui/cs_common_module/im/no_img_people_206x232_v2.png" width="87" height="98" alt="이미지 준비중"> </div> <div class="title_box"> <strong class="name type_ell_2 _html_ellipsis" style="max-height:4.8rem"><span class="_text">켈시 맨</span></strong><span class="sub_text type_ell_2 _html_ellipsis" style="max-height:4.8rem"><span class="_text">감독</span></span> </div> </div> </li> <li class="_item"> <div class="area_card"> <a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=94861&amp;qvt=0&amp;query=%EC%97%90%EC%9D%B4%EB%AF%B8%20%ED%8F%AC%EC%97%98%EB%9F%AC" class="area_link_box"> <div class="thumb"> <img src="https://search.pstatic.net/common?type=f&amp;size=174x196&amp;quality=75&amp;direct=true&amp;src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F84%2F201803081945155321.jpg" width="87" height="98" alt="에이미 포엘러" onerror="this.onerror=null;this.src='https://ssl.pstatic.net/sstatic/keypage/outside/scui/cs_common_module/im/no_img_people_206x232_v2.png';this.className='no_img';this.alt='이미지 준비중';"> </div> </a> <div class="title_box"> <strong class="name type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=94861&amp;qvt=0&amp;query=%EC%97%90%EC%9D%B4%EB%AF%B8%20%ED%8F%AC%EC%97%98%EB%9F%AC" class="_text">에이미 포엘러</a></strong><span class="sub_text type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=94861&amp;qvt=0&amp;query=%EC%97%90%EC%9D%B4%EB%AF%B8%20%ED%8F%AC%EC%97%98%EB%9F%AC" class="_text">주연</a></span> </div> </div> </li> <li class="_item"> <div class="area_card"> <a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=14011173&amp;qvt=0&amp;query=%EB%A7%88%EC%95%BC%20%ED%98%B8%ED%81%AC" class="area_link_box"> <div class="thumb"> <img src="https://search.pstatic.net/common?type=f&amp;size=174x196&amp;quality=75&amp;direct=true&amp;src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F172%2F202005061826347831.jpg" width="87" height="98" alt="마야 호크" onerror="this.onerror=null;this.src='https://ssl.pstatic.net/sstatic/keypage/outside/scui/cs_common_module/im/no_img_people_206x232_v2.png';this.className='no_img';this.alt='이미지 준비중';"> </div> </a> <div class="title_box"> <strong class="name type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=14011173&amp;qvt=0&amp;query=%EB%A7%88%EC%95%BC%20%ED%98%B8%ED%81%AC" class="_text">마야 호크</a></strong><span class="sub_text type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=14011173&amp;qvt=0&amp;query=%EB%A7%88%EC%95%BC%20%ED%98%B8%ED%81%AC" class="_text">주연</a></span> </div> </div> </li> <li class="_item"> <div class="area_card"> <a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=14082447&amp;qvt=0&amp;query=%EB%A3%A8%EC%9D%B4%EC%8A%A4%20%EB%B8%94%EB%9E%99" class="area_link_box"> <div class="thumb"> <img src="https://search.pstatic.net/common?type=f&amp;size=174x196&amp;quality=75&amp;direct=true&amp;src=https%3A%2F%2Fssl.pstatic.net%2Fimgmovie%2Fmdi%2Fpi%2F000001169%2F00000116932-t.jpg" width="87" height="98" alt="루이스 블랙" onerror="this.onerror=null;this.src='https://ssl.pstatic.net/sstatic/keypage/outside/scui/cs_common_module/im/no_img_people_206x232_v2.png';this.className='no_img';this.alt='이미지 준비중';"> </div> </a> <div class="title_box"> <strong class="name type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=14082447&amp;qvt=0&amp;query=%EB%A3%A8%EC%9D%B4%EC%8A%A4%20%EB%B8%94%EB%9E%99" class="_text">루이스 블랙</a></strong><span class="sub_text type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=14082447&amp;qvt=0&amp;query=%EB%A3%A8%EC%9D%B4%EC%8A%A4%20%EB%B8%94%EB%9E%99" class="_text">주연</a></span> </div> </div> </li> <li class="_item"> <div class="area_card"> <a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=159823&amp;qvt=0&amp;query=%ED%95%84%EB%A6%AC%EC%8A%A4%20%EC%8A%A4%EB%AF%B8%EC%8A%A4" class="area_link_box"> <div class="thumb"> <img src="https://search.pstatic.net/common?type=f&amp;size=174x196&amp;quality=75&amp;direct=true&amp;src=https%3A%2F%2Fssl.pstatic.net%2Fimgmovie%2Fmdi%2Fpi%2F000001305%2FPM130512_181135_000.jpg" width="87" height="98" alt="필리스 스미스" onerror="this.onerror=null;this.src='https://ssl.pstatic.net/sstatic/keypage/outside/scui/cs_common_module/im/no_img_people_206x232_v2.png';this.className='no_img';this.alt='이미지 준비중';"> </div> </a> <div class="title_box"> <strong class="name type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=159823&amp;qvt=0&amp;query=%ED%95%84%EB%A6%AC%EC%8A%A4%20%EC%8A%A4%EB%AF%B8%EC%8A%A4" class="_text">필리스 스미스</a></strong><span class="sub_text type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=159823&amp;qvt=0&amp;query=%ED%95%84%EB%A6%AC%EC%8A%A4%20%EC%8A%A4%EB%AF%B8%EC%8A%A4" class="_text">주연</a></span> </div> </div> </li> <li class="_item"> <div class="area_card"> <a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=151951&amp;qvt=0&amp;query=%ED%86%A0%EB%8B%88%20%ED%97%A4%EC%9D%BC" class="area_link_box"> <div class="thumb"> <img src="https://search.pstatic.net/common?type=f&amp;size=174x196&amp;quality=75&amp;direct=true&amp;src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F4%2F201711061110575921.png" width="87" height="98" alt="토니 헤일" onerror="this.onerror=null;this.src='https://ssl.pstatic.net/sstatic/keypage/outside/scui/cs_common_module/im/no_img_people_206x232_v2.png';this.className='no_img';this.alt='이미지 준비중';"> </div> </a> <div class="title_box"> <strong class="name type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=151951&amp;qvt=0&amp;query=%ED%86%A0%EB%8B%88%20%ED%97%A4%EC%9D%BC" class="_text">토니 헤일</a></strong><span class="sub_text type_ell_2 _html_ellipsis" style="max-height:4.8rem"><a nocr="" onclick="return goOtherCR(this, 'a=nco_x0a*A.cast&amp;r=1&amp;i=1800009D_000001F1BC64&amp;u=' + urlencode(this.href));" href="?where=nexearch&amp;sm=tab_etc&amp;mra=bjky&amp;pkid=1&amp;os=151951&amp;qvt=0&amp;query=%ED%86%A0%EB%8B%88%20%ED%97%A4%EC%9D%BC" class="_text">주연</a></span> </div> </div> </li> </ul> </div> </div>

# 주연 정보 추출 (XPath 사용)
names = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="title_box"]/strong[@class="name type_ell_2 _html_ellipsis"]/a[@class="_text"]'))
)

roles = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="title_box"]/span[@class="sub_text type_ell_2 _html_ellipsis"]/a[@class="_text"]'))
)

images = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="area_card"]/a[@class="area_link_box"]/div[@class="thumb"]/img'))
)

# 주연 정보 리스트 생성
cast_list = []
for name, role, image in zip(names, roles, images):
    cast_list.append({
        'name': name.text,
        'role': role.text,
        'image': image.get_attribute('src')
    })
    
# 감독 정보가 있는 요소 대기
casting_section = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="cm_content_area _cm_content_area_casting"]'))
)

# 이름, 역할, 이미지 URL 추출
names = casting_section.find_elements(By.XPATH, './/strong[@class="name type_ell_2 _html_ellipsis"]//span[@class="_text"]')
roles = casting_section.find_elements(By.XPATH, './/span[@class="sub_text type_ell_2 _html_ellipsis"]//span[@class="_text"]')
images = casting_section.find_elements(By.XPATH, './/div[@class="thumb"]//img')

# 감독 정보 리스트 생성
cast_list = []
for name, role, image in zip(names, roles, images):
    cast_list.append({
        'name': name.text,
        'role': role.text,
        'image': image.get_attribute('src')
    })
"""

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
    
lst = {
    'title': title,
    'release_date': release_date,
    'runtime': runtime,
    'audience': audience,
    'cast': cast_list  # 감독/출연 정보 리스트
#     'rating': rating
}

print(lst)