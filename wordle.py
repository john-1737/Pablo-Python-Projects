import tkinter as tk
import random as ra
from tkinter import messagebox as mb
turn=0

def submit():
    global turn
    entry_strs = []
    for i in entries:
        entry_strs.append(i.get())
        i.delete(0, 'end')
    guess = ''.join(entry_strs).upper()
    if len(guess) != 5:
        if len(guess) > 5:
            mb.showerror(message='Too long', icon='warning')
            return
        mb.showerror(message='Too short', icon='warning')
        return
    elif guess not in words:
        mb.showerror(message='Word not in word list', icon='warning')
        return
    for i, j in enumerate(labels[turn]):
        j.config(text=guess[i])
        if guess[i] == random_word[i]:
            j.config(bg='green')
        elif guess[i] in random_word:
            j.config(bg='#e5d800')
        else:
            j.config(bg='gray')
    if guess == random_word:
        mb.showinfo(message='Correct')
    elif turn == 5:
        mb.showinfo(message=f'The word was {random_word}')
    turn+=1

    
with open('fiveletterwords.txt') as f:
    words = f.read().upper().splitlines()

random_word = ra.choice(words).upper()

root = tk.Tk()

root.config(bg='black')
root.title('Wordle')
mainframe = tk.Frame(root)
mainframe.config(bg='black')
mainframe.pack(expand=True, fill='both')

labels = []

labels = [[tk.Label(mainframe, width=2, height=1, relief='solid', text=' ', font=('Arial', 44), bd=2, bg='black', fg='white', highlightbackground='white', highlightthickness=2) for i in range(5)] for i in range(6)]
for i in range(6):
    for j in range(5):
        label=labels[i][j]
        label.grid(column=j, row=i, padx=10, pady=10)

tk.Label(mainframe, text='Enter your guess:', font=('Arial', 20), bg='black', fg='white').grid(column=0, columnspan=5, row=6)
letter_vars = []
entries = [tk.Entry(mainframe, width=2, relief='solid', text=' ', font=('Arial', 44), bd=2, bg='black', fg='white', highlightbackground='white', highlightthickness=2, justify='center') for i in range(5)]
for i in range(5):
    letter_var = tk.StringVar()
    entries[i].grid(column=i, row=7, padx=10, pady=10)
    letter_vars.append(letter_var)
    entries[i].config(textvariable=letter_var)

tk.Button(mainframe, text='Submit', bg='blue', fg='black', command=submit).grid(column=0, row=8, columnspan=5)

root.mainloop()