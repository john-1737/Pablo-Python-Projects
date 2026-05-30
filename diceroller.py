"""Dice Roller, by Al Sweigart al@inventwithpython.com
Simulates dice rolls using the Dungeons & Dragons dice roll notation.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, simulation"""

import random, sys
from tkinter import Tk, Text, StringVar, font
from tkinter.ttk import Button, Label, Frame, Notebook, Entry, Scrollbar, Spinbox, Combobox
from tkinter import Button as TkButton

def check_dndvar(*args):
    if dndvar.get() == '':
        return
    dnd_str = dndvar.get().lower()
    dnd_str = list(dnd_str)
    dnd_str = [i for i in dnd_str if i in '1234567890d+-']
    while dnd_str.count('d') > 1:
        dnd_str.remove('d')
    while dnd_str.count('+') > 1:
        dnd_str.remove('+')
    while dnd_str.count('-') > 1:
        dnd_str.remove('-')
    if '+' in dnd_str and not 'd' in dnd_str:
        dnd_str.remove('+')
    if '-' in dnd_str and not 'd' in dnd_str:
        dnd_str.remove('-')
    if '+' in dnd_str and '-' in dnd_str:
        dnd_str.remove('-')
    dnd_str = ''.join(dnd_str)
    dndvar.set(dnd_str)

def check_number(var):
    if var.get() == '':
        return
    var_str = var.get().lower()
    var_str = list(var_str)
    var_str = [i for i in var_str if i in '1234567890']
    var_str = ''.join(var_str)
    var.set(var_str)

def add_to_dnd(char):
    dndvar.set(dndvar.get() + char)

def delete_from_dnd():
    dndvar.set(dndvar.get()[:-1])

def dnd_to_standard(dndvar):
    diceStr = dndvar.get()
    dice = [None, None, None]
    dIndex = diceStr.find('d')
    if dIndex == -1:
        dice[0] = 1

    # Get the number of dice. (The "3" in "3d6+1"):
    numberOfDice = diceStr[:dIndex]
    if not numberOfDice.isdecimal():
        dice[0] = 1
    else:
        dice[0] = int(numberOfDice)

    # Find if there is a plus or minus sign for a modifier:
    modIndex = diceStr.find('+')
    if modIndex == -1:
        modIndex = diceStr.find('-')

    # Find the number of sides. (The "6" in "3d6+1"):
    if modIndex == -1:
        numberOfSides = diceStr[dIndex + 1 :]
    else:
        numberOfSides = diceStr[dIndex + 1 : modIndex]
    if not numberOfSides.isdecimal():
        dice[1] = 1
    else:
        dice[1] = int(numberOfSides)

    # Find the modifier amount. (The "1" in "3d6+1"):
    if modIndex == -1:
        modAmount = 0
    else:
        modAmount = diceStr[modIndex + 1 :]
        if not modAmount.isdecimal:
            modAmount = 0
        else:
            modAmount = int(modAmount)
        if diceStr[modIndex] == '-':
            # Change the modification amount to negative:
            modAmount = -modAmount

    dice[2] = modAmount
    if dice[1] == 0:
        dice[1] = 1
    return dice

def roll_dice():
    if n.index(n.select()) == 0:
        if standard_vars[2].get() == 'None':
            dndvar.set(f'{standard_vars[0].get()}d{standard_vars[1].get()}')
        else:
            dndvar.set(f'{standard_vars[0].get()}d{"".join([i.get() for i in standard_vars[1:]])}')
    dice = dnd_to_standard(dndvar)
    # Simulate the dice rolls:
    rolls = []
    for i in range(dice[0]):
        rollResult = random.randint(1, dice[1])
        rolls.append(rollResult)

    # Display the total:
    totalvar.set(f'Total: {sum(rolls) + dice[2]}\nEach die:')
    each_die.config(state='normal')
    each_die.delete('1.0', 'end')
    # Display the individual rolls:
    for i, roll in enumerate(rolls):
        rolls[i] = str(roll)
    each_die.insert('end', ', '.join(rolls))

    # Display the modifier amount:
    if dice[2] != 0:
        if dice[2] == abs(dice[2]):
            modSign = '+'
        else:
            modSign = '-'
        each_die.insert('end', ', {}{}'.format(modSign, abs(dice[2])))
    each_die.config(state='disabled')

def switch_tabs(*args):
    if n.index(n.select()) == 0:
        dice = dnd_to_standard(dndvar)
        for i, j in zip(standard_vars[:2], dice[:2]):
            i.set(str(j))
        if dice[2] > 0:
            standard_vars[2].set('+')
        elif dice[2] == 0:
            standard_vars[2].set('None')
        else:
            standard_vars[2].set('-')
        standard_vars[3].set(str(abs(dice[2])))
    else:
        if standard_vars[2].get() == 'None':
            dndvar.set(f'{standard_vars[0].get()}d{standard_vars[1].get()}')
        else:
            dndvar.set(f'{standard_vars[0].get()}d{"".join([i.get() for i in standard_vars[1:]])}')

root = Tk()
root.title('Dice Roller')
f = Frame(root)
f.grid(sticky='nwes')
n = Notebook(f)
n.grid(column=0, row=0)
f1 = Frame(n)
f2 = Frame(n)
n.add(f1, text='Standard Format')
n.add(f2, text='Dungeons & Dragons Format')
#This code creates the Dungeons & Dragons notation window
dndvar = StringVar()
Entry(f2, textvariable=dndvar).grid(column=0, row=0, columnspan=4)
dndvar.trace_add('write', check_dndvar)
dnd_button_values = ('123', '456', '789')
for i, j in enumerate(dnd_button_values, start=1):
    for k, l in enumerate(j):
        TkButton(f2, width=2, height=2, text=l, command=lambda char=l: add_to_dnd(char)).grid(row=i, column=k)
for i, j in enumerate('+d-'):
    TkButton(f2, width=2, height=2, text=j, command=lambda char=j: add_to_dnd(char)).grid(row=5, column=i)
TkButton(f2, width=9, height=2, text='0', command=lambda: add_to_dnd('0')).grid(row=4, column=0, columnspan=2)
TkButton(f2, width=2, height=2, text='←', command=delete_from_dnd).grid(row=4, column=2)
#This code creates the standard notation window
standard_vars = [StringVar(), StringVar(), StringVar(), StringVar()]
Label(f1, text='Number of dice:').grid(column=0, row=0, columnspan=3)
Spinbox(f1, textvariable=standard_vars[0], from_=1, to=1000000).grid(column=0, row=1, columnspan=3)
Label(f1, text='Dice sides:').grid(column=0, row=2, columnspan=3)
Spinbox(f1, textvariable=standard_vars[1], from_=1, to=1000000).grid(column=0, row=3, columnspan=3)
Label(f1, text='Modification:').grid(column=0, row=4, columnspan=3)
Combobox(f1, textvariable=standard_vars[2], values=['+', '-', 'None'], state='readonly', width=4).grid(column=0, row=5)
Spinbox(f1, textvariable=standard_vars[3], from_=0, to=1000000, width=13).grid(column=1, row=5, columnspan=2)
for i in standard_vars[:2] + standard_vars[3:]:
    i.trace_add('write', lambda a, b, c, i=i: check_number(i))
Button(f, text='Roll dice', command=roll_dice).grid(column=0, row=1)
#This code sets up the rest of the interface
totalvar = StringVar()
Label(f, textvariable=totalvar).grid(column=0, row=2)
each_die = Text(f, width=40, wrap='word', font=font.nametofont('TkDefaultFont'), background='gray90', state='disabled')
each_die.grid(column=0, row=3)
s = Scrollbar(f, command=each_die.yview, orient='vertical')
s.grid(column=1, row=3, sticky='ns')
each_die['yscrollcommand'] = s.set
n.bind('<<NotebookTabChanged>>', switch_tabs)
root.mainloop()