"""Cho-Han, by Al Sweigart al@inventwithpython.com
The traditional Japanese dice game of even-odd.
View this code athttps://nostarch.com/big-book-small-python-projects
Tags: short, beginner, game"""

import random, sys
from tkinter import Tk, StringVar, PhotoImage, Toplevel
from tkinter.ttk import Frame, Button, Entry, Label

JAPANESE_NUMBERS = {1: 'ICHI', 2: 'NI', 3: 'SAN',
                    4: 'SHI', 5: 'GO', 6: 'ROKU'}

purse = 5000
def get_bet():
    # Place your bet:
    out_frame.grid_remove()
    result_frame.grid_remove()
    bet_frame.grid()
    bet_var.set('')
    bet_instructions.set('You have ' +str(purse)+ ' mon. How much do you bet?')
    bet_error.set('')

def submit_bet():
    pot = bet_var.get()
    if not pot.isdecimal():
        bet_error.set('Please enter a number.')
    elif int(pot) > purse:
        bet_error.set('You do not have enough to make that bet.')
    else:
        # This is a valid bet.
        pot = int(pot)  # Convert pot to an integer.
        roll()
        return
    bet_var.set('')

def roll():
    global dice1, dice2
    # Roll the dice.
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    bet_frame.grid_remove()
    decision_frame.grid()

def reveal(decision):
    global purse
    # Reveal the dice results:
    decision_frame.grid_remove()
    result_frame.grid()

    # Determine if the player won:
    rollIsEven = (dice1 + dice2) % 2 == 0
    if rollIsEven:
        correctBet = 'cho'
    else:
        correctBet = 'han'

    l1.config(text=JAPANESE_NUMBERS[dice1], image=DIE_IMAGES[dice1])
    l2.config(text=JAPANESE_NUMBERS[dice2], image=DIE_IMAGES[dice2])

    playerWon = decision == correctBet
    pot = int(bet_var.get())

    # Display the bet results:
    if playerWon:
        result.set(f'You won! You take {pot} mon. 🤑\nThe house collects a {pot // 10} mon fee.')
        purse = purse + pot  # Add the pot from player's purse.
        purse = purse - (pot // 10)  # The house fee is 10%.
    else:
        purse = purse - pot  # Subtract the pot from player's purse.
        result.set('You lost!')

def restart():
    if purse == 0:
        out()
    else:
        get_bet()

def out():
    result_frame.grid_remove()
    out_frame.grid()

def reload():
    global purse
    purse = 5000
    get_bet()

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Cho-Han!

In this traditional Japanese dice game, two dice are rolled in a bamboo
cup by the dealer sitting on the floor. The player must guess if the
dice total to an even (cho) or odd (han) number.
If you guess correctly, you earn money (although the gambling house
takes a small cut of all winnings), whereas if you guess incorrectly,
you lose money. If you run out of money, you have the option to reload
your purse.
          
Here are the Japanese words used in this game:

cho: even
han: odd
ichi: one
ni: two
san: three
shi: four
go: five
roku: six
mon: Japanese currency from the 1800s

This game is inspired by Al Sweigart's Cho-Han.''').grid()

root = Tk()
root.title('Cho-Han')
DIE_IMAGES = {}
for i in range(1, 7):
    DIE_IMAGES[i] = PhotoImage(file=f'die{i}.png')
f = Frame(root)
f.grid(sticky='nwes')
bet_frame = Frame(f)
bet_frame.grid(column=0, row=0, sticky='nwes')
decision_frame = Frame(f)
decision_frame.grid(column=0, row=0, sticky='nwes'); decision_frame.grid_remove()
result_frame = Frame(f)
result_frame.grid(column=0, row=0, sticky='nwes'); result_frame.grid_remove()
out_frame = Frame(f)
out_frame.grid(column=0, row=0, sticky='nwes'); out_frame.grid_remove()
Button(f, text='Help', command=help).grid(column=0, row=1)
bet_instructions = StringVar()
Label(bet_frame, textvariable=bet_instructions).grid(column=0, row=0)
bet_error = StringVar()
Label(bet_frame, textvariable=bet_error).grid(column=0, row=1)
bet_var = StringVar()
Entry(bet_frame, textvariable=bet_var).grid(column=0, row=2)
Button(bet_frame, text='Submit', command=submit_bet).grid(column=0, row=3)
Label(decision_frame, text='''The dealer swirls the cup and you hear the rattle of dice.
The dealer slams the cup on the floor, still covering the
dice and asks for your bet.''').grid(column=0, row=0, columnspan=2)
Button(decision_frame, text='CHO (even)', command=lambda: reveal('cho')).grid(column=0, row=1)
Button(decision_frame, text='HAN (odd)', command=lambda: reveal('han')).grid(column=1, row=1)
Label(result_frame, text='The dealer lifts the cup to reveal:').grid(column=0, row=0, columnspan=2)
l1 = Label(result_frame, compound='bottom'); l1.grid(column=0, row=1)
l2 = Label(result_frame, compound='bottom'); l2.grid(column=1, row=1)
result = StringVar()
Label(result_frame, textvariable=result).grid(column=0, row=2, columnspan=2)
Button(result_frame, text='Restart', command=restart).grid(column=0, row=3, columnspan=2)
Label(out_frame, text='You have run out of money!').grid(column=0, row=0)
Button(out_frame, text='Reload purse', command=reload).grid(column=0, row=1)
get_bet()
root.mainloop()