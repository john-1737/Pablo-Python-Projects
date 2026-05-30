"""Simple Substitution Cipher, by Al Sweigart al@inventwithpython.com
A simple substitution cipher has a one-to-one translation for each
symbol in the plaintext and each symbol in the ciphertext.
More info at: https://en.wikipedia.org/wiki/Substitution_cipher
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, cryptography, math"""

import random
from tkinter import Tk, StringVar, Toplevel
from tkinter.ttk import Notebook, Label, Frame, Button, Entry

try:
    import pyperclip  # pyperclip copies text to the clipboard.
except ImportError:
    pass  # If pyperclip is not installed, do nothing. It's no big deal.

# Every possible symbol that can be encrypted/decrypted:
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    global key, error, encrypted, decrypted, message, root
#     print('''Simple Substitution Cipher, by Al Sweigart
# A simple substitution cipher has a one-to-one translation for each
# symbol in the plaintext and each symbol in the ciphertext.''')
    root = Tk()
    root.title('Simple Substitution Cipher')
    f = Frame(root)
    f.grid(sticky='nsew')
    Label(f, text='Enter the key to use:').grid(column=0, row=0)
    key = StringVar()
    Entry(f, textvariable=key, width=26).grid(column=0, row=1)
    key.trace_add('write', update)
    error = StringVar(value='⚠︎ Invalid key')
    Label(f, textvariable=error, foreground='red').grid(column=0, row=2)
    Button(f, text='Generate random key', command=generateRandomKey).grid(column=0, row=3)
    Label(f, text='Enter the message to encrypt/decrypt:').grid(column=0, row=5)
    message = StringVar()
    Entry(f, textvariable=message).grid(column=0, row=6)
    message.trace_add('write', update)
    n = Notebook(f)
    n.grid(column=0, row=7)
    f1 = Frame(f)
    n.add(f1, text='Encrypt')
    f2 = Frame(f)
    n.add(f2, text='Decrypt')
    Label(f1, text='The encrypted message is:').grid(column=0, row=0)
    Label(f2, text='The decrypted message is:').grid(column=0, row=0)
    encrypted = StringVar()
    decrypted = StringVar()
    Label(f1, textvariable=encrypted).grid(column=0, row=1)
    Label(f2, textvariable=decrypted).grid(column=0, row=1)
    Button(f1, text='Copy to clipboard', command=copy_encrypted).grid(column=0, row=2)
    Button(f2, text='Copy to clipboard', command=copy_decrypted).grid(column=0, row=2)
    Button(f, text='Help', command=help).grid(column=0, row=8)
    root.mainloop()
    return

def checkKey(key):
    """Return True if key is valid. Otherwise return False."""
    keyList = list(key)
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()
    if keyList != lettersList:
        return False
    return True

def update(*args):
    key.set(key.get().upper())
    if not checkKey(key.get().upper()):
        error.set('⚠︎ Invalid key')
        encrypted.set('')
        decrypted.set('')
        return
    error.set('')
    encrypted.set(encryptMessage(message.get(), key.get()))
    decrypted.set(decryptMessage(message.get(), key.get()))

def encryptMessage(message, key):
    """Encrypt the message using the key."""
    return translateMessage(message, key, 'encrypt')


def decryptMessage(message, key):
    """Decrypt the message using the key."""
    return translateMessage(message, key, 'decrypt')


def translateMessage(message, key, mode):
    """Encrypt or decrypt the message using the key."""
    translated = ''
    charsA = LETTERS
    charsB = key
    if mode == 'decrypt':
        # For decrypting, we can use the same code as encrypting. We
        # just need to swap where the key and LETTERS strings are used.
        charsA, charsB = charsB, charsA

    # Loop through each symbol in the message:
    for symbol in message:
        if symbol.upper() in charsA:
            # Encrypt/decrypt the symbol:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # The symbol is not in LETTERS, just add it unchanged.
            translated += symbol

    return translated


def generateRandomKey():
    """Generate and return a random encryption key."""
    key_list = list(LETTERS)  # Get a list from the LETTERS string.
    random.shuffle(key_list)  # Randomly shuffle the list.
    key.set(''.join(key_list))  # Get a string from the list.

def copy_encrypted():
    pyperclip.copy(encrypted.get())

def copy_decrypted():
    pyperclip.copy(decrypted.get())

def help():
    win = Toplevel(root)
    win.title('Help')
    n = Notebook(win)
    n.grid(sticky='nwes')

    n.add(Label(n, text='''Welcome to Simple Substitution Cipher!
A simple substitution cipher has a one-to-one translation for each
symbol in the plaintext and each symbol in the ciphertext.
The translation is determined by a key that maps each consecutive
letter of the alphabet to the corresponding letter in the key.
          
This program is inspired by Al Sweigart's Simple Substitution Cipher.'''), text='About')
    
    f1 = Frame(n)
    n.add(f1, text='Encryption')
    Label(f1, text='''A simple substitution cipher has a one-to-one translation for each
symbol in the plaintext and each symbol in the ciphertext.
The translation is determined by a key that maps each consecutive
letter of the alphabet to the corresponding letter in the key.
For example, if the key was TCSOUQXBVMNZGFLPHJIRAYWEDK, the letters
of the alphabet would be encrypted in this format:''').grid(column=0, row=0)
    Label(f1, text='''ABCDEFGHIJKLMNOPQRSTUVWXYZ
↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎↕︎
TCSOUQXBVMNZGFLPHJIRAYWEDK''', font='TkFixedFont').grid(column=0, row=1)
    Label(f1, text='''When we encrypt, we substitute the letters in the top row for the
letters in the bottom row, and we do it the other way when we
decrypt. Because each letter can be encrypted for another
letter, but no two can be encrypted for the same letter, there
are 26 possible letters for the letter A, 25 for B, and so on. This
means there are 26×25×24…3×2×1 possible combinations, which works
out to 403,291,461,126,605,635,584,000,000 possible combinations.
That's too many keys to test each of them, so you may wonder how you
break the cipher. The way you do it is by noting something as
follows. If the letter M appears a lot in the message, and the
letter E appears a lot in the English language, then M might equal E.''').grid(column=0, row=2)
    n.add(Label(n, text='''To use this program, follow the following steps:
• Enter a key.
• Enter a message.
• Select whether to encrypt or decrypt.
You can create a key manually, or press Generate random key to make a random
one. If the key is invalid, the message will not show and the text "Invalid key"
will appear below the key. You can press Copy to clipboard to copy the message
to your clipboard.'''), text='Using the program')

# If this program was run (instead of imported), run the program:
if __name__ == '__main__':
    main()
