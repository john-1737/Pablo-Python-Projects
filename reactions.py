from tkinter import *
tk = Tk()
canvas = Canvas(tk, width=400, height=200)
canvas.pack()
red = canvas.create_polygon(10, 10, 10, 60, 50, 35, fill='red')
blue = canvas.create_polygon(10, 70, 10, 120, 50, 95, fill='blue')
canvas.create_text(130, 130, text='To move the red triangle, click the A key.', fill='red')
canvas.create_text(130, 150, text='To move the blue triangle, click the L key.', fill='blue')
def movered(event):
    canvas.move(red, 5, 0)
def moveblue(event):
    canvas.move(blue, 5, 0)
canvas.bind_all('<KeyPress-A>', movered)
canvas.bind_all('<KeyPress-L>', moveblue)
tk.mainloop()