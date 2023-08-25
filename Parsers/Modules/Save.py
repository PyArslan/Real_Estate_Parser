import pandas as pd
import datetime

class Save:

    @staticmethod
    def to_xlsx(estate_list, site, count=0):

        data = {
            'Дата публикации': [i['Дата публикации'] if 'Дата публикации' in i else 'Не указано' for i in estate_list],            
            'Примечание': [i['Примечание'] if 'Примечание' in i else 'Не указано' for i in estate_list],
            'Цель': [i['Цель'] if 'Цель' in i else 'Не указано' for i in estate_list],
            'Тип недвижимости': [i['___'] if '___' in i else 'Не указано' for i in estate_list],
            'Наименование': [i['Наименование'] if 'Наименование' in i else 'Не указано' for i in estate_list],
            'Местоположение': [i['Местоположение'] if 'Местоположение' in i else 'Не указано' for i in estate_list],
            'Адрес': [i['Адрес'] if 'Адрес' in i else 'Не указано' for i in estate_list],
            'Материал изготовления': [i['Материал изготовления'] if 'Материал изготовления' in i else 'Не указано' for i in estate_list],
            'Год постр.': [i['Год постр.'] if 'Год постр.' in i else 'Не указано' for i in estate_list],
            'Кол-во комнат': [i['Количество комнат'] if 'Количество комнат' in i else 'Не указано' for i in estate_list],
            'Планировка': [i['Планировка'] if 'Планировка' in i else 'Не указано' for i in estate_list],
            'На каком этаже': [i['На каком этаже'] if 'На каком этаже' in i else 'Не указано' for i in estate_list],
            'Этажность дома': [i['Этажность дома'] if 'Этажность дома' in i else 'Не указано' for i in estate_list],
            'Общая площадь': [float(i['Общая площадь']) if 'Общая площадь' in i else 'Не указано' for i in estate_list],
            'Цена предложения ТМТ': [int(i['Цена предложения ТМТ']) if 'Цена предложения ТМТ' in i else 'Не указано' for i in estate_list],
            'Цена за 1 кв.метр': [float(i['Цена за 1 кв.метр']) if 'Цена за 1 кв метр' in i else 'Не указано' for i in estate_list],
            'Коммуникации': [i['Коммуникации'] if 'Коммуникации' in i else 'Не указано' for i in estate_list],
            'Санузел': [i['Санузел'] if 'Санузел' in i else 'Не указано' for i in estate_list],
            'Состояние ремонта': [i['Состояние ремонта'] if 'Состояние ремонта' in i else 'Не указано' for i in estate_list],
            'Web ссылка': [i['Web ссылка'] for i in estate_list],
            'Конт.номер': [i['Конт.номер'] if 'Конт.номер' in i else 'Не указано' for i in estate_list],
            'Статус': [i['Статус'] if 'Статус' in i else 'Не указано' for i in estate_list],
            'Ссылка на скриншоты': [i['Ссылка на скриншоты'] if 'Ссылка на скриншоты' in i else 'Не указано' for i in estate_list],
        }

        df = pd.DataFrame(data)
        df.index += 1

        today = datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        df.to_excel(f'Parse_Files\\{site}_{today}_{count}_.xlsx', index=False)

    @staticmethod
    def links(link_list, site):
        
        with open(f"Parse_Files\\Links_{site}.txt", "w", encoding="utf8") as file:
            for i in link_list:
                file.write(f"{i},")

            file.close()
