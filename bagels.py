"""Bagels, by Al Sweigart al@inventwithpython.com
A deductive logic game where you must guess a number based on clues.
This code is available at https://nostarch.com/big-book-small-python-programming
A version of this game is featured in the book, "Invent Your Own
Computer Games with Python" https://nostarch.com/inventwithpython
Tags: short, game, puzzle"""

import random
from tkinter import Tk, StringVar, Menu, messagebox, Toplevel
from tkinter.ttk import Entry, Frame, Label, Button, Menubutton, Notebook

def change_difficulty(d):
    difficulty.set(d)
    new_game()

def new_game():
    global length, guesses, secretNumber, previous_guesses
    length = {'easy': 3, 'medium': 4, 'hard': 5}[difficulty.get()]
    guesses = 10
    numbers = list('0123456789')  # Create a list of digits 0 to 9.
    random.shuffle(numbers)  # Shuffle them into random order.
    secretNumber = ''
    for i in range(length):
        secretNumber += str(numbers[i])
    start_frame.grid_remove()
    game_frame.grid()
    previous_guesses = ['' for i in range(10)]
    previous_var.set('\n'*10)
    e.grid()
    set_entry('')
    b.grid()
    root.bind('<Return>', lambda e: b.invoke())
    instruction.set(f'I am thinking of a {length} digit number.\n\n\nYou have 10 guesses left. Take a guess.')

def reset_difficulty():
    if guesses == 0 or messagebox.askokcancel(message='Are you sure? This will start a new game, and you will lose your progress.'):
        new_game()
    else:
        difficulty.set({3: 'easy', 4: 'medium', 5: 'hard'}[length])

def set_entry(text):
    e.delete(0, 'end')
    e.insert(0, text)

def getClues(guess, secretNum):
    """Returns a string with the pico, fermi, bagels clues for a guess
    and secret number pair."""
    if guess == secretNum:
        return 'You got it!'

    clues = []

    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            # A correct digit is in the correct place.
            clues.append('Fermi')
        elif guess[i] in secretNum:
            # A correct digit is in the incorrect place.
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'  # There are no correct digits at all.
    else:
        # Sort the clues into alphabetical order so their original order
        # doesn't give information away.
        clues.sort()
        # Make a single string from the list of string clues.
        return ' '.join(clues)

def start_screen():
    game_frame.grid_remove()
    start_frame.grid()
    root.unbind('<Return>')

def previous_guess_format(clues):
    clues = clues.split(' ')
    for i in range(len(clues)):
        clues[i] = clues[i][0].lower()
    return ' '.join(clues)

def guess_again():
    global guesses
    num = e.get()
    if not num.isdigit():
        instruction.set(f'I am thinking of a {length} digit number.\n\nPlease enter a number.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return
    if not len(num) == length:
        instruction.set(f'I am thinking of a {length} digit number.\n\nPlease enter a {length} digit number.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return
    if str(num) in [i.split(':')[0] for i in previous_guesses]:
        instruction.set(f'I am thinking of a {length} digit number.\n\nYou\'ve already guessed this number.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return
    if sorted(list(set(num))) != sorted(list(num)):
        instruction.set(f'I am thinking of a {length} digit number.\n\nPlease enter a number without duplicates.\nYou have {guesses} guesses left. Take a guess.')
        set_entry('')
        return        
    guesses -= 1
    if num == secretNumber:
        previous_guesses[guesses] = f'{num}: ✓'
        previous_var.set('\n'.join(previous_guesses[::-1]))
        e.grid_remove()
        b.grid_remove()
        root.unbind('<Return>')
        guesses = 0
        instruction.set('Yay! You guessed my number!')
        return
    clues = getClues(num, secretNumber)
    previous_guesses[guesses] = f'{num}: {previous_guess_format(clues)}'
    instruction.set(f'I am thinking of a {length} digit number.\n\nYour clues are:\n{clues}\nYou have {guesses} guesses left. Take a guess.')
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
    n.add(Label(n, text='''Welcome to Bagels!
In this game, you have 10 chances to guess a number.
You can choose between Easy, Medium, and Hard difficulty.
Easy difficulty gives you a 3 digit number.
Medium difficulty gives you 4 digit number.
Hard difficulty gives you a 5 digit number.

This game is inspired by Al Sweigart's Bagels.'''), text='Overview')
    
    n.add(Label(n, text='''To guess a number while playing, enter the number in the
entry field and press Submit.
When you guess a number, the screen will the following clues:
Pico: One digit is correct but in the wrong position.
Fermi: One digit is correct and in the right position.
Bagels: No digit is correct.
The number will also appear in the previous guesses list,
which shows the previous guesses, and also a letter p for
every correct digit but incorrect position, a f for every
correct digit and correct position, a b if no digits are
correct, and a ✓ if it is correct.
For example, if the list shows this:
                
715: fp
123: b
                
it means the number 713 has one correct digit in the right
position and one correct digit in the wrong position, and
the number 123 has no correct digits.
Note that you can guess numbers beginning in 0s, like 012.'''), text='Playing')
    
    n.add(Label(n, text='''The following buttons appear in the home screen:
Easy: Starts a game at easy difficulty. (3 digit number)
Medium: Starts a game at medium difficulty. (4 digit number)
Hard: Starts a game at hard difficulty. (5 digit number)
Help: Shows help screen.
                
The following buttons appear in the playing screen:
Submit: Submit your guess.
New Game: Starts a new game.
Difficulty: Starts a new game with a different difficulty.
Open Home Screen: Takes you to the home screen.
Help: Shows help screen.'''), text='Controls')

root = Tk()
root.title('Bagels')
difficulty = StringVar(value='hard')
f = Frame(root)
f.grid(sticky='nwes')
start_frame = Frame(f)
start_frame.grid(column=0, row=0)
game_frame = Frame(f)
game_frame.grid(column=0, row=0); game_frame.grid_remove()
Label(start_frame, text='Welcome to Bagels!\nSelect a difficulty or click Help.').grid(column=0, row=0)
Button(start_frame, text='Easy', command=lambda: change_difficulty('easy')).grid(column=0, row=1)
Button(start_frame, text='Medium', command=lambda: change_difficulty('medium')).grid(column=0, row=2)
Button(start_frame, text='Hard', command=lambda: change_difficulty('hard')).grid(column=0, row=3)
previous_guesses = ['' for i in range(10)]
previous_var = StringVar(value='\n'*10)
Label(game_frame, textvariable=previous_var).grid(column=0, row=1)
Label(game_frame, text='Previous guesses:').grid(column=0, row=0)
Label(game_frame, text='Key:\np : correct digit, wrong position\nf : correct digit, correct position\nb : no correct digits\n✓ : correct').grid(column=0, row=2)
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