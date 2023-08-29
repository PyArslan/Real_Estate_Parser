from Modules.Find import Find
from Modules.Save import Save


class Jayym:

    def __init__(self, Find, Save):
        self.Find = Find()
        self.Save = Save
        self.Find.get("https://jayym.com/properties.html")
        
    def parse_links(self):
        card_list = self.Find.xs("//section[@id='listings']/a")

        link_list = []

        for i in card_list:
            link_list.append(i.get_attribute('href'))

        self.Save.links(link_list, "Jayym")

    def parse_cards(self):
        pass


if __name__ == "__main__":
    Jayym(Find, Save)