from tkinter import *
import random
import time
displaytext = False
score = 0

class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(starts)
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x = self.x * -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
    
        if pos[1] <= 0 or pos[3] >= self.canvas_height:
            self.y = self.y * -1

tk = Tk()
tk.title('Bounce Game')
tk.resizable(0, 0) 
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

ball = Ball(canvas, 'black')

while True:
    ball.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)