from tkinter import Tk, Canvas, Toplevel, StringVar
from tkinter import Label as label
from tkinter.ttk import Entry, Frame, Button, Label
from random import randint, choice

def start_screensaver():
    global win, c, cw, ch
    win = Toplevel(root)
    win.geometry('1000x1000')
    win.bind_all('<Button-1>', lambda e: win.destroy())
    win.bind_all('<Button-2>', lambda e: win.destroy())
    win.bind_all('<Button-3>', lambda e: win.destroy())
    win.bind_all('<KeyPress>', lambda e: win.destroy())
    win.focus()
    cw = win.winfo_width()
    ch = win.winfo_height()
    c = Canvas(win, width=cw, height=ch)
    c.grid(sticky='nwes')
    win.after(randint(500, 2000), add_emoji)
    win.after(20, move_emoji)
    win.mainloop()

def add_emoji():
    c.create_text(randint(0, cw), ch+15, text=choice(emojis), font=('Helvetica', 30), tags='emoji')
    win.update()
    win.after(randint(500, 2000), add_emoji)

def move_emoji():
    c.move('emoji', 0, -15)
    win.update()
    win.after(20, move_emoji)

root = Tk()
root.title('Screensaver')
emojis = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
f = Frame(root)
f.grid(sticky='nwes')
Label(f, text='Select 5 emojis for screensaver:').grid(column=0, row=0, columnspan=5)
for i in range(5):
    Label(f, text=f'Emoji {i+1}:').grid(column=i, row=1)
    Entry(f, textvariable=emojis[i], font=('Helvetica', 30), width=2).grid(column=i, row=2)
bg = '#0000ff'
label(f, text='This is the background color', background=bg).grid(column=0, row=3, columnspan=3)
Button(f, text='Change').grid(column=3, row=3, columnspan=2)
Button(f, text='Start Screensaver', command=start_screensaver).grid(column=0, row=4, columnspan=5)
root.mainloop()