from Modules.Find import Find
from Modules.Save import Save


class Turkmenportal:

    def __init__(self, Find, Save):
        self.Find = Find()
        self.Save = Save
        self.Find.get("https://turkmenportal.com/estates/nedvizhimost")

    def parse_links(self):
        """ TODO: for i in count_pages """
        card_list = self.Find.xs("//div[@class='entry-title']/a")

        link_list = []

        for card in card_list:
            link_list.append(card.get_attribute('href'))

        self.Save.links(link_list, "Turkmenportal")

    def parse_cards(self):
        with open(f"Parse_Files\\Links_Turkmenportal.txt", "r", encoding="utf8") as file:
                link_list = file.readline().split(",")[:-1]
                file.close()

        estate_list = []

        for count in range(len(link_list)):
            if count % 10 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, "Turkmenportal", count)
                self.Save.links(link_list, "Turkmenportal")


            link = link_list.pop(0)
            print(f"{count+1}. {link}")

            try:
                self.Find.get(link)
            except self.Find.WE:
                print("[Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
                pass

            card = [["Web ссылка", link]]

            card.append(["Наименование", self.Find.x("//h1[@class='blog_header']").text])
            card.append(["Дата публикации", self.Find.x("//time[@class='article_header_date']").text[5:]])

            title = self.Find.x("//p[@class='title']").text.split(" ")
            price, square = None, None
            for i in title:
                data = title[title.index(i)-1]
                if "м²" in i:
                    square = float(data)
                    card.append(["Общая площадь", data])
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


            print("\n\n-----------\n",card,end="\n-----------\n\n")
            estate_list.append({key.strip(): value.strip() for key,value in card})


        self.Save.to_xlsx(estate_list, "Turkmenportal", count)
        self.Save.links(link_list)


if __name__ == "__main__":
    Turkmenportal = Turkmenportal(Find, Save)
    Turkmenportal.parse_cards()

