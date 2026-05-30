from tkinter import Tk, Canvas, IntVar, StringVar
from tkinter.ttk import Label, Notebook, Entry, Treeview, Spinbox, Frame, Button, Scrollbar
from math import sin, cos, radians
from pyperclip import copy

UPPER_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def translate(message, key, encrypt):
    translated = ''
    if encrypt == False:
        key = -key
    for character in message:
        if character.isupper():
            # Concatenate uppercase translated character.
            transCharIndex = (UPPER_LETTERS.find(character) + key) % 26
            translated += UPPER_LETTERS[transCharIndex]
        elif character.islower():
            # Concatenate lowercase translated character.
            transCharIndex = (LOWER_LETTERS.find(character) + key) % 26
            translated += LOWER_LETTERS[transCharIndex]
        else:
            # Concatenate the character untranslated.
            translated += character
    return translated

def update(*args):
    c.delete('keytext')
    for i,j in enumerate(UPPER_LETTERS, start=key.get()-1):
        c.create_text((sin(radians((i/26)*360))*70)+103, (cos(radians((i/26)*360))*70)+103, text=j, angle=(i/26)*360, tags='keytext')
    encrypted.set(translate(text.get(), key.get()-1, True))
    decrypted.set(translate(text.get(), key.get()-1, False))

def update_hack(*args):
    for i in hacktree.get_children():
        hacktree.delete(i)
    for i in range(1, 27):
        hacktree.insert('', 'end', text=i, values=(translate(hacktext.get(), i-1, False),))

root = Tk()
root.title('Caesar Cipher')
key = IntVar(value=1)
key.trace_add('write', update)
text = StringVar()
text.trace_add('write', update)
encrypted = StringVar()
decrypted = StringVar()
f = Frame(root)
f.grid(sticky='nsew')
n = Notebook(f)
n.grid(sticky='nsew')
cipher = Frame(n)
n.add(cipher, text='Cipher')
hacker = Frame(n)
n.add(hacker, text='Hacker')
Label(cipher, text='Select key 1-26:').grid(column=0, row=0)
Label(cipher, text='Enter message:').grid(column=0, row=2)
Entry(cipher, textvariable=text).grid(column=0, row=3)
mode = Notebook(cipher)
mode.grid(column=0, row=4)
encrypt = Frame(mode)
mode.add(encrypt, text='Encrypt')
decrypt = Frame(mode)
mode.add(decrypt, text='Decrypt')
c = Canvas(cipher, width=200, height=200, highlightthickness=0, bd=0)
c.grid(column=0, row=1)
c.create_oval(3, 3, 203, 203, outline='black', width=1)
c.create_oval(23, 23, 183, 183, outline='black', width=1)
c.create_oval(43, 43, 163, 163, outline='black', width=1)
for i,j in enumerate(UPPER_LETTERS):
    c.create_text((sin(radians((i/26)*360))*90)+103, (cos(radians((i/26)*360))*90)+103, text=j, angle=(i/26)*360)
for i,j in enumerate(UPPER_LETTERS):
    c.create_text((sin(radians((i/26)*360))*70)+103, (cos(radians((i/26)*360))*70)+103, text=j, angle=(i/26)*360, tags='keytext')
s = Spinbox(c, from_=1, to=26, wrap=True, textvariable=key, width=3)
s.state(['readonly'])
c.create_window(103, 103, window=s)
Label(encrypt, text='The encrypted message is:').grid(column=0, row=0); Label(decrypt, text='The decrypted message is:').grid(column=0, row=0)
Label(encrypt, textvariable=encrypted).grid(column=0, row=1), Label(decrypt, textvariable=decrypted).grid(column=0, row=1)
Button(encrypt, text='Copy to clipboard', command=lambda:copy(encrypted.get())).grid(column=0, row=2)
Button(decrypt, text='Copy to clipboard', command=lambda:copy(decrypted.get())).grid(column=0, row=2)
hacktext = StringVar()
hacktext.trace_add('write', update_hack)
Label(hacker, text='Enter text to brute force:').grid(column=0, row=0, columnspan=2)
Entry(hacker, textvariable=hacktext).grid(column=0, row=1, columnspan=2)
Label(hacker, text='All possible keys:').grid(column=0, row=2, columnspan=2)
hacktree = Treeview(hacker, columns=('message',), height=15)
hacktree.grid(column=0, row=3)
hacktree.column('#0', width=30)
hacktree.heading('#0', text='Key')
hacktree.heading('message', text='Message')
for i in range(1, 27):
    hacktree.insert('', 'end', text=i, values=('',))
sb = Scrollbar(hacker, command=hacktree.yview)
sb.grid(column=1, row=3, sticky='ns')
hacktree['yscrollcommand'] = sb.set
root.mainloop()