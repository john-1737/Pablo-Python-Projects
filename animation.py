import time
from tkinter import *
tk = Tk()
canvas = Canvas(tk, width=400, height=200)
canvas.pack()
canvas.create_polygon(10, 10, 10, 60, 50, 35)
canvas.create_polygon(10, 70, 10, 120, 50, 95)
for x in range(1, 61):
    canvas.move(1, 5, 0)
    canvas.move(2, 8, 0)
    tk.update()
    time.sleep(0.05)
tk.mainloop()
