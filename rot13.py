"""ROT13 Cipher, by Al Sweigart al@inventwithpython.com
The simplest shift cipher for encrypting and decrypting text.
More info at https://en.wikipedia.org/wiki/ROT13
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, cryptography"""

import pyperclip
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Label, Entry, Button

# Set up the constants:
UPPER_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def update(*args):
    message = plaintext.get()
    translated = ''
    for character in message:
        if character.isupper():
            # Concatenate uppercase translated character.
            transCharIndex = (UPPER_LETTERS.find(character) + 13) % 26
            translated += UPPER_LETTERS[transCharIndex]
        elif character.islower():
            # Concatenate lowercase translated character.
            transCharIndex = (LOWER_LETTERS.find(character) + 13) % 26
            translated += LOWER_LETTERS[transCharIndex]
        else:
            # Concatenate the character untranslated.
            translated += character
    ciphertext.set(translated)

def copy():
    pyperclip.copy(ciphertext.get())

root = Tk()
root.title('ROT13 Cipher')
f = Frame(root)
f.grid(sticky='nwes')
Label(f, text='Enter a message to encrypt/decrypt:').grid(column=0, row=0)
plaintext = StringVar()
ciphertext = StringVar()
Entry(f, textvariable=plaintext).grid(column=0, row=1)
Label(f, text='The translated message is:').grid(column=0, row=2)
Label(f, textvariable=ciphertext).grid(column=0, row=3)
Button(f, text='Copy to clipboard', command=copy).grid(column=0, row=4)
plaintext.trace_add('write', update)
root.mainloop()
