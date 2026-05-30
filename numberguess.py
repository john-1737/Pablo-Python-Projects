"""Guess the Number, by Al Sweigart al@inventwithpython.com
Try to guess the secret number based on hints.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, game"""

import random
from tkinter import Tk, StringVar, Menu, messagebox, Toplevel
from tkinter.ttk import Entry, Frame, Label, Button, Menubutton, Notebook

def change_difficulty(d):
    difficulty.set(d)
    new_game()

def new_game():
    global highest, guesses, secretNumber, previous_guesses
    highest = {'easy': 10, 'medium': 50, 'hard': 100}[difficulty.get()]
    guesses = 10
    secretNumber = random.randint(1, highest)
    start_frame.grid_remove()
    game_frame.grid()
    previous_guesses = ['' for i in range(10)]
    previous_var.set('\n'*10)
    e.grid()
    set_entry('')
    b.grid()
    root.bind('<Return>', lambda e: b.invoke())
    instruction.set(f'I am thinking of a number in between 1 and {highest}.\n\n\nYou have 10 guesses left. Take a guess.')

def reset_difficulty():
    if guesses == 0 or messagebox.askokcancel(message='Are you sure? This will start a new game, and you will lose your progress.'):
        new_game()
    else:
        difficulty.set({10: 'easy', 50: 'medium', 100: 'hard'}[highest])

def set_entry(text):
    e.delete(0, 'end')
    e.insert(0, text)

def start_screen():
    game_frame.grid_remove()
    start_frame.grid()
    root.unbind('<Return>')

def guess_again():
    global guesses
    num = e.get()
    if not num.isdigit():
        instruction.set(f'I am thinking of a number in between 1 and {highest}.\n\nPlease enter a number.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return
    num = int(num)
    if not 1 <= num <= highest:
        instruction.set(f'I am thinking of a number in between 1 and {highest}.\n\nPlease enter a number between 1 and {highest}.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return
    if str(num) in [i.split(':')[0] for i in previous_guesses]:
        instruction.set(f'I am thinking of a number in between 1 and {highest}.\n\nYou\'ve already guessed this number.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return
    guesses -= 1
    if num < secretNumber:
        previous_guesses[guesses] = f'{num}: -'
        instruction.set(f'I am thinking of a number in between 1 and {highest}.\n\nYour guess is too low.\nYou have {guesses} guesses left. Take a guess.')
    elif num > secretNumber:
        previous_guesses[guesses] = f'{num}: +'
        instruction.set(f'I am thinking of a number in between 1 and {highest}.\n\nYour guess is too high.\nYou have {guesses} guesses left. Take a guess.')
    elif num == secretNumber:
        previous_guesses[guesses] = f'{num}: ✓'
        previous_guesses.sort(key=lambda x: x.split(':')[0])
        previous_var.set('\n'.join(previous_guesses[::-1]))
        e.grid_remove()
        b.grid_remove()
        root.unbind('<Return>')
        guesses = 0
        instruction.set('Yay! You guessed my number!')
        return
    previous_guesses.sort(key=lambda x: x.split(':')[0])
    previous_var.set('\n'.join(previous_guesses[::-1]))
    if guesses == 0:
        e.grid_remove()
        b.grid_remove()
        root.unbind('<Return>')
        instruction.set(f'Game over. The number I was thinking of was {secretNumber}')
        return
    set_entry('')

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    n = Notebook(f)
    n.grid()
    n.add(Label(n, text='''Welcome to Guess The Number!
In this game, you have 10 chances to guess a number.
You can choose between Easy, Medium, and Hard difficulty.
Easy difficulty gives you a number between 0 and 10.
Medium difficulty gives you a number between 0 and 50.
Hard difficulty gives you a number between 0 and 100.

This game is inspired by Al Sweigart's Guess The Number.'''), text='Overview')
    
    n.add(Label(n, text='''To guess a number while playing, enter the number in the
entry field and press Submit.
When you guess a number, the screen will show whether the
number is too high, too low, or correct. The number will
also appear in the previous guesses list, which shows the
previous guesses, and also a + sign if the number is too
high, a - if it is too low, and a ✓ if it is correct.
For example, if the list shows this:
                
58: +
30: -
                
it means the number is higher than 30, but less than 58.'''), text='Playing')
    
    n.add(Label(n, text='''The following buttons appear in the home screen:
Easy: Starts a game at easy difficulty. (number from 1-10)
Medium: Starts a game at medium difficulty. (number from 1-50)
Hard: Starts a game at hard difficulty. (number from 1-100)
Help: Shows help screen.
                
The following buttons appear in the playing screen:
Submit: Submit your guess.
New Game: Starts a new game.
Difficulty: Starts a new game with a different difficulty.
Open Home Screen: Takes you to the home screen.
Help: Shows help screen.'''), text='Controls')

root = Tk()
root.title('Guess The Number')
difficulty = StringVar(value='hard')
f = Frame(root)
f.grid(sticky='nwes')
start_frame = Frame(f)
start_frame.grid(column=0, row=0)
game_frame = Frame(f)
game_frame.grid(column=0, row=0); game_frame.grid_remove()
Label(start_frame, text='Welcome to Guess The Number!\nSelect a difficulty or click Help.').grid(column=0, row=0)
Button(start_frame, text='Easy', command=lambda: change_difficulty('easy')).grid(column=0, row=1)
Button(start_frame, text='Medium', command=lambda: change_difficulty('medium')).grid(column=0, row=2)
Button(start_frame, text='Hard', command=lambda: change_difficulty('hard')).grid(column=0, row=3)
previous_guesses = ['' for i in range(10)]
previous_var = StringVar(value='\n'*10)
Label(game_frame, textvariable=previous_var).grid(column=0, row=1)
Label(game_frame, text='Previous guesses:').grid(column=0, row=0)
Label(game_frame, text='Key:\n+ : too high\n- : too low\n✓ : correct').grid(column=0, row=2)
instruction = StringVar()
Label(game_frame, textvariable=instruction).grid(column=0, row=3)
e = Entry(game_frame)
e.grid(column=0, row=4)
b = Button(game_frame, text='Submit', default='active', command=guess_again)
b.grid(column=0, row=5)
mb = Menubutton(game_frame, text='Difficulty')
m = Menu(mb)
for i in ['Easy', 'Medium', 'Hard']:
    m.add_radiobutton(label=i, variable=difficulty, value=i.lower(), command=reset_difficulty)
mb['menu'] = m
mb.grid(column=0, row=7)
Button(game_frame, text='New Game', command=new_game).grid(column=0, row=6)
Button(game_frame, text='Open Home Screen', command=start_screen).grid(column=0, row=8)
Button(f, text='Help', command=help).grid(column=0, row=1)
root.mainloop()