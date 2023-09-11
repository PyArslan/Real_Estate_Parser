from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchDriverException
from selenium.common.exceptions import SessionNotCreatedException

from time import sleep
import datetime
import os
import urllib


""" Класс с упрощённым синтаксисом для более удобного нахождения элементов по xpath """
class Find:

    def __init__(self):
        
        option = Options()
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_argument("--disable-infobars")
        option.add_argument("--window-size=1900,1080")
        option.add_argument("--disable-notifications")

        self.today = datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        self.driver = webdriver.Chrome(options=option)
        # self.driver.set_window_position(-10000, 0, windowHandle='current')

        self.NSEE = NoSuchElementException
        self.TE = TimeoutException
        self.WE = WebDriverException
        self.SNCE = SessionNotCreatedException
        self.NSDE = NoSuchDriverException
        self.ENIE = ElementNotInteractableException

    def x(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)
    
    def xs(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    def xcl(self, xpath, method=1):
        if method == 1:
            self.driver.find_element(By.XPATH, xpath).click()
        elif method == 2:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, xpath))

    def xsk(self, xpath, keys):
        self.driver.find_element(By.XPATH, xpath).send_keys(keys)

    def refresh(self):
        self.driver.refresh()

    def get(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def wait_until(self, xpath, num):
        return WebDriverWait(self.driver, num).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def sshot(self,  filename, scroll):
        self.driver.execute_script("document.body.style.zoom='60%'")
        self.driver.execute_script(f"window.scrollTo(0, {scroll})")
        sleep(2)
        
        if not os.path.exists(f"Parse_Files\\Pictures_{self.today}"):
            os.makedirs(f"Parse_Files\\Pictures_{self.today}")

        self.driver.get_screenshot_as_file(f'Parse_Files\\Pictures_{self.today}\\{filename}.png') 

    def scroll(self, pos):
        self.driver.execute_script(f"window.scrollTo(0, {pos})")

    def image(self, src, filename):
        try:
            urllib.request.urlretrieve(src, filename)
        except urllib.error.URLError:
            sleep(3)
            urllib.request.urlretrieve(src, filename)
        except TypeError:
          print("TypeError during downloading file, continue")
