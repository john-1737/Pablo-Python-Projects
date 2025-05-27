import tkinter as tk
import time as t
from tkinter import ttk, messagebox

def subtract(top_num, bot_num):
    if top_num > 9999 or bot_num > 9999:
        messagebox.showinfo(message='One or both of the numbers is too big (greater than 9,999).')
        return
    if top_num < 0 or bot_num < 0:
        messagebox.showinfo(message='One or both of the numbers is negative.')
        return
    bot_list, top_list = list(str(bot_num).zfill(4))[::-1], list(str(top_num).zfill(4))[::-1]
    for i in range(4):
        top_list[i] = int(top_list[i])
        bot_list[i] = int(bot_list[i])        
        top_places[i].set(top_list[i])
        bot_places[i].set(bot_list[i])
    if bot_num > top_num:
        bot_list, top_list = top_list, bot_list
        negative_var.set('-')
    for i in range(4):
        place = top_list[i] - bot_list[i]
        if place < 0:
            j = 1
            while top_list[i+j] == 0:
                top_list[i+j] = 7 + base8.get()
                j+=1
            top_list[i+j] -= 1
            top_list[i] += 8 + base8.get()
            place = top_list[i]- bot_list[i]
        if borrow.get():
            for i in range(4):
                top_places[i].set(top_list[i])
                bot_places[i].set(bot_list[i])
        answer_places[i].set(place)

def clear():
    top_var.set(0)
    bot_var.set(0)
    base8.set(2)
    for i in top_places + bot_places + answer_places:
        i.set(0)
    negative_var.set('')    
          
root = tk.Tk()
top_var = tk.IntVar()
bot_var = tk.IntVar()
base8 = tk.IntVar()
base8.set(2)
tk.Checkbutton(root, text='Base 8', variable=base8, onvalue=0, offvalue=2).grid(column=4, row=3, columnspan=4)
top_places = [tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()]
bot_places = [tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()]
answer_places = [tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()]
tk.Label(root, text='Enter numbers in the entry boxes to subtract.').grid(column=0, row=0, columnspan=8)
tk.Entry(root, textvariable=top_var).grid(column=0, row=1, columnspan=8)
tk.Entry(root, textvariable=bot_var).grid(column=0, row=2, columnspan=8)
#tk.Button(root, text='Solve', command=lambda top_num=top_var.get(), bot_num=bot_var.get() : subtract(top_num, bot_num)).grid(column=0, row=3, columnspan=8)
tk.Button(root, text='Solve', command=lambda: subtract(top_var.get(), bot_var.get())).grid(column=0, row=3, columnspan=4)
for i in (8, 6, 4, 2):
    tk.Label(root, text={8:'Ones', 6:'Tens', 4:'Hundreds', 2:'Thousands'}[i]).grid(column=i, row=4)
    poss = {8:0, 6:1, 4:2, 2:3}
    tk.Label(root, textvariable=top_places[poss[i]]).grid(column=i, row=5)
    tk.Label(root, textvariable=bot_places[poss[i]]).grid(column=i, row=6)
    tk.Label(root, textvariable=answer_places[poss[i]]).grid(column=i, row=7)

root.option_add('*tearoff', tk.FALSE)
win = tk.Toplevel(root)
menubar = tk.Menu(win)
win['menu'] = menubar
win.withdraw()
settings = tk.Menu(menubar)
menubar.add_cascade(menu=settings, label='Settings')
borrow = tk.BooleanVar()
settings.add_checkbutton(label='Show Borrowing', variable=borrow, onvalue=True, offvalue=False)
settings.add_command(label='Clear Screen', command=clear)
instructions = tk.Menu(menubar)
menubar.add_cascade(label='Instructions', menu=instructions)
instructions.add_command(label='Instructions', command=lambda:messagebox.showinfo(message='''This program can subtract two numbers given in the entry boxes.
It first arranges them into thousands, hundreds, tens, and ones, and then subtracts each place and borrows from the next place. It can also subtarct values with a negative answer, although it can't subtract negative values.
To see the borrowing, turn on Show Borrowing in Settings.
This program can't handle negative numbers or numbers greater than 9,999.'''))

root.title('Subtracting')
negative_var = tk.StringVar()
negative_var.set('')
tk.Label(root, textvariable=negative_var).grid(column=0, row=7)
root.mainloop()
