from tkinter import *
from kaspersmicrobit import KaspersMicrobit
import random
import time

BLUETOOTH_MICROBIT_OUD = '54:54:75:72:75:9E'
BLUETOOTH_MICROBIT_NIEUW = 'E3:7E:99:0D:C1:BA'

MICROBIT_BUTTON_A = 'e95dda90-251d-470a-a062-fa1922dfa9a8'
MICROBIT_BUTTON_B = 'e95dda91-251d-470a-a062-fa1922dfa9a8'

class Bal:
    def __init__(self, canvas, paddle, paddle2, color):
        self.canvas = canvas
        self.paddle = paddle
        self.paddle2 = paddle2
        self.id = canvas.create_oval(10, 10, 26, 26, fill=color)
        self.canvas.move(self.id, 232, 232)
        starts = [-2, -1, 1, 2]
        # -3, , 3
        random.shuffle(starts)
        self.x = starts[0]
        self.y = starts[3]
        self.punten_blue = 0
        self.punten_red = 0
        self.puntentelling = self.canvas.create_text(20, 20, text=self.punten_blue, font=('helvetica', 20))
        self.puntentelling2 = self.canvas.create_text(480, 480, text=self.punten_red, font=('helvetica', 20))
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.y += self.y
        self.hit_bottom = False

    def hit_paddle(self, pos, paddle):
        paddle_pos = self.canvas.coords(paddle.id)
        if (pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]):
            if (pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]) \
               or (pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]):
                return  True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = -self.y
            self.punten_red += 1
            self.canvas.itemconfig(self.puntentelling2, text=self.punten_red, font=('helvetica', 20))
        if pos[3] >= self.canvas_height:
            self.punten_blue += 1
            self.canvas.itemconfig(self.puntentelling, text=self.punten_blue, font=('helvetica', 20))
            self.y = -self.y
        if (self.hit_paddle(pos, self.paddle) == True) \
           or (self.hit_paddle(pos, self.paddle2) == True):
            self.y = -self.y
        if pos[0] <= 0:
            self.x = -self.x
        if pos[2] >= self.canvas_width:
            self.x = -self.x

class Paddle:
    def __init__(self, canvas, color, snelheid, min_snelheid):
        self.canvas = canvas
        self.snelheid = snelheid
        self.min_snelheid = min_snelheid
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.x = 0
        self.vertraag = True
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = self.min_snelheid

    def turn_right(self, evt):
        self.x = self.snelheid

    def vertraagbal(self, evt):
        self.vertraag = False


tk = Tk()
tk.title("spel")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
paddletest = 0
paddle = Paddle(canvas, 'blue', 2, -2)
canvas.move(paddle.id, 200, 450)
paddle2 = Paddle(canvas, 'red', 4, -4)
canvas.move(paddle2.id, 200, 50)
bal = Bal(canvas, paddle, paddle2, 'red')

def sluit_tk_en_kuis_op():
    microbit1.disconnect()
    tk.destroy()
    """    microbit2.disconnect()"""


tk.protocol("WM_DELETE_WINDOW", sluit_tk_en_kuis_op)
canvas.bind_all('<KeyPress-Left>', paddle.turn_left)
canvas.bind_all('<KeyPress-Right>', paddle.turn_right)
canvas.bind_all('<Key>', paddle.vertraagbal)


def knop_A_nieuw(sender, data):
    paddle.turn_left(None)
    paddle.vertraag = False

def knop_B_nieuw(sender, data):
    paddle.turn_right(None)
    paddle.vertraag = False


def knop_B_oud(s):
    paddle2.turn_right(None)
    paddle2.vertraag = False
    

def knop_A_oud(s):
    paddle2.turn_left(None)
    paddle2.vertraag = False


microbit1 = KaspersMicrobit(BLUETOOTH_MICROBIT_NIEUW)
microbit1.connect()
microbit1.notify(MICROBIT_BUTTON_A, knop_A_nieuw)
microbit1.notify(MICROBIT_BUTTON_B, knop_B_nieuw)
canvas.bind_all('<KeyPress-Left>', knop_A_oud)
canvas.bind_all('<KeyPress-Right>', knop_B_oud)
"""
microbit2 = KaspersMicrobit(BLUETOOTH_MICROBIT_OUD)
microbit2.connect()
microbit2.notify(MICROBIT_BUTTON_A, knop_A_oud)
microbit2.notify(MICROBIT_BUTTON_B, knop_B_oud)
"""

while not bal.hit_bottom:
    if paddle.vertraag == True and paddle2.vertraag == True:
        time.sleep(0.01)
    else:
        paddle.draw()
        paddle.draw()
        paddle2.draw()
        bal.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

canvas.create_text(200, 200, text='Game over', font=('helvetica', 20))
tk.update_idletasks()
tk.update()

microbit1.disconnect()
