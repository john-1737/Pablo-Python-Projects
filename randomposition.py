from tkinter import *
import random
import time
tk = Tk()
canvas = Canvas(tk, width=400, height=400)
canvas.pack()
while True:
    x = random.randrange(350)
    y = random.randrange(350)
    a = canvas.create_rectangle(x, y, x + 50, y + 50, state='normal', fill='black')
    tk.update()
    #time.sleep(0.1)