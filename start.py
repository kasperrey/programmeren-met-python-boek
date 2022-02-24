import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
import paddlespel4module
import paddlespelbluetoothmodule
import time

class Begin:
    def __init__(self):
        self.start = False
        self.window = tk.Tk()
        self.window.title('spellen')
        self.window.geometry('500x250')
        ttk.Label(self.window, text = "kies een spel :",
                        font = ("Times New Roman", 10)).grid(column = 0,
                        row = 5, padx = 10, pady = 25)
        self.n = tk.StringVar()
        self.spelletjes = ttk.Combobox(self.window, width = 27, textvariable = self.n)
        self.spelletjes['values'] = ('paddlespel',
                                       'paddlespel_2_microbits_2_personen',
                                       'paddlespel-bluetooth'
                                       )
        b1 = Button(self.window, text = "start",command=self.knop)
        b1.place(relx = 1, x =-2, y = 2, anchor = 'ne')
        self.spelletjes.grid(column = 1, row = 5)
        self.spelletjes.current()
        while not self.start:
            self.window.update_idletasks()
            self.window.update()
            time.sleep(0.01)
        self.n = self.n.get()
        if self.n == 'paddlespel':
            self.window.destroy()
            v = paddlespel4module.spel()
            if v == True:
                d = Begin()
        elif self.n == 'paddlespel-bluetooth':
            self.window.destroy()
            v = paddlespelbluetoothmodule.spel()
            if v == True:
                d = Begin()
        elif self.n == 'paddlespel_2_microbits_2_personen':
            self.window.destroy()
            v = paddlespelbluetooth2_man_tegen_man.spel()
            if v == True:
                d = Begin()


    def knop(self):
        self.start = True

    def knop2(self):
        print('er')

d = Begin()
