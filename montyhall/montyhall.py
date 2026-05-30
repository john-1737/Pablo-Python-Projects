"""The Monty Hall Problem, by Al Sweigart al@inventwithpython.com
A simulation of the Monty Hall game show problem.
More info at https://en.wikipedia.org/wiki/Monty_Hall_problem
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, math, simulation"""

import random, sys
from tkinter import Tk, PhotoImage, StringVar, Toplevel, Menu
from tkinter.ttk import Frame, Label, Button, Treeview
from webbrowser import open as url


class door:
    def __init__(self, root, closed, car, goat, x, y, xspan=1):
        self.closed = closed
        self.label = Label(root, image=self.closed)
        self.label.grid(column=x, row=y, columnspan=xspan)
    def show_closed(self):
        self.label.config(image=self.closed)
    def show_image(self, image):
        self.label.config(image=image)

def fill_success():
    totalSwaps = swapWins + swapLosses
    if totalSwaps != 0:  # Prevent zero-divide error.
        swapSuccess = round(swapWins / totalSwaps * 100, 1)
    else:
        swapSuccess = 0.0

    totalStays = stayWins + stayLosses
    if (stayWins + stayLosses) != 0:  # Prevent zero-divide.
        staySuccess = round(stayWins / totalStays * 100, 1)
    else:
        staySuccess = 0.0

    for i in tree.get_children():
        tree.delete(i)
    tree.insert('', 'end', text='Swapping:', values=(swapWins, swapLosses, swapSuccess))
    tree.insert('', 'end', text='Staying:', values=(stayWins, stayLosses, staySuccess))

def start_game():
    global doorThatHasCar
    for i in doors:
        i.show_closed()
    doorThatHasCar = random.randint(1, 3)
    dbutton1.grid()
    dbutton2.grid()
    dbutton3.grid()
    sbutton1.grid_remove()
    sbutton2.grid_remove()
    play.grid_remove()
    selectvar.set('')
    promptvar.set('Pick a door 1, 2, or 3:\n')

def select_door(door):
    global doorPick, showGoatDoor
    dbutton1.grid_remove()
    dbutton2.grid_remove()
    dbutton3.grid_remove()
    sbutton1.grid()
    sbutton2.grid()
    doorPick = door
    while True:
        # Select a door that is a goat and not picked by the player:
        showGoatDoor = random.randint(1, 3)
        if showGoatDoor != doorPick and showGoatDoor != doorThatHasCar:
            break

    # Show this goat door to the player:
    if showGoatDoor == 1:
        door1.show_image(goat)
    elif showGoatDoor == 2:
        door2.show_image(goat)
    elif showGoatDoor == 3:
        door3.show_image(goat)
    
    selectvar.set(f'You have selected door {doorPick}.')
    promptvar.set(f'Door {doorPick} contains a goat!\nDo you want to swap doors?')

def select_swap(swap):
    global doorPick, swapWins, swapLosses, stayWins, stayLosses
    sbutton1.grid_remove()
    sbutton2.grid_remove()
    play.grid()
    if swap == True:
        if doorPick == 1 and showGoatDoor == 2:
            doorPick = 3
        elif doorPick == 1 and showGoatDoor == 3:
            doorPick = 2
        elif doorPick == 2 and showGoatDoor == 1:
            doorPick = 3
        elif doorPick == 2 and showGoatDoor == 3:
            doorPick = 1
        elif doorPick == 3 and showGoatDoor == 1:
            doorPick = 2
        elif doorPick == 3 and showGoatDoor == 2:
            doorPick = 1
    selectvar.set(f'You have selected door {doorPick}.')
    car_door = doorThatHasCar-1
    for i, j in enumerate(doors):
        if i == car_door:
            j.show_image(car)
        else:
            j.show_image(goat)

    # Record wins and losses for swapping and not swapping:
    if doorPick == doorThatHasCar:
        promptvar.set(f'Door {doorThatHasCar} has the car!\nYou won!')
        if swap == True:
            swapWins += 1
        elif swap == False:
            stayWins += 1
    else:
        promptvar.set(f'Door {doorThatHasCar} has the car!\nSorry, you lost.')
        if swap == True:
            swapLosses += 1
        elif swap == False:
            stayLosses += 1
    fill_success()

def show_instructions():
    win = Toplevel(root)
    winf = Frame(win)
    winf.grid(sticky='nwes')
    Label(winf, text='''The Monty Hall Problem

In the Monty Hall game show, you can pick one of three doors. One door
has a new car for a prize. The other two doors have worthless goats:''').grid(column=0, row=0, columnspan=3)
    door(winf, doori1, car, goat, 0, 1).show_closed()
    door(winf, doori2, car, goat, 1, 1).show_closed()
    door(winf, doori3, car, goat, 2, 1).show_closed()
    Label(winf, text='''Say you pick Door #1.
Before the door you choose is opened, another door with a goat is opened:''').grid(column=0, row=2, columnspan=3)
    door(winf, doori1, car, goat, 0, 3).show_closed()
    door(winf, doori2, car, goat, 1, 3).show_closed()
    door(winf, goat, car, goat, 2, 3).show_closed()
    Label(winf, text='''You can choose to either open the door you originally picked or swap
to the other unopened door.

It may seem like it doesn't matter if you swap or not, but your odds
do improve if you swap doors! This program demonstrates the Monty Hall
problem by letting you do repeated experiments.

You can read an explanation of why swapping is better at
https://en.wikipedia.org/wiki/Monty_Hall_problem.

This program is based on Al Sweigart's Monty Hall Problem.''').grid(column=0, row=4, columnspan=3)

root = Tk()
root.title('Monty Hall Problem')
swapWins = 0
swapLosses = 0
stayWins = 0
stayLosses = 0
car = PhotoImage(file='door-car.png')
goat = PhotoImage(file='door-goat.png')
f = Frame(root)
f.grid(sticky='nwes')
doori1 = PhotoImage(file='door1.png')
doori2 = PhotoImage(file='door2.png')
doori3 = PhotoImage(file='door3.png')
door1 = door(f, PhotoImage(file='door1.png'), car, goat, 0, 0)
door2 = door(f, PhotoImage(file='door2.png'), car, goat, 1, 0, 2)
door3 = door(f, PhotoImage(file='door3.png'), car, goat, 3, 0)
selectvar = StringVar()
Label(f, textvariable=selectvar).grid(column=0, row=1, columnspan=4)
promptvar = StringVar()
Label(f, textvariable=promptvar).grid(column=0, row=2, columnspan=4)
dbutton1 = Button(f, text='Door 1', command=lambda: select_door(1))
dbutton1.grid(column=0, row=3)
dbutton2 = Button(f, text='Door 2', command=lambda: select_door(2))
dbutton2.grid(column=1, row=3, columnspan=2)
dbutton3 = Button(f, text='Door 3', command=lambda: select_door(3))
dbutton3.grid(column=3, row=3)
sbutton1 = Button(f, text='Yes', command=lambda:select_swap(True))
sbutton1.grid(column=0, row=3, columnspan=2)
sbutton2 = Button(f, text='No', command=lambda:select_swap(False))
sbutton2.grid(column=2, row=3, columnspan=2)
play = Button(f, text='Play again', command=start_game)
play.grid(column=0, row=3, columnspan=4)
Label(f, text='Success totals:').grid(column=0, row=4, columnspan=4)
tree = Treeview(f, columns=('Wins', 'Losses', 'Success rate'), height=3)
for i in ['Wins', 'Losses', 'Success rate']:
    tree.column(i, width=75)
    tree.heading(i, text=i)
tree.column('#0', width=75)
tree.grid(column=0, row=5, columnspan=4)
m = Menu(root)
root['menu'] = m
about_menu = Menu(m)
m.add_cascade(menu=about_menu, label='About')
about_menu.add_command(label='How To Play', command=show_instructions)
about_menu.add_command(label='Wikipedia Article', command=lambda: url('https://en.wikipedia.org/wiki/Monty_Hall_problem'))
m.add_command(label='Reset', command=start_game)
fill_success()
doors = [door1, door2, door3]
start_game()
root.mainloop()