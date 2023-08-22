from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException
# from selenium.common.exceptions import ElementNotInteractableException
# from selenium.common.exceptions import NoSuchDriverException
# from selenium.common.exceptions import SessionNotCreatedException

import pandas as pd
import os
import time
import datetime

""" Класс с упрощённым синтаксисом для более удобного нахождения элементов по xpath """
class Find:

    def __init__(self):
        
        option = Options()
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_argument("--disable-infobars")
        option.add_argument("--window-size=1900,1080")
        # option.add_argument("--start-maximized")
        option.add_argument("--disable-notifications")

        self.today = datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        self.driver = webdriver.Chrome(options=option)
        self.driver.set_window_position(-10000, 0, windowHandle='current')


    def x(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)
    
    def xs(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    def xcl(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()

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
    
    def sshot(self,  filename):
        self.driver.execute_script("document.body.style.zoom='60%'")
        self.driver.execute_script("window.scrollTo(0, 200)")
        time.sleep(2)
        
        if not os.path.exists(f"Parse_Files\\Pictures_{self.today}"):
            os.makedirs(f"Parse_Files\\Pictures_{self.today}")

        self.driver.get_screenshot_as_file(f'Parse_Files\\Pictures_{self.today}\\{filename}.png') 

class Save:
    @staticmethod
    def to_xlsx(cars_list, count=0):

        data = {
            'Ссылка': [i['Ссылка'] for i in cars_list],
            'Файл': [i['Ссылка на файл'] if 'Ссылка на файл' in i else 'Не указано' for i in cars_list],
            'Марка': [i['Марка'] if 'Марка' in i else 'Не указано' for i in cars_list],
            'Модель': [i['Модель'] if 'Модель' in i else 'Не указано' for i in cars_list],
            'Год Выпуска': [i['Год'] if 'Год' in i else 'Не указано' for i in cars_list],
            'Кузов': [i['Кузов'] if 'Кузов' in i else 'Не указано' for i in cars_list],
            'Тип привода': [i['Тип привода'] if 'Тип привода' in i else 'Не указано' for i in cars_list],
            'Объем двигателя': [i['Мотор'] if 'Мотор' in i else 'Не указано' for i in cars_list],
            'Коробка ПП': [i['Коробка'] if 'Коробка' in i else 'Не указано' for i in cars_list],
            'Пробег км.': [i['Пробег'] if 'Пробег' in i else 'Не указано' for i in cars_list],
            'Цвет': [i['Цвет'] if 'Цвет' in i else 'Не указано' for i in cars_list],
            'Месторасположение': [i['Место'] if 'Место' in i else 'Не указано' for i in cars_list],
            'Телефон': [i['Номер телефона'] if 'Номер телефона' in i else 'Не указано' for i in cars_list],
            'Дата публикации': [i['Дата публикации'] if 'Дата публикации' in i else 'Не указано' for i in cars_list],
            'Цена предложения ТМТ': [int(i['Цена'].replace(".","")) if 'Цена' in i else 'Не указано' for i in cars_list],
            'Описание': [i['Описание'] if 'Описание' in i else 'Не указано' for i in cars_list]
        }

        df = pd.DataFrame(data)
        df.index += 1

        today = datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        df.to_excel(f'Parse_Files\\Tmcars_{today}_{count}_.xlsx', index=False)

    @staticmethod
    def links(link_list):
        
        with open("Parse_Files\\Links.txt", "w", encoding="utf8") as file:
            for i in link_list:
                file.write(f"{i},")

            file.close()

class Tmcars:
    
    def __init__(self, Find):
        self.Find = Find()
        self.Find.get("https://tmcars.info/others/nedvijimost")


    def parse_links(self):
        card_list = self.Find.xs("//div[@class='item7-card-img']/a")

        link_list = []

        for card in card_list:
            link_list.append(card.get_attribute('href'))

        Save.links(link_list)


    def parse_cards(self):
        pass