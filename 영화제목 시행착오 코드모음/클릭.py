from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver 설정 (예: Chrome)
driver = webdriver.Chrome()

# 네이버 영화 페이지로 이동
driver.get("https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2010150&qvt=0&query=%ED%94%84%EB%9E%91%EC%8A%A4%20%EC%98%81%ED%99%94%EC%B2%98%EB%9F%BC")

# 페이지 로딩 대기 시간 설정
delay = 10  # 초 단위

try:
    # 관람평 탭 버튼 클릭
    # '관람평' 탭을 기다렸다가 클릭
    관람평_탭 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="menu" and text()="관람평"]'))
    )
    관람평_탭.click()
    print("관람평 탭 버튼을 클릭했습니다.")
    
    # 잠시 대기하여 페이지가 완전히 로드되도록 함
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '//a[@class="more_link" and contains(@onclick, "ratingmore")]'))
    )
    
    # '더보기' 버튼 클릭
    rating_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@class="more_link" and contains(@onclick, "ratingmore")]'))
    )
    rating_button.click()
    print("더보기 버튼을 클릭했습니다.")
except Exception as e:
    print(f"오류 발생: {e}")

# 필요에 따라 추가적인 작업 수행

# WebDriver 종료
driver.quit()
