from tkinter import Tk, Label, StringVar, font
from tkinter.ttk import Frame, Button
from tkinter.ttk import Label as ThemeLabel
import random as ra
from tkinter import messagebox as mb
from pyperclip import copy


def submit(evt):
    global turn, guess
    if len(guess) != 5:
        error.set('Not enough letters')
        return
    elif guess not in words:
        error.set('Not in word list')
        return
    error.set('')
    result = ''
    for i, j in enumerate(labels[turn]):
        j.config(text=guess[i])
        if guess[i] == random_word[i]:
            j.config(bg='green')
            result += '🟩'
        elif guess[i] in random_word:
            j.config(bg='lightgreen')
            result += '🟨'
        else:
            j.config(bg='gray')
            result += '⬜️'
    results.append(result)
    if guess == random_word:
        root.after(2000, end_screen)
    elif turn == 5:
        error.set(random_word)
        root.after(2000, end_screen)
    turn+=1
    guess = ''

def submit_letter(event):
    global guess
    if event.keysym == 'BackSpace':
        try:
            guess = guess[0:-1]
        except:
            pass
    elif len(guess) != 5:
        guess += event.keysym.upper()
    for i, j in enumerate(labels[turn]):
        try:
            j.config(text=guess[i])
        except:
            j.config(text='')

def end_screen():
    gframe.grid_remove()
    end_frame.grid()
    if guess == random_word:
        result_var.set(f'You got the word in {turn+1} tries!')
    else:
        result_var.set('You didn\'t get the word in this puzzle.\nMaybe next time.')

def copy_results():
    copy('\n'.join(results))

def start_game():
    global guess, results, labels, random_word, turn
    end_frame.grid_remove()
    gframe.grid()
    guess = ''
    results = []
    random_word = ra.choice(words).upper()
    turn=0
    error.set('')
    font_dict = font.nametofont('TkDefaultFont').actual()
    font_dict['weight'] = 'bold'
    ThemeLabel(gframe, textvariable=error, font=font.Font(**font_dict)).grid(column=0, row=0, columnspan=5)
    labels = [[Label(gframe, width=2, height=1, text=' ', font=('Arial', 44), highlightbackground='gray75', highlightthickness=2, bg='white') for i in range(5)] for i in range(6)]
    for i in range(6):
        for j in range(5):
            labels[i][j].grid(column=j, row=i+1, pady=2, padx=2)
    for i in 'abcdefghijklmnopqrstuvwxyz':
        root.bind(f'<{i}>', submit_letter)
    root.bind('<BackSpace>', submit_letter)
    root.bind('<Return>', submit)
    
with open('fiveletterwords.txt') as f:
    words = f.read().upper().splitlines()

root = Tk()
root.title('Wordle')
gframe = Frame(root)
gframe.grid(sticky='nsew')
end_frame = Frame(root)
end_frame.grid(sticky='nsew')
font_dict = font.nametofont('TkDefaultFont').actual()
font_dict['weight'] = 'bold'
font_dict['size'] = 50
ThemeLabel(end_frame, text='Thanks for playing today!', font=font_dict).grid(column=0, row=0)
result_var = StringVar()
ThemeLabel(end_frame, textvariable=result_var).grid(column=0, row=1)
Button(end_frame, text='Copy Results', command=copy_results).grid(column=0, row=2)
Button(end_frame, text='New Game', command=start_game).grid(column=0, row=3)
error = StringVar()
start_game()
root.mainloop()