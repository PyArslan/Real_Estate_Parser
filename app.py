import tkinter as Tk
from tkinter.scrolledtext import ScrolledText

from Parsers.Tmcars import Tmcars
from Parsers.Turkmenportal import Turkmenportal
from Parsers.Naydizdes import Naydizdes
from Parsers.Jayym import Jayym   

from Parsers.Modules.Find import Find
from Parsers.Modules.Save import Save

import os
from time import sleep
from threading import Thread


class Controller(object):
    
    def __init__(self):
        self.stop_threads = False
        self.thread_check = None
        self.selected_site = False
        
        self.thread_Tmcars = None
        self.thread_Turkmenportal = None
        self.thread_Jayym = None
        self.thread_Naydizdes = None

    def select_site(self, site):
        self.selected_site = site

        if site == "Tmcars":
            txt_link['menu'].delete(0, 'end')
            links_array = [
                           "https://tmcars.info/others/nedvijimost", 
                            "https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov",
                            "https://tmcars.info/others/nedvijimost/arenda-komnaty-kvartiry-i-doma",
                            "https://tmcars.info/others/nedvijimost/arenda-ofisa",
                            "https://tmcars.info/others/nedvijimost/spros-na-arendu-komnaty-kvartiry.."
                            ]
            
            for i in links_array:
                txt_link["menu"].add_command(label=i, command=Tk._setit(link_variables, i))
            link_variables.set("https://tmcars.info/others/nedvijimost")
                            
                                    
        elif site == "Jayym":
            txt_link['menu'].delete(0, 'end')
            links_array = [
                            'https://jayym.com/properties.html',
                            'https://jayym.com/properties/sell/',
                            'https://jayym.com/properties/rent/',
                            'https://jayym.com/properties/sell/house/',
                            'https://jayym.com/properties/sell/dupleks/',
                            'https://jayym.com/properties/sell/apartment/',
                            'https://jayym.com/properties/sell/commercial-property/',
                            'https://jayym.com/properties/sell/land/',
                            'https://jayym.com/properties/sell/elite-housing/'
                            ]
            
            for i in links_array:
                txt_link["menu"].add_command(label=i, command=Tk._setit(link_variables, i))
            link_variables.set("https://jayym.com/properties.html")

        elif site == "Naydizdes":
            txt_link['menu'].delete(0, 'end')
            links_array = [
                            "https://www.naydizdes.com/nedvijimost/",
                            'https://www.naydizdes.com/prodaja-kvartir/',
                            'https://www.naydizdes.com/arenda-kvartir/',
                            'https://www.naydizdes.com/prodaja-ofisov-magazinov/',
                            'https://www.naydizdes.com/arenda-ofisov-magazinov/',
                            'https://www.naydizdes.com/arenda-komnati/',
                            'https://www.naydizdes.com/prodaja-zemli/',
                            'https://www.naydizdes.com/ashgabat/nedvijimost/',
                            'https://www.naydizdes.com/ashgabat/nedvijimost/',
                            'https://www.naydizdes.com/dasoguz-welayaty/nedvijimost/',
                            'https://www.naydizdes.com/ahal/nedvijimost/',
                            'https://www.naydizdes.com/lebap/nedvijimost/',
                            'https://www.naydizdes.com/balkan/nedvijimost/',
                            'https://www.naydizdes.com/mary-welayaty/nedvijimost/'
                            ]
            
            for i in links_array:
                txt_link["menu"].add_command(label=i, command=Tk._setit(link_variables, i))
            link_variables.set("https://www.naydizdes.com/nedvijimost/")
        else:
            txt_link['menu'].delete(0, 'end')
            links_array = [
                           "https://turkmenportal.com/estates",
                            ]
            
            for i in links_array:
                txt_link["menu"].add_command(label=i, command=Tk._setit(link_variables, i))
            link_variables.set("https://turkmenportal.com/estates")

    def stop_thread_check(self, check="thread"):
        """ Эту функцию отправляем в файлы парсеры для 
            проверки переменной из этого файла """
        if check == "thread":
            if self.stop_threads == True:
                return True
            else:
                return False
        elif check == "buttons": 
            button_start["state"] = "normal"
            button_continue["state"] = "normal"

        

    def start(self, count_pages, link, own_link, path, take_photos):
        button_start["state"] = "disabled"
        button_continue["state"] = "disabled"

        try:
            count_pages = int(count_pages)
        except ValueError:
            self.output("[Ошибка] Некорректное значение страниц!")
            button_start["state"] = "normal"
            button_continue["state"] = "normal"
            return 0

        if own_link:
            link = own_link


        self.stop_threads = False

        if not self.selected_site:
            self.output("[Ошибка] Выберите сайт!")
            button_start["state"] = "normal"
            button_continue["state"] = "normal"
            return 0
        
        if self.selected_site == "Tmcars":
            self.thread = Thread(target = lambda: Tmcars(Find, Save, self.stop_thread_check, self.output).parse_links(link, count_pages, path, take_photos))
        elif self.selected_site == "Turkmenportal":
            self.thread = Thread(target = lambda: Turkmenportal(Find, Save, self.stop_thread_check, self.output).parse_links(link, count_pages, path, take_photos))
        elif self.selected_site == "Jayym":
            self.thread = Thread(target = lambda: Jayym(Find, Save, self.stop_thread_check, self.output).parse_links(link, count_pages, path, take_photos))
        elif self.selected_site == "Naydizdes":
            self.thread = Thread(target = lambda: Naydizdes(Find, Save, self.stop_thread_check, self.output).parse_links(link, count_pages, path, take_photos))

        self.thread.start()

        if shutdown.get() == 1:
            self.thread_check = Thread(target = lambda: self.check_thread_alive(shutdown=True, time_sleep=10))
            self.thread_check.start()


    def continue_parsing(self, path, take_photos):
        button_start["state"] = "disabled"
        button_continue["state"] = "disabled"

        self.stop_threads = False

        if not self.selected_site:
            self.output("[Ошибка] Выберите сайт!")
            button_start["state"] = "normal"
            button_continue["state"] = "normal"
            return 0
        
        if not path:
            self.output("[Ошибка] Укажить путь до скриншотов!")
            button_start["state"] = "normal"
            button_continue["state"] = "normal"
            return 0
        
        if path[-1] != "\\":
            path = path + "\\"

        if self.selected_site == "Tmcars":
            self.thread = Thread(target = lambda: Tmcars(Find, Save, self.stop_thread_check, self.output).parse_cards(path, take_photos))
        elif self.selected_site == "Turkmenportal":
            self.thread = Thread(target = lambda: Turkmenportal(Find, Save, self.stop_thread_check, self.output).parse_cards(path, take_photos))
        elif self.selected_site == "Jayym":
            self.thread = Thread(target = lambda: Jayym(Find, Save, self.stop_thread_check, self.output).parse_cards(path, take_photos))
        elif self.selected_site == "Naydizdes":
            self.thread = Thread(target = lambda: Naydizdes(Find, Save, self.stop_thread_check, self.output).parse_cards(path, take_photos))

        self.thread.start()

        if shutdown.get() == 1:
            self.thread_check = Thread(target = lambda: self.check_thread_alive(shutdown=True, time_sleep=10))
            self.thread_check.start()


    def check_thread_alive(self, shutdown=False, time_sleep=3):
        while True:
            if self.thread.is_alive():
                sleep(time_sleep)
            else:
                button_start["state"] = "normal"
                button_continue["state"] = "normal"
                button_finish["state"] = "normal"
                if shutdown:
                    os.system("shutdown /s /t 120")
                break

    def finish(self): 
        button_finish["state"] = "disabled"
        self.stop_threads = True

        self.thread_Tmcars = None
        self.thread_Turkmenportal = None
        self.thread_Jayym = None
        self.thread_Naydizdes = None
        self.thread_check = None

        self.selected_site = False

        self.thread_check = Thread(target = lambda: self.check_thread_alive())
        self.thread_check.start()

        

    def output(self, text):
        console_output.insert(Tk.END, f"{text}\n")
        console_output.see("end")

if __name__ == "__main__":

    if not os.path.exists("Parse_Files"):
        os.makedirs("Parse_Files")

    control = Controller()

    root = Tk.Tk()
    root.title('Real Estate Parser')
    root.wm_iconbitmap('house.ico')
    root.configure(background='#ececec')

    width, height = 1360//3, 768//7
    root.geometry(f'550x510+{width}+{height}')

# ============================Variables 1============================ #

    label_count = Tk.Label(root, text='Количество страниц: ')
    label_count.place(x=10, y=3) 

    txt_count = Tk.Entry(root, width=10)  
    txt_count.place(x=140, y=5) 
    txt_count.configure(background='#ffffff', borderwidth=2, relief="groove")


    link_variables = Tk.StringVar(root)
    link_variables.set("") # default value

    links_array = [""]
    txt_link = Tk.OptionMenu(root, link_variables, *links_array)
    
    txt_link.place(x=320, y=5) 
    txt_link.configure(background='#ffffff', borderwidth=2, relief="groove", width=30)

    label_own_link = Tk.Label(root, text='Своя ссылка: ')
    label_own_link.place(x=240, y=40) 

    own_link = Tk.Entry(root, width=36) 
    own_link.place(x=320, y=40)  
    own_link.configure(background='#ffffff', borderwidth=2, relief="groove")

# ============================Site Select============================ #

    site = Tk.StringVar(value="None")

    button_Tmcars = Tk.Radiobutton(root, text='Tmcars', value='Tmcars', variable=site, width=15, command=lambda: control.select_site("Tmcars"))
    button_Tmcars.place(x=10, y=70) 

    button_Naydizdes = Tk.Radiobutton(root, text='Naydizdes', value='Naydizdes', variable=site, width=15, command=lambda: control.select_site("Naydizdes"))
    button_Naydizdes.place(x=140, y=70) 

    button_Jayym = Tk.Radiobutton(root, text='Jayym', value='Jayym', variable=site, width=15, command=lambda: control.select_site("Jayym"))
    button_Jayym.place(x=285, y=70) 

    button_Turkmenportal = Tk.Radiobutton(root, text='Turkmenportal', value='Turkmenportal', variable=site, width=15, command=lambda: control.select_site("Turkmenportal"))
    button_Turkmenportal.place(x=400, y=70) 

# ============================Options Select============================ #

    button_start = Tk.Button(root, text='Начать', width=17, command = lambda: control.start(txt_count.get(), link_variables.get(), own_link.get(), txt_file_path.get(), take_photos.get()))
    button_start.place(x=10, y=110) 

    button_continue = Tk.Button(root, text='Продолжить', width=17, command=lambda: control.continue_parsing(txt_file_path.get(), take_photos.get()))
    button_continue.place(x=210, y=110) 

    button_finish = Tk.Button(root, text='Приостановить', width=17, command=control.finish)
    button_finish.place(x=410, y=110)

# ============================Variables 2============================ #

    shutdown = Tk.IntVar(value=0)

    CheckShutdown = Tk.Checkbutton(root, text='Выключение ПК',variable=shutdown, onvalue=1, offvalue=0)
    CheckShutdown.place(x=10, y=145)

    take_photos = Tk.IntVar(value=1)

    CheckPhotos = Tk.Checkbutton(root, text='Фото',variable=take_photos, onvalue=1, offvalue=0)
    CheckPhotos.place(x=145, y=145)


    label_file_path = Tk.Label(root, text='Путь к Фото: ')
    label_file_path.place(x=220, y=148) 

    txt_file_path = Tk.Entry(root, width=36)  
    txt_file_path.insert(Tk.END, "D:\\ScreenshotsEstate\\")
    txt_file_path.place(x=300, y=148) 
    txt_file_path.configure(background='#ffffff', borderwidth=2, relief="groove")

# ============================Console============================ #

    console_output = ScrolledText(root, width=64, height=20, font="Fixedsys 12", wrap="word", bg="black", fg="white", bd=4)
    console_output.place(x=7, y=175)

    console_output.insert(Tk.END, f"Добро Пожаловать!\n\n{'Информация':-^63}\n")
    console_output.insert(Tk.END, f"1. Выберите сайт, введите количество страниц и запустите процесс\n")
    console_output.insert(Tk.END, f"2. 1 страница равна: \n\t100 ссылок Tmcars\n\t100 ссылок Naydizdes\n\t32 ссылки Jayym\n\t20 ссылок Turkmenportal\n")
    console_output.insert(Tk.END, f"3. Чтобы спарсить все объявления введите 0\n")
    console_output.insert(Tk.END, f"4. Если бразуер встал - обновите страницу\n")
    console_output.insert(Tk.END, f"5. Если браузер закрылся, а процесс не завершился - Ошибка, обратитесь к разработчику\n")
    console_output.insert(Tk.END, f"{'':-^64}\n\n")

    root.mainloop()