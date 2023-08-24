from Modules.Find import Find
from Modules.Save import Save

import time
import datetime



class Tmcars:
    
    def __init__(self, Find, Save):
        self.Find = Find()
        self.Save = Save
        self.Find.get("https://tmcars.info/others/nedvijimost")
        
    @staticmethod
    def date_check(date_to_check):

        if "sag öň" in date_to_check:
            hours = int(date_to_check[:date_to_check.index("sag öň")].strip())
            formatted_date = (datetime.datetime.today() - datetime.timedelta(hours=hours)).strftime('%d.%m.%Y')

        elif "düýn" in date_to_check:
            formatted_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y')


        elif "gün öň" in date_to_check:
            days = int(date_to_check[:date_to_check.index("gün öň")].strip())
            formatted_date = (datetime.datetime.today() - datetime.timedelta(days=days)).strftime('%d.%m.%Y')

        elif "şu wagt" in date_to_check:
            formatted_date = datetime.datetime.today().strftime('%d.%m.%Y')

        else:
            formatted_date = date_to_check.strip()

        return formatted_date

    def parse_links(self):
        card_list = self.Find.xs("//div[@class='item7-card-img']/a")

        link_list = []

        for card in card_list:
            link_list.append(card.get_attribute('href'))

        self.Save.links(link_list)


    def parse_cards(self):
        with open("Parse_Files\\Links.txt", "r", encoding="utf8") as file:
                link_list = file.readline().split(",")[:-1]
                file.close()

        estate_list = []

        for count in range(len(link_list)):
            if count % 10 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, count)
                self.Save.links(link_list)


            link = link_list.pop(0)
            print(f"{count+1}. {link}")

            try:
                self.Find.get(link)
            except self.Find.WE:
                print("[Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
                pass

            if count < 2:
                try:
                    print("Ищу")
                    close_modal_button = self.Find.wait_until('//*[contains(@id, "popupModal")]//button[@class="close"]', 4)
                    print("Нашёл!")
                    close_modal_button.click()
                    time.sleep(2)
                except self.Find.TE:
                    print("TimeoutException")
                    pass
                except self.Find.ENIE:
                    print("ElementNotInteractableException")
                    time.sleep(5)
                    close_modal_button.click()
                    time.sleep(2)
                    pass

            card = [["Web ссылка", link]]

            try:
                Date_and_place = self.Find.x("//div[@class='list-id']/div/div/span").text.split("/")
            except self.Find.NSEE:
                # self.output("[Исключено] Объявление удаленно\n")
                continue


            Name = self.Find.x("//div[@class='item-det mb-4']/h1").text
            card.append(["Наименование", Name])


            try:
                Description = self.Find.x("//div[@class='mb-5 entry-content-text expanded']/p").text
            except self.Find.NSEE:
                pass


            date = Date_and_place.pop(-1)
            place = Date_and_place.pop(0)

            adress = ""
            for i in Date_and_place:
                adress += i.strip() + " "
            adress = adress.strip()

            card.append(["Местоположение", place])
            card.append(["Адрес", adress])
            card.append(["Дата публикации", self.date_check(date)])

            card.append(["Примечание", Description])

            try:
                info_list = self.Find.xs('//div[@class="table-responsive"]/table/tbody/tr')
            except self.Find.NSEE:
                continue

            for info in info_list:
                if "Цена" in info.text.split(":")[0]:
                    price = info.text.split(":")
                    card.append([price[0], price[1][:-3].replace(".","")])
                else:
                    card.append(info.text.split(":"))

            print("\n\n-----------\n",card,end="\n-----------\n\n")
            estate_list.append({key.strip(): value.strip() for key,value in card})


        self.Save.to_xlsx(estate_list, count)
        self.Save.links(link_list)

if __name__ == "__main__":
    Tmcars(Find, Save).parse_cards()