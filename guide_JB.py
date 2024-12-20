from tkinter import *
import time
import random
t = 0

ls = ["1) This is the FIRST long sentence "
      +"that is still going on the second line." ,
      "2) This is the SECOND long sentence "
      +"that is also still going on a second line",
     "3) This is the THIRD long sentence "
      +"that is also still going on a second line"]

tk = Tk()
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()

textbox = canvas.create_text(200, 200, text = ls[t], width = 250, fill = 'red')

def increment_up(event):
    global t
    t += 1
    canvas.itemconfig(textbox, text = ls[t%len(ls)])

def increment_down(event):
    global t
    t -= 1
    canvas.itemconfig(textbox, text = ls[t%len(ls)])

canvas.bind_all('<KeyPress-Right>', increment_up)
canvas.bind_all('<KeyPress-Left>', increment_down)

tk.mainloop()