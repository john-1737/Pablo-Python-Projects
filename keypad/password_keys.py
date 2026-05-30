from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from tkinter import Tk, PhotoImage
from tkinter.ttk import Button, Label, Frame
import time
from sys import exit

def _respond_num_key(key='?123'):
    global enteredtext, display, symbol_display
    if key in ('1234567890'):
        enteredtext += key
    elif key == '.':
        if '.'  not in enteredtext:
            enteredtext += '.'
    elif key == 'delete':
        enteredtext = list(enteredtext)
        try:
            enteredtext.pop()
        except:
            pass
        enteredtext = ''.join(enteredtext)
    elif key == '-':
        if enteredtext.startswith('-'):
            enteredtext = list(enteredtext)
            enteredtext.pop(0)
            enteredtext = ''.join(enteredtext)
        else:
            enteredtext = '-' + enteredtext

def _exit_str_keyboard():
    global exit
    exit = True

def int_keyboard(head='Enter number', inittext=''):
    global exit
    global close
    global enteredtext, key_buttons
    exit = False
    close = False
    root = Tk()
    f = Frame(root)
    f.grid(sticky='nwes')
    root.title(head)
    enteredtext = ''
    textlabel = Label(root, text=inittext, foreground='gray')
    textlabel.grid(column=0, row=0, columnspan=11)
    key_buttons = {}
    for y, i in enumerate((tuple('789'),
            tuple('456'),
            tuple('123')), start=1):
        for x, j in enumerate(i):
            img = PhotoImage(file=f'key{j}.png')
            PhotoImage.subsample(img, x=4)
            button = Button(root, image=img, command=lambda j=j : _respond_num_key(j))
            button.grid(column=x, row=y)
            key_buttons[j] = button
    button = Button( text='0',command= lambda :_respond_num_key('0'))
    button.grid(column=0, row=4, columnspan=2)
    key_buttons['0'] = button
    button = Button( text='.',command= lambda :_respond_num_key('.'))
    button.grid(column=2, row=4, columnspan=1)
    key_buttons['.'] = button
    button = Button(text='enter',command=_exit_str_keyboard)
    button.grid(column=3, row=3, rowspan=2)
    key_buttons['?123'] = button
    while True:
        if exit:
            if close:
                enteredtext = ''
            break
        else:
            if enteredtext:
                textlabel.config(text=enteredtext, foreground='black')
            else:
                textlabel.config(text=inittext, fg='gray')
            root.update()
    root.destroy()
    try:
        return int(enteredtext)
    except:
        return 0.0

tries = 3
while True:
    for i in range(tries, -1, -1):
        password = int_keyboard(f'Enter password ({i} tries left)', 'Enter the password')
        if password == 2025:
            mb.showinfo(message='Correct')
            exit()
        elif not password:
            exit()
        if i:
            mb.showinfo(message=f'Incorrect password ({i} tries left)')
    go = mb.askokcancel(message='Press OK to try again in 10 seconds.')
    if not go:
        break
    time.sleep(10)
