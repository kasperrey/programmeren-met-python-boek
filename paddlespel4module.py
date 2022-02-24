from tkinter import *
import random
import time

def spel():
    class Bal:
        def __init__(self, canvas, paddle, color):
            self.canvas = canvas
            self.paddle = paddle
            self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
            self.canvas.move(self.id, 245, 100)
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]
            self.y = -5
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
                self.y = 5
            if pos[3] >= self.canvas_height:
                self.hit_bottom = True
            if self.hit_paddle(pos) == True:
                paddle_snelheid = abs(paddle.x)
                self.y = paddle_snelheid - paddle_snelheid * 2
                self.punten = self.punten + 1
                self.canvas.itemconfig(self.puntentelling, text=self.punten, font=('helvetica', 20))
            if pos[0] <= 0:
                self.x = 5
            if pos[2] >= self.canvas_width:
                self.x = -5

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
            self.canvas.bind_all('<Button-1>', self.vertraagbal)

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

    while bal.hit_bottom == False:
        if paddle.vertraag == True:
            time.sleep(0.01)
        elif bal.hit_bottom == False:
            paddle.draw()
            bal.draw()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
        
    canvas.create_text(200, 200, text='Game over', font=('helvetica', 20))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
    tk.destroy()
    return True
