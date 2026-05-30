"""Leetspeak, by Al Sweigart al@inventwithpython.com
Translates English messages into l33t5p34]<.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, word"""

import random, pyperclip
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Label, Button, Entry

def main():
    global root, english, leet, info, b
    root = Tk()
    root.title('Leetspeak')
    f = Frame(root)
    f.grid(sticky='nwes')
    Label(f, text='Enter your message to convert to leetspeak:').grid(column=0, row=0)
    english = StringVar()
    leet = StringVar()
    info = StringVar()
    Entry(f, textvariable=english).grid(column=0, row=1)
    Button(f, text='Convert to leetspeak', command=englishToLeetspeak).grid(column=0, row=2)
    Label(f, textvariable=info).grid(column=0, row=3)
    Label(f, textvariable=leet).grid(column=0, row=4)
    b = Button(f, text='Copy to clipboard', command=copy_leet)
    b.grid(column=0, row=5) ; b.grid_remove()
    root.mainloop()

def englishToLeetspeak():
    """Convert the English string in message and return leetspeak."""
    message = english.get()
    # Make sure all the keys in `charMapping` are lowercase.
    charMapping = {
    'a': ['4', '@'], 'c': ['(', '¢'], 'e': ['3', '€'],
    'i': ['1', '!', '|'], 'l': ['£'],
    'o': ['0'], 's': ['$', '5'], 't': ['7', '+'],
    'y': ['¥']}
    leetspeak = ''
    for char in message:  # Check each character:
        # There is a 70% chance we change the character to leetspeak.
        if char.lower() in charMapping and random.random() <= 0.70:
            possibleLeetReplacements = charMapping[char.lower()]
            leetReplacement = random.choice(possibleLeetReplacements)
            leetspeak = leetspeak + leetReplacement
        else:
            # Don't translate this character:
            leetspeak = leetspeak + char
    leet.set(leetspeak)
    info.set(f'The leetspeak for {message} is:')
    b.grid()

def copy_leet():
    pyperclip.copy(leet.get())

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()