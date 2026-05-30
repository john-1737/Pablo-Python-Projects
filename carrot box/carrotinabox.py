"""Carrot in a Box, by Al Sweigart al@inventwithpython.com
A silly bluffing game between two human players. Based on the game
from the show, 8 Out of 10 Cats.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, beginner, game, two-player"""

import random
from tkinter import Tk, StringVar, PhotoImage, Toplevel
from tkinter.ttk import Frame, Button, Entry, Label

def show_instructions():
    win = Toplevel(root)
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''This is a bluffing game for two human players. Each player has a box.
One box has a carrot in it. To win, you must have the box with the
carrot in it.

This is a very simple and silly game.

The first player looks into their box (the second player must close
their eyes during this.) The first player then says "There is a carrot
in my box" or "There is not a carrot in my box". The second player then
gets to decide if they want to swap boxes or not.
        
This game is based on Al Sweigart's Carrot In A Box.''').grid()

root = Tk()
root.title('Carrot In A Box')
boxes = {}
for i in ('red', 'blue'):
    boxdict = {}
    for j in ('closed', 'empty', 'carrot'):
        boxdict[j] = PhotoImage(file=f'box-{i}-{j}.png')
    boxes[i] = boxdict.copy()
mainframe = Frame(root)
mainframe.grid(sticky='nwes')
f = Frame(mainframe)
f.grid(column=0, row=0, sticky='nwes')
Button(mainframe, text='Help', command=show_instructions).grid(column=0, row=1)
p1Name = StringVar()
p2Name = StringVar()
entry1 = Entry(f, textvariable=p1Name)
entry1.grid(column=1, row=0)
entry2 = Entry(f, textvariable=p2Name)
entry2.grid(column=1, row=1)
name1 = Label(f, text='Human player 1, enter your name:')
name1.grid(column=0, row=0)
name2 = Label(f, text='Human player 2, enter your name:')
name2.grid(column=0, row=1)
box_label = Label(f, text='')
box_label.grid(column=0, row=0, columnspan=2)
box1 = Label(f, textvariable=p1Name, compound='top')
box1.grid(column=0, row=1)
box2 = Label(f, textvariable=p2Name, compound='top')
box2.grid(column=1, row=1)
instruction_label = Label(f, text='')
instruction_label.grid(column=0, row=2, columnspan=2)
continue_button = Button(f, text='Continue')
continue_button.grid(column=0, row=3, columnspan=2)
yes_button = Button(f, text='Yes')
yes_button.grid(column=0, row=3)
no_button = Button(f, text='No')
no_button.grid(column=1, row=3)

def clear_frame(f):
    for i in f.winfo_children():
        i.grid_remove()

def enter_names():
    clear_frame(f)
    entry1.grid()
    entry2.grid()
    name1.grid()
    name2.grid()
    p1Name.set('')
    p2Name.set('')
    continue_button.grid()
    continue_button.config(text='Start', command=start_game)

def start_game():
    clear_frame(f)
    box_label.grid()
    box1.grid()
    box2.grid()
    instruction_label.grid()
    continue_button.grid()
    continue_button.config(text='Continue', command=show_first_box)
    box_label.config(text='Here are two boxes:')
    box1.config(image=boxes['red']['closed'])
    box2.config(image=boxes['blue']['closed'])
    instruction_label.config(text=f'''{p1Name.get()}, you have a red box in front of you.
{p2Name.get()}, you have a blue box in front of you.

{p1Name.get()}, you will get to look into your box.
{p2Name.get()}, close your eyes and don\'t look!!!
When {p2Name.get()} has closed their eyes, press Continue.''')
    
def show_first_box():
    global carrotInFirstBox
    if random.randint(1, 2) == 1:
        carrotInFirstBox = True
    else:
        carrotInFirstBox = False
    if carrotInFirstBox:
        box1.config(image=boxes['red']['carrot'])
        instruction_label.config(text='''Your box has a carrot!
Press Continue to continue.''')
    else:
        box1.config(image=boxes['red']['empty'])
        instruction_label.config(text='''Your box does not have a carrot.
Press Continue to continue.''')
    box_label.config(text=f'{p1Name.get()}, here is the inside of your box:')
    continue_button.config(command=open_eyes)

def open_eyes():
    box1.config(image=boxes['red']['closed'])
    box_label.config(text='')
    instruction_label.config(text=f'''{p1Name.get()}, tell {p2Name.get()} to open their eyes.
Then press Continue to continue.''')
    continue_button.config(command=tell_p2)
    
def tell_p2():
    instruction_label.config(text=f'''{p1Name.get()}, say one of the following sentences to {p2Name.get()}.
  1) There is a carrot in my box.
  2) There is not a carrot in my box.
                             
Then press Continue to continue.''')
    continue_button.config(command=ask_swap)

def ask_swap():
    instruction_label.config(text=f'{p2Name.get()}, do you want to swap boxes with {p1Name.get()}?')
    continue_button.grid_remove()
    yes_button.grid()
    no_button.grid()
    yes_button.config(command=lambda: swap(True))
    no_button.config(command=lambda: swap(False))

def swap(swapped):
    global firstBox, secondBox, carrotInFirstBox
    yes_button.grid_remove()
    no_button.grid_remove()
    continue_button.grid()
    firstBox = 'red'
    secondBox = 'blue'

    if swapped:
        carrotInFirstBox = not carrotInFirstBox
        firstBox, secondBox = secondBox, firstBox

    box1.config(image=boxes[firstBox]['closed'])
    box2.config(image=boxes[secondBox]['closed'])
    box_label.config(text='Here are the two boxes:')
    instruction_label.config(text='Press Continue to reveal the winner.')
    continue_button.config(command=show_winner)

def show_winner():
    box_label.config(text='')
    if carrotInFirstBox:
        box1.config(image=boxes[firstBox]['carrot'])
        box2.config(image=boxes[secondBox]['empty'])
        instruction_label.config(text=f'{p1Name.get()} is the winner!\n\nPress Restart to play again.')
    else:
        box1.config(image=boxes[firstBox]['empty'])
        box2.config(image=boxes[secondBox]['carrot'])
        instruction_label.config(text=f'{p2Name.get()} is the winner!\n\nPress Restart to play again.')
    continue_button.config(text='Restart', command=enter_names)

enter_names()
root.mainloop()


# print()
# print(p2Name + ', do you want to swap boxes with ' + p1Name + '? YES/NO')
# while True:
#     response = input('> ').upper()
#     if not (response.startswith('Y') or response.startswith('N')):
#         print(p2Name + ', please enter "YES" or "NO".')
#     else:
#         break

# firstBox = 'RED '  # Note the space after the "D".
# secondBox = 'GOLD'

# if response.startswith('Y'):
#     carrotInFirstBox = not carrotInFirstBox
#     firstBox, secondBox = secondBox, firstBox

# print('''HERE ARE THE TWO BOXES:
#   __________     __________
#  /         /|   /         /|
# +---------+ |  +---------+ |
# |   {}  | |  |   {}  | |
# |   BOX   | /  |   BOX   | /
# +---------+/   +---------+/'''.format(firstBox, secondBox))
# print(playerNames)

# input('Press Enter to reveal the winner...')
# print()

# if carrotInFirstBox:
#     print('''
#    ___VV____      _________
#   |   VV    |    |         |
#   |   VV    |    |         |
#   |___||____|    |_________|
#  /    ||   /|   /         /|
# +---------+ |  +---------+ |
# |   {}  | |  |   {}  | |
# |   BOX   | /  |   BOX   | /
# +---------+/   +---------+/'''.format(firstBox, secondBox))

# else:
#     print('''
#    _________      ___VV____
#   |         |    |   VV    |
#   |         |    |   VV    |
#   |_________|    |___||____|
#  /         /|   /    ||   /|
# +---------+ |  +---------+ |
# |   {}  | |  |   {}  | |
# |   BOX   | /  |   BOX   | /
# +---------+/   +---------+/'''.format(firstBox, secondBox))

# print(playerNames)

# # This modification made possible through the 'carrotInFirstBox variable
# if carrotInFirstBox:
#     print(p1Name + ' is the winner!')
# else:
#     print(p2Name + ' is the winner!')

# print('Thanks for playing!')
