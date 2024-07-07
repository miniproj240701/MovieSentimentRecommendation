from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# WebDriver 설정 및 페이지 로드
driver = webdriver.Chrome()
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=1840411&qvt=0&query=영화%20나를%20잊지%20말아요%20보러가기')

# '보러가기' 탭 클릭 (필요 시)
def click_tab_by_text(driver, text):
    tabs = driver.find_elements(By.CSS_SELECTOR, '.tab_list .tab .menu')
    for tab in tabs:
        if tab.text == text:
            tab.click()
            time.sleep(1)
            break

click_tab_by_text(driver, '보러가기')

# 스트리밍 옵션과 가격 정보를 담을 리스트 초기화
streaming_options = []

# HTML 요소에서 스트리밍 정보 추출
try:
    streaming_html = driver.find_element(By.CSS_SELECTOR, ".ott_list_area.state_open").get_attribute('outerHTML')
    soup = BeautifulSoup(streaming_html, 'html.parser')

    # 각 스트리밍 옵션의 세부 정보 추출
    price_items = soup.find_all('li')
    for item in price_items:
        try:
            price_text = item.find('span', class_='info_price').get_text(strip=True) if item.find('span', class_='info_price') else "가격 정보 없음"
            platform_tag = item.find('a', class_='thumb')
            link = platform_tag['href'] if platform_tag and 'href' in platform_tag.attrs else None  # 스트리밍 페이지로의 링크

            streaming_options.append({
                "가격": price_text,
                "링크": link
            })
        except Exception as e:
            print(f"Error parsing item: {e}")
            continue
except Exception as e:
    print(f"Error fetching streaming options: {e}")

# 스트리밍 옵션이 없으면 빈 리스트로 설정
if not streaming_options:
    streaming_options = []

print(streaming_options)  # 디버깅용 출력

# 드라이버 종료
driver.quit()
