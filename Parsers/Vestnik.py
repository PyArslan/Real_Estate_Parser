from Modules.Find import Find
from Modules.Save import Save

class Vestnik:

    def __init__(self, Find, Save):
        self.Find = Find()
        self.Save = Save
        try:
            self.Find.get("https://vestniktm.com/")
        except self.Find.WE:
            print("[Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
            return 0
        

    def parse_links(self, count_pages=0):
        link_list = []
        old_cards = ['Old_cards']

        for page in range(1, count_pages+1):
            sites = [f'https://vestniktm.com/c99-p{page}.html',
                    f'https://vestniktm.com/c235-p{page}.html',
                    f'https://vestniktm.com/c236-p{page}.html',
                    f'https://vestniktm.com/c237-p{page}.html',
                    f'https://vestniktm.com/c238-p{page}.html',
                    f'https://vestniktm.com/c239-p{page}.html',
                    f'https://vestniktm.com/c94-p{page}.html'
                    ]
            for site in sites:
                try:
                    self.Find.get(site)
                except self.Find.WE:
                    print("[Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
                    continue

                cards = self.Find.xs("//tbody/tr[@class='stradv ads']/td[2]/a")

                if cards == old_cards:
                    continue

                print(len(cards))
                for i in cards:
                    link_list.append(i.get_attribute("href"))

                old_cards = cards

        print(len(link_list))
        self.Save.links(link_list, "Vestnik")


    def parse_cards(self):
        with open(f"Parse_Files\\Links_Vestnik.txt", "r", encoding="utf8") as file:
                link_list = file.readline().split(",")[:-1]
                file.close()

        estate_list = []

        for count in range(len(link_list)):
            if count % 1000 == 0 and count != 0:
                self.Save.to_xlsx(estate_list, "Vestnik", count)
                self.Save.links(link_list, "Vestnik")


            link = link_list.pop(0)
            print(f"{count+1}. {link}")

            try:
                self.Find.get(link)
            except self.Find.WE:
                print("[Ошибка] Не удалось подключиться. Попробуёте зайти на сайт вручную, если получится то обратитесь к разработчику, если нет - проблема на самом сайте")
                pass

            

if __name__ == "__main__":
    Vestnik = Vestnik(Find, Save)
    Vestnik.parse_links(2)