import tkinter as Tk
from tkinter.scrolledtext import ScrolledText

from Parser import Tmcars, Find
import os
from threading import Thread,Event

class Controller(object):
    
    def __init__(self):
        self.thread1 = None
        self.stop_threads = Event()

    def start(self):
        self.stop_threads.clear()
        self.thread1 = Thread(target = lambda: Tmcars(Find).parse_links())
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

    button_start = Tk.Button(root, text='Начать', width=15, command=control.start)
    button_start.place(x=10, y=10) 


    root.mainloop()