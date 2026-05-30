"""Million Dice Roll Statistics Simulator
By Al Sweigart al@inventwithpython.com
A simulation of one million dice rolls.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, math, simulation"""

import random, time
from PIL import Image, ImageTk
from tkinter import Tk, StringVar, messagebox
from tkinter.ttk import Treeview, Label, Entry, Button, Progressbar, Frame, Scrollbar
rolling = False

def split_gif_into_frames(gif_path, right=False):
    """
    Splits an animated GIF into individual image frames.

    Args:
        gif_path (str): The path to the input GIF file.
        output_folder (str): The folder where individual frames will be saved.
    """
    frames = []
    with Image.open(gif_path) as im:
        for i in range(im.n_frames):
            im.seek(i)
            im.convert('RGBA')
            frames.append(ImageTk.PhotoImage(im))
    frames.pop(0)
    return frames

def roll_dice():
    global rolling
    if rolling == True:
        return
    num = numvar.get()
    if not num.isdecimal():
        messagebox.showwarning('Please enter an integer.')
        return
    num = int(num)
    results = {}
    for i in range(num, (num * 6) + 1):
        results[i] = 0
    t.grid_remove()
    s.grid_remove()
    l.grid()
    b.grid()

    # Simulate dice rolls:
    frame = 0
    for i in range(1000000):
        if i % 1000 == 0:
            l.config(text=f'Simulating 1,000,000 rolls of {num} dice...\n{int(round(i / 10000, 0))}% done...', image=frames[frame//5000], compound='bottom')
            b.config(value=i/10000)
            root.update()

        total = 0
        for j in range(num):
            total = total + random.randint(1, 6)
        results[total] = results[total] + 1
        frame += 1
        frame %= len(frames)*5000
    t.grid()
    s.grid()
    l.grid_remove()
    b.grid_remove()
    rolling = False

    # Display results:
    for i in t.get_children():
        t.delete(i)
    for i in range(num, (num * 6) + 1):
        roll = results[i]
        percentage = round(results[i] / 10000, 1)
        t.insert('', 'end', text=i, values=(roll, percentage))
    

root = Tk()
root.title('Million Dice Roll Statistics Simulator')
numvar = StringVar()
f = Frame(root)
f.grid(sticky='nwes')
Label(f, text='Enter how many six-sided dice you want to roll:').grid(column=0, row=0, columnspan=2)
Entry(f, textvariable=numvar).grid(column=0, row=1, columnspan=2)
Button(f, text='Roll', default='active', command=roll_dice).grid(column=0, row=2, columnspan=2)
l = Label(f)
l.grid(column=0, row=3, columnspan=2); l.grid_remove()
b = Progressbar(f)
b.grid(column=0, row=4, columnspan=2); b.grid_remove()
t = Treeview(f, columns=('rolls', 'percentage'))
t.heading('#0', text='Total')
t.heading('rolls', text='Rolls')
t.heading('percentage', text='Percentage')
t.grid(column=0, row=3, rowspan=2)
s = Scrollbar(f, orient='vertical', command=t.yview)
t['yscrollcommand'] = s.set
s.grid(column=1, row=3, rowspan=2, sticky='ns')
frames = split_gif_into_frames('die_animated.gif')
root.mainloop()