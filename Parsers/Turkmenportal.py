


class Turkmenportal:

    def __init__(self, Find, Save, stop_thread_check, output=print):
        self.Find = Find()
        self.Save = Save
        self.output = output
        self.stop_thread_check = stop_thread_check

        self.output("[Turkmenportal] Начинаю парсинг...")

        try:
            self.Find.get("https://turkmenportal.com/estates/nedvizhimost")
        except self.Find.WE:
            self.output("[Turkmenportal->Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
            return 0

    def parse_links(self, own_link, count_pages=0, path="D:\\ScreenshotsEstate\\", take_screenshots=1):
        link_list = []

        if count_pages == 0:
            pages = self.Find.x("//div[@class='row sub_categories horizontal minimized dynamic']").text.split("(")

            for elem in pages:
                pages[pages.index(elem)] = ''.join([i for i in elem if i.isdigit()])

            pages = [int(i) for i in pages if i]
            count_pages = round(sum(pages)/20)

        self.output(f"[Turkmenportal] Количество страниц: {count_pages}")
            

        for page in range(1, count_pages+1):
            if self.stop_thread_check() == True:
                self.Save.links(link_list, "Turkmenportal")
                self.output("[Turkmenportal] Парсинг ссылок успешно остановился!")
                return 1
            
            self.output(f"[Turkmenportal] Страница: {page}")
            self.Find.get(f"https://turkmenportal.com/estates/a/index?Estates_sort=date_added.desc&page={page}&path=nedvizhimost")
            card_list = self.Find.xs("//div[@class='entry-title']/a")

            for card in card_list:
                if "estates" in card.get_attribute('href'):
                    link_list.append(card.get_attribute('href'))

        self.Save.links(link_list, "Turkmenportal")
        self.output("[Turkmenportal] Парсинг ссылок успешно завершился!")
        
        # self.stop_thread_check("buttons")
        self.parse_cards(path, take_screenshots)

    def parse_cards(self, path, take_screenshots):
        with open(f"Parse_Files\\Links_Turkmenportal.txt", "r", encoding="utf8") as file:
                link_list = file.readline().split(",")[:-1]
                file.close()

        estate_list = []

        for count in range(len(link_list)):
            if self.stop_thread_check() == True:
                self.Save.to_xlsx(estate_list, "Turkmenportal", count)
                self.Save.links(link_list, "Turkmenportal")
                self.output("[Turkmenportal] Парсинг объявлений успешно остановился!")
                return 1
            
            if count % 1000 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, "Turkmenportal", count)
                self.Save.links(link_list, "Turkmenportal")


            link = link_list.pop(0)
            self.output(f"{count+1}. {link}")

            try:
                self.Find.get(link)
            except self.Find.WE:
                self.output("[Turkmenportal->Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
                pass

            card = [["Web ссылка", link]]

            card.append(["Наименование", self.Find.x("//h1[@class='blog_header']").text])
            card.append(["Дата публикации", self.Find.x("//time[@class='article_header_date']").text[5:]])

            title = self.Find.x("//p[@class='title']").text.split(" ")
            price, square = None, None
            for i in title:
                data = title[title.index(i)-1]
                if "м²" in i:
                    square = float(data.replace(",",""))
                    card.append(["Общая площадь", data.replace(",","")])
                if "ком." in i:
                    card.append(["Количество комнат", data])
                if "ман." in i:
                    data = data.replace(",","")
                    price = float(data)
                    card.append(["Цена предложения ТМТ", data[:data.find(".")]])

            if price != None and square != None:
                card.append(["Цена за 1 кв.метр", str(round(price/square, 2))])

            card.append(["Примечание", self.Find.x("//div[@class='description-content']/p").text])

            owner = [i.text for i in self.Find.xs("//div[@class='item-params c-1']/dl/dd")]
            for i in owner:
                if "+" in i or i.isdigit() == True:
                    card.append(["Конт.номер", i])

            filename = "Turkmenportal_" + link.split("/")[-1]
            card.append(["Ссылка на скриншоты", path + filename])

            if take_screenshots:
                self.Find.sshot(filename, 200)


            estate_list.append({key.strip(): value.strip() for key,value in card})


        self.Save.to_xlsx(estate_list, "Turkmenportal", count)
        self.Save.links(link_list)
        self.output("[Turkmenportal] Парсинг объявлений успешно завершился!")
        self.stop_thread_check("buttons")
        


if __name__ == "__main__":
    from Modules.Find import Find
    from Modules.Save import Save
    
    Turkmenportal = Turkmenportal(Find, Save)
    Turkmenportal.parse_links(0)

