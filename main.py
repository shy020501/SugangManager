from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import argparse
from distutils.util import strtobool 

class SugangManager:
    def __init__(self):
        """
        수강신청 매니저 초기화
        """
        self.setup_driver()

    def setup_driver(self):
        """
        크롬 드라이버 설정 및 초기화
        """
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--ignore-certificate-errors')
        
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # chrome_options.add_argument('--headless=new')
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
        except Exception as e:
            print("Failed to initialize Chrome driver:")
            raise e
            
        self.wait = WebDriverWait(self.driver, 10)
        
    def input_login(self, user_id, user_pw):
        """
        학번, 비번 칸 자동 입력
        
        Args:
            user_id (str): 학번
            user_pw (str): 비밀번호
        """
        id_input = self.driver.find_element(By.ID, "id")
        id_input.clear()
        id_input.send_keys(user_id) 
        
        time.sleep(random.uniform(1.0, 2.0))
        
        pw_input = self.driver.find_element(By.ID, "pwd")
        pw_input.clear()
        pw_input.send_keys(user_pw)

        time.sleep(random.uniform(1.0, 2.0))
        
        
    def run_mananger(self, user_id, user_pw, grade, to_integrate, classes, min_wait_time, max_wait_time):
        """
        반복적으로 수강신청 페이지 확인 후, 빈자리가 있으면 자동으로 신청
        
        Args:
            user_id (str): 학번
            user_pw (str): 비밀번호
            grade (str): 학년 (1~4)
            to_integrate (bool): TO 통합 수강신청인지 여부 (맞으면 True)
            classes (list[str]): 수강 신청할 수업(들)의 학수번호 (분반까지)
            min_wait_time (float): 최소 대기 시간 (매크로 방지)
            max_wait_time (float): 최대 대기 시간 (매크로 방지)
        """
        self.driver.get("https://sugang.skku.edu/")
        while True:
            time.sleep(random.uniform(min_wait_time, max_wait_time))
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame("Main")
            try:
                login_button = self.driver.find_element(By.ID, "btn_login")
                self.input_login(user_id, user_pw)
                login_button.click()
                
            except NoSuchElementException:
                iframe_element = self.driver.find_element(By.ID, "contentFrame")
                self.driver.switch_to.frame(iframe_element)
                self.driver.switch_to.frame("topFrame")
                
                menu = self.driver.find_element(By.ID, "cssmenu")
                li_elements = menu.find_elements(By.TAG_NAME, "li")
                
                if len(li_elements) > 1:
                    second_li = li_elements[1]

                    sugang_btn = second_li.find_element(By.TAG_NAME, "a")
                    sugang_btn.click()

                else:
                    print("수강신청 버튼 클릭 안됨. 보이면 나한테 톡 좀.")
                    
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame("Main")
                iframe_element = self.driver.find_element(By.ID, "contentFrame")
                self.driver.switch_to.frame(iframe_element)
                self.driver.switch_to.frame("mainFrame")
                
                try:
                    rows = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="listLecture"]//tr')))
                    valid_rows = [row for row in rows if row.get_attribute("id") and row.get_attribute("id").isdigit() and int(row.get_attribute("id")) >= 1]
                    
                except NoSuchElementException:
                    print("책가방에 담은 과목들 안불러와짐. 제대로 담겨있는지 확인하고, 담겨 있으면 나한테 톡 좀.")
                    
                try:
                    for row in valid_rows:
                        haksu_td = row.find_element(By.XPATH, './/td[@aria-describedby="listLecture_haksu_no"]')
                        haksu_no = haksu_td.text.strip()
                        
                        if haksu_no in classes:
                            if not to_integrate: # 티통 아닐 때는 학년 별 잔여 수업 확인
                                available_seats = row.find_element(By.XPATH, f'.//td[@aria-describedby="listLecture_jagwa{grade}"]').text.strip()
                            else: # 티통일 때는 전체 잔여 수업 확인
                                available_seats = row.find_element(By.XPATH, './/td[@aria-describedby="listLecture_tot_dhw"]').text.strip()
                            
                            current, total = map(int, available_seats.split(" / "))
                            if current < total:
                                print(f"강의 {haksu_no} 잔여석 존재")
                                apply_button = row.find_element(By.XPATH, './/td[@aria-describedby="listLecture_mode"]//span[contains(text(), "신청")]')
                                apply_button.click()
                                time.sleep(random.uniform(1.0, 2.0))
                                
                except Exception as e:
                    print(f"각 과목 탐색 중 오류 : {e}")
                    
    def __del__(self):
        """
        드라이버 정리
        """
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except:
            pass
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str, required=True, help="학번 입력")
    parser.add_argument('--pw', type=str, required=True, help="비밀번호 입력")
    parser.add_argument('--grade', type=str, required=True, help="학년 입력")
    parser.add_argument('--to_integrate', type=lambda x: bool(strtobool(x)), required=True, help="티통이면 True 아니면 False")
    parser.add_argument('--classes', nargs='+', required=True, help="들을 수업의 학수번호-분반 정확하게 입력")
    parser.add_argument('--min', type=float, required=False, default=3.0)
    parser.add_argument('--max', type=float, required=False, default=5.0)
    
    args = parser.parse_args()
    
    manager = SugangManager()
    manager.run_mananger(
        user_id=args.id, 
        user_pw=args.pw, 
        grade=args.grade, 
        to_integrate=args.to_integrate, 
        classes=args.classes, 
        min_wait_time=args.min, 
        max_wait_time=args.max
    )