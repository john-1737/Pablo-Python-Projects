from tkinter import *
import random
import time
tk = Tk()
canvas = Canvas(tk, width=400, height=400)
canvas.pack()
while True:
    polygon = canvas.create_polygon(random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),random.randrange(400),state='normal')
    tk.update()
    time.sleep(1)
    canvas.itemconfig(polygon, state='hidden')