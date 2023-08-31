import time
import datetime



class Tmcars:
    
    def __init__(self, Find, Save):
        self.Find = Find()
        self.Save = Save
        try:
            self.Find.get("https://tmcars.info/others/nedvijimost")
        except self.Find.WE:
            print("[Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
            return 0
        
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

    def parse_links(self, count_pages=0):
        link_list = []

        if count_pages == 0:
            count_pages = round(int(self.Find.x("//div[@class='sorting-results']/h6/span").text.strip())/100)
            print(count_pages)

        
        for page in range(count_pages):
            self.Find.get(f"https://tmcars.info/others/nedvijimost?offset={page*100}&max=100&lang=ru")
            card_list = self.Find.xs("//div[@class='item7-card-img']/a")

            for card in card_list:
                link_list.append(card.get_attribute('href'))

        self.Save.links(link_list, "Tmcars")


    def parse_cards(self):
        with open(f"Parse_Files\\Links_Tmcars.txt", "r", encoding="utf8") as file:
                link_list = file.readline().split(",")[:-1]
                file.close()

        estate_list = []

        for count in range(len(link_list)):
            if count % 1000 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, "Tmcars", count)
                self.Save.links(link_list, "Tmcars")


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
                data = info.text.split(":")[0]
                if "Цена" in data:
                    price = info.text.split(":")[1][:-3].replace(".","")
                    card.append(["Цена предложения ТМТ", price])
                
                elif "Категория" in data:
                    target = info.text.split(":")[1]
                    target = target.split(" / ")[1][:target.split(" / ")[1].find(" ")]
                    card.append(["Цель", target])

                elif "Этаж" == data.strip():
                    card.append(["На каком этаже", info.text.split(":")[1]])

                elif "Ремонт" in data:
                    card.append(["Состояние ремонта", info.text.split(":")[1]])

                elif "Номер телефона" in data:
                    card.append(["Конт.номер", info.text.split(":")[1]])

                else:
                    card.append(info.text.split(":"))

            print("\n\n-----------\n",card,end="\n-----------\n\n")
            estate_list.append({key.strip(): value.strip() for key,value in card})


        self.Save.to_xlsx(estate_list, "Tmcars", count)
        self.Save.links(link_list)

if __name__ == "__main__":
    from Modules.Find import Find
    from Modules.Save import Save

    Tmcars = Tmcars(Find, Save)
    Tmcars.parse_links(0)
    # Tmcars.parse_cards()