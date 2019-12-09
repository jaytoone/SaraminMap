import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from urllib.request import urlopen
import time
import add_to_xy
import folium

# ----- MAP SETTING -----#
SaraminMap = folium.Map(location=[37.532193, 126.978330], zoom_start=13)


# ----- CRAWLING -----#
# url = "http://www.saramin.co.kr/zf_user/search?cat_cd=404%2C407%2C408%2C413&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&loc_mcd=101000&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
# url = input("크롤링할 url 주소를 입력해주세요 : ")
url = "http://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=default_mysearch&cat_key=60225%2C60616"
path = "C:/Users/Lenovo/PycharmProjects/BackTester/venv/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get(url)

i = 1
while True:

    try:
        loca = driver.find_elements_by_class_name("area_corp_info a")

        # 기업 정보 Click
        for j in range(len(loca)):

            loca[j].send_keys('\n')

            basic_tab = driver.window_handles[0]
            next_tab = driver.window_handles[1]
            driver.switch_to.window(window_name=next_tab)

            # 페이지에서 주소 정보 크롤링
            try:
                address = driver.find_element_by_class_name("txt_address")
                print(address.text, add_to_xy.location(address.text))
                folium.Marker([add_to_xy.location(address.text)[0], add_to_xy.location(address.text)[1]], popup=address.text).add_to(SaraminMap)

            except Exception as e:
                print("주소 데이터가 존재하지 않습니다.")

            driver.switch_to.window(window_name=basic_tab)

        # 페이지 넘기기
        page_number = driver.find_elements_by_class_name("page_nation a")
        page_number[i].click()
        i += 1
        SaraminMap.save('SaraminMap.html')

        if page_number[-1].text != '다음':
            if i == len(page_number):
                print()
                print("페이지 끝")
                break
        else:
            # 첫 페이지
            if len(page_number) == 10:  # i = 9, 페이지 넘어감
                if i >= 10:
                    i = 1
            else:  # i = 10, 페이지 넘어감
                if i >= 11:
                    i = 1
        print()

        # 페이지 로딩 시간
        time.sleep(1.5)

    except Exception as e:
        print("페이지 로딩 중 에러 발생!")
        print(e)

driver.close()
driver.quit()
