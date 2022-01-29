from tkinter import *
from kaspersmicrobit import KaspersMicrobit
import random
import time

BLUETOOTH_MICROBIT_OUD = '54:54:75:72:75:9E'
BLUETOOTH_MICROBIT_NIEUW = 'E3:7E:99:0D:C1:BA'

MICROBIT_BUTTON_A = 'e95dda90-251d-470a-a062-fa1922dfa9a8'
MICROBIT_BUTTON_B = 'e95dda91-251d-470a-a062-fa1922dfa9a8'

class Bal:
    def __init__(self, canvas, paddle, color):
        self.v = input('hoe snel wil je dat de bal gaat(pixsels per honderste seconden)')
        self.snelheid = int(self.v)
        self.snelheid_abs = abs(self.snelheid)
        self.n = self.snelheid_abs - self.snelheid_abs * 2
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = self.n
        self.punten = 0
        self.puntentelling = self.canvas.create_text(20, 20, text=self.punten, font=('helvetica', 20))
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return  True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = self.snelheid
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            paddle_snelheid = abs(paddle.x)
            self.y = paddle_snelheid - paddle_snelheid * 2
            self.punten = self.punten + 1
            self.canvas.itemconfig(self.puntentelling, text=self.punten, font=('helvetica', 20))
        if pos[0] <= 0:
            self.x = self.snelheid
        if pos[2] >= self.canvas_width:
            self.x = self.n

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.vertraag = True
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Key>', self.vertraagbal)
        self.canvas.bind_all('<<MICROBIT_BUTTON_A>>', self.turn_left)
        self.canvas.bind_all('<<MICROBIT_BUTTON_B>>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -4

    def turn_right(self, evt):
        self.x = 4

    def vertraagbal(self, evt):
        self.vertraag = False


tk = Tk()
tk.title("spel")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'blue')
bal = Bal(canvas, paddle, 'red')

def redraw():
    if paddle.vertraag:
        time.sleep(0.01)
    elif not bal.hit_bottom:
        paddle.draw()
        bal.draw()
    elif bal.hit_bottom:
        canvas.create_text(200, 200, text='Game over', font=('helvetica', 20))
    tk.after(10, redraw)


tk.after(10, redraw)

def knop_A(sender, data):
    tk.event_generate('<<MICROBIT_BUTTON_A>>', when='tail')
    paddle.vertraag = False



def knop_B(sender, data):
    tk.event_generate('<<MICROBIT_BUTTON_B>>', when='tail')
    paddle.vertraag = False


microbit1 = KaspersMicrobit(BLUETOOTH_MICROBIT_NIEUW)
microbit1.connect()
microbit1.notify(MICROBIT_BUTTON_A, knop_A)
microbit1.notify(MICROBIT_BUTTON_B, knop_B)


def sluit_tk_en_kuis_op():
    microbit1.disconnect()
    tk.destroy()


tk.protocol("WM_DELETE_WINDOW", sluit_tk_en_kuis_op)

tk.mainloop()
