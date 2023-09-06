
import datetime

class Naydizdes:

    def __init__(self, Find, Save, stop_thread_check, output=print):
        self.Find = Find()
        self.Save = Save
        self.output = output
        self.stop_thread_check = stop_thread_check

        self.output("[Naydizdes] Начинаю парсинг...")

        try:
            self.Find.get("https://www.naydizdes.com/nedvijimost/")
        except self.Find.WE:
            self.output("[Naydizdes->Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
            return 0

    @staticmethod
    def changekey(array, keys):
        for i in keys:
            try:
                if "Площадь" in i[1]:
                    array[i[0]] = array.pop(i[1])[:-2]
                elif "Цена" in i[1]:
                    array[i[0]] = array.pop(i[1]).replace(",","").strip()
                else:
                    array[i[0]] = array.pop(i[1])
            except KeyError:
                pass

        return array

    def date_check(self, date_to_check):

        if "часа назад" in date_to_check:
            hours = int(date_to_check[:date_to_check.index("часа")].strip())
            formatted_date = (datetime.datetime.today() - datetime.timedelta(hours=hours)).strftime('%d.%m.%Y')
            return formatted_date
        
        if "недель назад" in date_to_check:
            weeks = int(date_to_check[:date_to_check.index("недель")].strip())
            formatted_date = (datetime.datetime.today() - datetime.timedelta(weeks=weeks)).strftime('%d.%m.%Y')
            return formatted_date
        
        if "на прошлой неделе" in date_to_check:
            formatted_date = (datetime.datetime.today() - datetime.timedelta(weeks=1)).strftime('%d.%m.%Y')
            return formatted_date
        
        if "дней назад" in date_to_check:
            days = int(date_to_check[:date_to_check.index("дней назад")].strip())
            formatted_date = (datetime.datetime.today() - datetime.timedelta(days=days)).strftime('%d.%m.%Y')
            return formatted_date
        
        if "вчера" in date_to_check:
            formatted_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y')
            return formatted_date

        if "минут назад" in date_to_check:
            minutes = int(date_to_check[:date_to_check.index("минут назад")].strip())
            formatted_date = (datetime.datetime.today() - datetime.timedelta(minutes=minutes)).strftime('%d.%m.%Y')
            return formatted_date
        


    def parse_links(self, own_link, count_pages=0):
        link_list = []

        self.Find.get(own_link)

        if count_pages == 0:
            count_pages = int(self.Find.x("//div[@class='paginator']").text.split(" ")[-2])

        self.output(f"[Naydizdes] Количество страниц: {count_pages}")    

        for page in range(1, count_pages+1):
            if self.stop_thread_check() == True:
                self.Save.links(link_list, "Naydizdes")
                self.output("[Naydizdes] Парсинг ссылок успешно остановился!")
                return 1
            
            self.output(f"[Naydizdes] Страница: {page}")
            if page != 1:
                self.Find.get(own_link + f"{page}/")
            card_list = self.Find.xs("//a[@class='item_link clearfix']")

            for i in card_list:
                link_list.append(i.get_attribute('href'))

        self.Save.links(link_list, "Naydizdes")
        self.output("[Naydizdes] Парсинг ссылок успешно завершился!")
        self.stop_thread_check("buttons")

    def parse_cards(self, path, take_screenshots):
        with open(f"Parse_Files\\Links_Naydizdes.txt", "r", encoding="utf8") as file:
            link_list = file.readline().split(",")[:-1]
            file.close()

        estate_list = []

        for count in range(len(link_list)):
            if self.stop_thread_check() == True:
                self.Save.to_xlsx(estate_list, "Naydizdes", count)
                self.Save.links(link_list, "Naydizdes")
                self.output("[Naydizdes] Парсинг объявлений успешно остановился!")
                return 1
            
            if count % 1000 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, "Naydizdes", count)
                self.Save.links(link_list, "Naydizdes")


            link = link_list.pop(0)
            self.output(f"{count+1}. {link}")

            try:
                self.Find.get(link)
            except self.Find.WE:
                self.output("[Naydizdes->Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
                

            info_labels = [i.text[:i.text.find(":")] for i in self.Find.xs("//div[@class='post_custom_fields clearfix mxn1']/div/div/span[contains(@class, 'cf_label')]")]
            info_values = [i.text for i in self.Find.xs("//div[@class='post_custom_fields clearfix mxn1']/div/div/span[contains(@class, 'cf_value')]")]

            info = dict(zip(info_labels, info_values))
            info["Наименование"] = self.Find.x("//div[contains(@class, 'clearfix mt1')]/h1").text
            info["Примечание"] = self.Find.x("//p[@class='description']").text
            info["Web ссылка"] = link
            info['Дата публикации'] = self.date_check(info.pop('Опубликовано'))

            keys = [
                ['На каком этаже', 'Этаж'],
                ['Общая площадь', 'Площадь'],
                ['Цена предложения ТМТ', 'Цена'],
                ['Количество комнат', 'Комнаты'],
                ['Состояние ремонта', 'Состояние'],
                ['Адрес', 'Район'],
                ['Конт.номер', 'Телефон'],
                ['Цель', 'Тип объявления']
                ]
        
            info = self.changekey(info, keys)

            try:
                info['Цена за 1 кв.метр'] = str(round(float(info['Цена предложения ТМТ']) / float(info['Общая площадь']), 2))
            except KeyError:
                pass

            filename = "Naydizdes_" + link.split("-")[-1][:-5]
            info["Ссылка на скриншоты"] = path + filename

            if take_screenshots:
                self.Find.sshot(filename, 50)

            estate_list.append(info)

        self.Save.to_xlsx(estate_list, "Naydizdes", count)
        self.Save.links(link_list, "Naydizdes")
        self.output("[Naydizdes] Парсинг объявлений успешно завершился!")
        self.stop_thread_check("buttons")



if __name__ == "__main__":
    from Modules.Find import Find
    from Modules.Save import Save

    Naydizdes = Naydizdes(Find, Save)
    Naydizdes.parse_links(0)
    # Naydizdes.parse_cards()

