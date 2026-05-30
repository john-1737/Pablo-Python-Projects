"""sPoNgEcAsE, by Al Sweigart al@inventwithpython.com
Translates English messages into sPOnGEcAsE.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, word"""

import random, pyperclip
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Label, Button, Entry

def main():
    global root, english, spongetext, info, b
    root = Tk()
    root.title('sPOnGeCaSe')
    f = Frame(root)
    f.grid(sticky='nwes')
    Label(f, text='eNtEr yOuR mEsSaGe tO coNvErT tO sPoNgEcAsE:').grid(column=0, row=0)
    english = StringVar()
    spongetext = StringVar()
    info = StringVar()
    Entry(f, textvariable=english).grid(column=0, row=1)
    Button(f, text='cOnVErT tO sPoNGeCaSE', command=englishToSpongecase).grid(column=0, row=2)
    Label(f, textvariable=info).grid(column=0, row=3)
    Label(f, textvariable=spongetext).grid(column=0, row=4)
    b = Button(f, text='cOpY tO cLIpBoArD', command=copy_leet)
    b.grid(column=0, row=5) ; b.grid_remove()
    root.mainloop()

def englishToSpongecase():
    """Return the spongecase form of the given string."""
    message = english.get()
    spongecase = ''
    useUpper = False

    for character in message:
        if not character.isalpha():
            spongecase += character
            continue

        if useUpper:
            spongecase += character.upper()
        else:
            spongecase += character.lower()

        # Flip the case, 90% of the time.
        if random.randint(1, 100) <= 90:
            useUpper = not useUpper  # Flip the case.
    spongetext.set(spongecase)
    info.set(f'tHe SpONgeCaSe fOr {message} Is:')
    b.grid()

def copy_leet():
    pyperclip.copy(spongetext.get())

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()