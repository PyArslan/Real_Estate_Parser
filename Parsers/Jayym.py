

class Jayym:

    def __init__(self, Find, Save, stop_thread_check, output=print):
        self.Find = Find()
        self.Save = Save
        self.output = output
        self.stop_thread_check = stop_thread_check

        self.output("[Jayym] Начинаю парсинг...")

        try:
            self.Find.get("https://jayym.com/properties.html")
        except self.Find.WE:
            self.output("[Jayym->Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
            return 0

    @staticmethod
    def changekey(array, keys):
        for i in keys:
            try:
                if "Площадь" in i[1]:
                    array[i[0]] = array.pop(i[1])[:-2].strip()
                else:
                    array[i[0]] = array.pop(i[1])
            except KeyError:
                pass

        return array

    def parse_links(self, own_link, count_pages=0, path="D:\\ScreenshotsEstate\\", take_screenshots=1):

        link_list = []

        if own_link[-1] != "/":
            own_link = own_link[:own_link.find(".html")] + "/"

        self.Find.get(own_link)
 
        if count_pages == 0:
            count_pages = self.Find.x("//li[@class='transit']").text
            count_pages = int(count_pages[count_pages.rfind(" "):])
        
        self.output(f"[Jayym] Количество страниц: {count_pages}")


        for page in range(1, count_pages+1):
            if self.stop_thread_check() == True:
                self.Save.links(link_list, "Jayym")
                self.output("[Jayym] Парсинг ссылок успешно остановился!")
                return 1
            
            self.output(f"[Jayym] Страница: {page}")
            if page != 1:
                self.Find.get(own_link + f"index{page}.html")
                
            card_list = self.Find.xs("//section[@id='listings']/article/div[2]/a")

            for i in card_list:
                link_list.append(i.get_attribute('href'))

        self.Save.links(link_list, "Jayym")
        self.output("[Jayym] Парсинг ссылок успешно завершился!")

        # self.stop_thread_check("buttons")
        self.parse_cards(path, take_screenshots)

    def parse_cards(self, path, take_screenshots):
        with open(f"Parse_Files\\Links_Jayym.txt", "r", encoding="utf8") as file:
            link_list = file.readline().split(",")[:-1]
            file.close()

        estate_list = []

        for count in range(len(link_list)):
            if self.stop_thread_check() == True:
                self.Save.to_xlsx(estate_list, "Jayym", count)
                self.Save.links(link_list, "Jayym")
                self.output("[Jayym] Парсинг объявлений успешно остановился!")
                return 1
            
            if count % 1000 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, "Jayym", count)
                self.Save.links(link_list, "Jayym")


            link = link_list.pop(0)
            self.output(f"{count+1}. {link}")

            try:
                self.Find.get(link)
            except self.Find.WE:
                self.output("[Jayym->Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")

            keys = [i.text for i in self.Find.xs("//div[@class='listing-fields']//span") if i.text != ""]
            values = [i.text for i in self.Find.xs("//div[@class='listing-fields']//div[@class='value']")]
            info = dict(zip(keys,values))

            info['Наименование'] = self.Find.x("//div[@class='row listing-header']/h1").text

            try:
                phone = self.Find.x("//div[@id='df_field_phone']/div[2]/a").text
            except self.Find.NSEE:
                phone = ""
            info['Конт.номер'] = "+" + ''.join([i for i in phone if i.isdigit()])
            
            price = self.Find.x("//*[@id='df_field_price']/span").text
            info['Цена предложения ТМТ'] = ''.join([i for i in price if i.isdigit()])

            info['Web ссылка'] = link

            keys = [
                ['Этажность дома', 'Этажность здания'],
                ['Дата публикации', 'Добавлено'],
                ['На каком этаже', 'Этаж'],
                ['Общая площадь', 'Площадь'],
                ['Цена предложения ТМТ', 'Цена'],
                ['Количество комнат', 'Комнаты'],
                ['Состояние ремонта', 'Ремонт'],
                ['Местоположение', 'Город'],
                ['Адрес', 'Район'],
                ['Цель', 'Недвижимость.'],
                ['Примечание', 'Описание']
            ]

            info = self.changekey(info, keys)

            try:
                info['Цена за 1 кв.метр'] = str(round(float(info['Цена предложения ТМТ']) / float(info['Общая площадь']), 2))
            except KeyError:
                pass
        
            filename = "Jayym_" + link.split("-")[-1][:-5]
            info["Ссылка на скриншоты"] = path + filename

            if take_screenshots:
                self.Find.sshot(filename, 200)

            estate_list.append(info)

        self.Save.to_xlsx(estate_list, "Jayym", count)
        self.Save.links(link_list)
        self.output("[Jayym] Парсинг объявлений успешно завершился!")
        self.stop_thread_check("buttons")

if __name__ == "__main__":
    from Modules.Find import Find
    from Modules.Save import Save

    Jayym(Find, Save).parse_links(0)