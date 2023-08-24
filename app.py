import tkinter as Tk
from tkinter.scrolledtext import ScrolledText

from Parsers.Tmcars import Tmcars
from Parsers.Modules.Find import Find
from Parsers.Modules.Save import Save

import os
from threading import Thread,Event

class Controller(object):
    
    def __init__(self):
        self.thread1 = None
        self.stop_threads = Event()

    def start(self):
        self.stop_threads.clear()
        self.thread1 = Thread(target = lambda: Tmcars(Find, Save).parse_links())
        self.thread1.start()

    def finish(self):
        self.stop_threads.set()
        self.thread1 = None


if __name__ == "__main__":

    if not os.path.exists("Parse_Files"):
        os.makedirs("Parse_Files")

    control = Controller()

    root = Tk.Tk()
    root.title('Real Estate Parser')
    root.configure(background='#ececec')

    width, height = 1360//3, 768//5
    root.geometry(f'550x475+{width}+{height}')

    # label_count = Tk.Label(root, text='Количество страниц: ')
    # label_count.place(x=10, y=3) 

    # txt_count = Tk.Entry(root, width=10)  
    # txt_count.place(x=140, y=5) 
    # txt_count.configure(background='#ffffff', borderwidth=2, relief="groove")


    # variables = Tk.StringVar(root)
    # variables.set("https://tmcars.info/others/nedvijimost") # default value

    # txt_link = Tk.OptionMenu(root, variables, 
    #                         "https://tmcars.info/others/nedvijimost", 
    #                         "https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov",
    #                         "https://tmcars.info/others/nedvijimost/arenda-komnaty-kvartiry-i-doma",
    #                         "https://tmcars.info/others/nedvijimost/arenda-ofisa",
    #                         "https://tmcars.info/others/nedvijimost/spros-na-arendu-komnaty-kvartiry.."
    #                          )
    
    # txt_link.place(x=320, y=5) 
    # txt_link.configure(background='#ffffff', borderwidth=2, relief="groove", width=30)

    # label_args_entry = Tk.Label(root, text='Своя ссылка: ')
    # label_args_entry.place(x=240, y=40) 

    # args_entry = Tk.Entry(root, width=36) 
    # args_entry.place(x=320, y=40)  
    # args_entry.configure(background='#ffffff', borderwidth=2, relief="groove")


    button_start = Tk.Button(root, text='Начать', width=15, command=control.start())
    button_start.place(x=10, y=70) 

    # button_continue = Tk.Button(root, text='Продолжить', width=15)
    # button_continue.place(x=220, y=70) 

    # button_finish = Tk.Button(root, text='Приостановить', width=15)
    # button_finish.place(x=420, y=70)


    # take_screenshots = Tk.IntVar(value=1)

    # CheckScreenshots = Tk.Checkbutton(root, text='Скриншоты',variable=take_screenshots, onvalue=1, offvalue=0)
    # CheckScreenshots.place(x=10, y=110)


    # label_file_path = Tk.Label(root, text='Путь к скриншотам: ')
    # label_file_path.place(x=175, y=110) 

    # txt_file_path = Tk.Entry(root, width=36)  
    # txt_file_path.insert(Tk.END, "D:\\Screenshotsteh\\")
    # txt_file_path.place(x=300, y=110) 
    # txt_file_path.configure(background='#ffffff', borderwidth=2, relief="groove")


    console_output = ScrolledText(root, width=64, height=20, font="Fixedsys 12", wrap="word", bg="black", fg="white", bd=4)
    console_output.place(x=7, y=140)

    console_output.insert(Tk.END, f"Добро Пожаловать!\n\n{'Информация':-^63}\n")
    console_output.insert(Tk.END, f"1. Введите количество страниц и запустите процесс\n")
    console_output.insert(Tk.END, f"2. 1 страница = 100 ссылок\n")
    console_output.insert(Tk.END, f"3. Чтобы спарсить все объявления введите 0\n")
    console_output.insert(Tk.END, f"4. Если бразуер встал - обновите страницу\n")
    console_output.insert(Tk.END, f"5. Окно браузера нельзя уменьшать меньше чем его значение при открытии\n")
    console_output.insert(Tk.END, f"{'':-^64}\n\n")

    root.mainloop()