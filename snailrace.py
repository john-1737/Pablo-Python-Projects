"""Snail Race, by Al Sweigart al@inventwithpython.com
Fast-paced snail racing action!
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, artistic, beginner, game, multiplayer"""

import random, time, sys
from tkinter import Tk, Canvas, IntVar, StringVar, PhotoImage
from tkinter.ttk import Frame, Spinbox, Entry, Label, Button

# Set up the constants:
MAX_NUM_SNAILS = 8
MAX_NAME_LENGTH = 20
FINISH_LINE = 40  # (!) Try modifying this number.


def get_names():
    global name_vars
    race_canvas.grid_remove()
    names.grid()
    name_error.set('')
    num_names.set(2)
    name_vars = [StringVar(), StringVar()]
    fill_name_list()

def update_names(*args):
    global name_vars
    if len(name_vars) == num_names.get() + 1:
        del name_vars[-1]
    elif len(name_vars) == num_names.get() - 1:
        name_vars.append(StringVar())
    fill_name_list()

def fill_name_list():
    for i in name_list.winfo_children():
        i.destroy()
    for i, j in enumerate(name_vars):
        Label(name_list, text=f'Enter snail {i+1}\'s name:').grid(column=0, row=i*2)
        Entry(name_list, textvariable=j).grid(column=0, row=i*2+1)

def submit_names():
    names = [i.get() for i in name_vars]
    for i in names:
        if len(i) == 0:
            name_error.set('Please enter names for all the snails.')
            return
    if len(set(names)) != len(names):
        name_error.set('Please enter different names for all the snails.')
        return
    race()

def get_shortened_name(name, max=MAX_NAME_LENGTH):
    new_name = name[:max]
    if len(new_name) != len(name):
        new_name = new_name[:max-1] + '…'
    return new_name

def race():
    global b, textwidths
    names.grid_remove()
    race_canvas.grid()
    race_canvas.delete('all')
    try:
        b1.destroy()
        b2.destroy()
    except:
        pass
    race_canvas.create_text(5, 0, text='Start', anchor='nw')
    race_canvas.create_text(FINISH_LINE*15+5, 0, text='Finish', anchor='ne')
    textwidths = []
    for i, j in enumerate([k.get() for k in name_vars]):
        race_canvas.create_image(5, i*30+30, image=snail, tags='race items', anchor='nw')
        text = race_canvas.create_text(5, i*30+30, text=get_shortened_name(j), tags='race items', anchor='sw')
        root.update()
        textwidths.append(race_canvas.bbox(text)[2] - race_canvas.bbox(text)[0])
    b = Button(race_canvas, text='Start', default='active', command=start_race)
    race_canvas.create_window((FINISH_LINE*15+15)/2+5, 255/2, window=b, tags='start')

def start_race():
    global snailNames
    race_canvas.delete('start')
    b.destroy()
    snailNames = [i.get() for i in name_vars]
    snailProgress = {}
    for snailName in snailNames:
        snailProgress[snailName] = 0
    for i in range(3, 0, -1):
        race_canvas.delete('start')
        race_canvas.create_text((FINISH_LINE*15+15)/2+5, 255/2, text=str(i), tags='start', font=('Helvetica', 75))
        root.update()
        time.sleep(1)
    race_canvas.delete('start')
    root.update()
    numSnailsRacing = num_names.get()
    while True:  # Main program loop.
        # Pick random snails to move forward:
        for i in range(random.randint(1, numSnailsRacing // 2)):
            randomSnailName = random.choice(snailNames)
            snailProgress[randomSnailName] += 1

            # Check if a snail has reached the finish line:
            if snailProgress[randomSnailName] == FINISH_LINE:
                winner(snailProgress)
                return

        # (!) EXPERIMENT: Add a cheat here that increases a snail's progress
        # if it has your name.

        time.sleep(0.01)  # (!) EXPERIMENT: Try changing this value.

        # (!) EXPERIMENT: What happens if you comment this line out?

        # Display the snails (with name tags):
        race_canvas.delete('all')
        race_canvas.create_text(5, 0, text='Start', anchor='nw')
        race_canvas.create_text(FINISH_LINE*15+5, 0, text='Finish', anchor='ne')
        for i, snailName in enumerate(snailNames):
            spaces = snailProgress[snailName]
            race_canvas.create_image(spaces*15+5, i*30+30, image=snail, tags='race items', anchor='nw')
            race_canvas.create_line(0, i*30+45, spaces*15+5, i*30+45, width=2, fill='#00ff00')
            if (FINISH_LINE*15+15) - (spaces*15+5) < textwidths[i]:
                race_canvas.create_text(FINISH_LINE*15+15, i*30+30, text=get_shortened_name(snailName), tags='race items', anchor='se')
            else:
                race_canvas.create_text(spaces*15+5, i*30+30, text=get_shortened_name(snailName), tags='race items', anchor='sw')
        root.update()

def winner(snailProgress):
    race_canvas.delete('all')
    race_canvas.create_text(5, 0, text='Start', anchor='nw')
    race_canvas.create_text(FINISH_LINE*15+5, 0, text='Finish', anchor='ne')
    for i, snailName in enumerate(snailNames):
        spaces = snailProgress[snailName]
        race_canvas.create_image(spaces*15+5, i*30+30, image=snail, tags='race items', anchor='nw')
        race_canvas.create_line(0, i*30+45, spaces*15+5, i*30+45, width=2, fill='#00ff00')
        if (FINISH_LINE*15+15) - (spaces*15+5) < textwidths[i]:
            race_canvas.create_text(FINISH_LINE*15+15, i*30+30, text=get_shortened_name(snailName), tags='race items', anchor='se')
        else:
            race_canvas.create_text(spaces*15+5, i*30+30, text=get_shortened_name(snailName), tags='race items', anchor='sw')
    root.update()
    global b1, b2
    race_canvas.create_rectangle((FINISH_LINE*15+15)/2+5-200, 255/2-100, (FINISH_LINE*15+15)/2+5+200, 255/2+100, fill='white', outline='black')
    race_canvas.create_text((FINISH_LINE*15+15)/2+5, 255/2-100, text='We have a winner!', anchor='n')
    snailNames.sort(key=lambda i: snailProgress[i], reverse=True)
    race_canvas.create_text((FINISH_LINE*15+15)/2+5, 255/2-75, text='🥇: ' + get_shortened_name(snailNames[0], 16), anchor='n', font=('Helvetica', 40))
    race_canvas.create_text((FINISH_LINE*15+15)/2+5, 255/2-25, text='🥈: ' + get_shortened_name(snailNames[1]), anchor='n')
    try:
        race_canvas.create_text((FINISH_LINE*15+15)/2+5, 255/2, text='🥉: ' + get_shortened_name(snailNames[2]), anchor='n')
    except IndexError:
        pass
    b1 = Button(race_canvas, text='Play Again', command=race)
    b2 = Button(race_canvas, text='Restart', command=get_names)
    race_canvas.create_window((FINISH_LINE*15+15)/2+5, 255/2+25, window=b1)
    race_canvas.create_window((FINISH_LINE*15+15)/2+5, 255/2+50, window=b2)
    root.update()

root = Tk()
root.title('Snail Race')
snail = PhotoImage(file='snail.png')
f = Frame(root)
f.grid(sticky='nwes')
num_names = IntVar(value=2)
name_vars = [StringVar(), StringVar()]
name_error = StringVar()
num_names.trace_add('write', update_names)
names = Frame(f)
names.grid(column=0, row=0)
race_canvas = Canvas(f, height=255, width=FINISH_LINE*15+20)
race_canvas.grid(column=0, row=0); race_canvas.grid_remove()
race_canvas.create_text(5, 0, text='Start', anchor='nw')
race_canvas.create_text(FINISH_LINE*15+5, 0, text='Finish', anchor='ne')
s = Spinbox(names, from_=2, to=8, textvariable=num_names, width=1)
name_list = Frame(names)
name_list.grid(column=0, row=2, columnspan=2)
s.state(['readonly'])
s.grid(column=1, row=0)
Label(names, text='How many snails will race? (Max 8)').grid(column=0, row=0)
Label(names, textvariable=name_error).grid(column=0, row=1, columnspan=2)
Button(names, text='Submit', command=submit_names, default='active').grid(column=0, row=3, columnspan=2)
get_names()
root.mainloop()