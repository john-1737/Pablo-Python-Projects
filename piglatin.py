"""Pig Latin, by Al Sweigart al@inventwithpython.com
Translates English messages into Igpay Atinlay.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, word"""

import random, pyperclip
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Label, Button, Entry

def main():
    global root, english, platin, info, b
    root = Tk()
    root.title('Pig Latin')
    f = Frame(root)
    f.grid(sticky='nwes')
    Label(f, text='Enter your message to convert to pig latin:').grid(column=0, row=0)
    english = StringVar()
    platin = StringVar()
    info = StringVar()
    Entry(f, textvariable=english).grid(column=0, row=1)
    Button(f, text='Convert to pig latin', command=englishToPiglatin).grid(column=0, row=2)
    Label(f, textvariable=info).grid(column=0, row=3)
    Label(f, textvariable=platin).grid(column=0, row=4)
    b = Button(f, text='Copy to clipboard', command=copy_platin)
    b.grid(column=0, row=5) ; b.grid_remove()
    root.mainloop()

def englishToPiglatin():
    """Convert the English string in message and return pig latin."""
    message = english.get()
    pigLatin = ''  # A string of the pig latin translation.
    for word in message.split():
        # Separate the non-letters at the start of this word:
        prefixNonLetters = ''
        while len(word) > 0 and not word[0].isalpha():
            prefixNonLetters += word[0]
            word = word[1:]
        if len(word) == 0:
            pigLatin = pigLatin + prefixNonLetters + ' '
            continue

        # Separate the non-letters at the end of this word:
        suffixNonLetters = ''
        while not word[-1].isalpha():
            suffixNonLetters = word[-1] + suffixNonLetters
            word = word[:-1]

        # Remember if the word was in uppercase or titlecase.
        wasUpper = word.isupper()
        wasTitle = word.istitle()

        word = word.lower()  # Make the word lowercase for translation.

        # Separate the consonants at the start of this word:
        prefixConsonants = ''
        while len(word) > 0 and not word[0] in ('a', 'e', 'i', 'o', 'u', 'y'):
            prefixConsonants += word[0]
            word = word[1:]

        # Add the pig latin ending to the word:
        if prefixConsonants != '':
            word += prefixConsonants + 'ay'
        else:
            word += 'yay'

        # Set the word back to uppercase or titlecase:
        if wasUpper:
            word = word.upper()
        if wasTitle:
            word = word.title()

        # Add the non-letters back to the start or end of the word.
        pigLatin += prefixNonLetters + word + suffixNonLetters + ' '
    platin.set(pigLatin)
    info.set(f'The pig latin for {message} is:')
    b.grid()

def copy_platin():
    pyperclip.copy(platin.get())

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()