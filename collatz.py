"""Collatz Sequence, by Al Sweigart al@inventwithpython.com
Generates numbers for the Collatz sequence, given a starting number.
More info at: https://en.wikipedia.org/wiki/Collatz_conjecture
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, math"""

import sys, time
from tkinter import Tk, StringVar, Text, messagebox, Toplevel
from tkinter.ttk import Frame, Label, Button, Entry, Scrollbar

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Collatz Sequence, Collatz Conjecture,
or, the 3n + 1 Problem!

The Collatz sequence is a sequence of numbers produced from a starting
number n, following three rules:

1) If n is even, the next number n is n / 2.
2) If n is odd, the next number n is n * 3 + 1.
3) If n is 1, stop. Otherwise, repeat.

It is generally thought, but so far not mathematically proven, that
every starting number eventually terminates at 1.
        
This program is inspired by Al Sweigart's Collatz Sequence.''').grid()

def calculate():
    response = number.get()
    if not response.isdecimal() or response == '0':
        messagebox.showwarning(message='You must enter an integer greater than 0.')
        return

    n = int(response)
    collatz_nums = [str(n)]
    while n != 1:
        if n % 2 == 0:  # If n is even...
            n = n // 2
        else:  # Otherwise, n is odd...
            n = 3 * n + 1

        collatz_nums.append(str(n))
    t.config(state='normal')
    t.delete('0.0', 'end')
    t.insert('end', ', '.join(collatz_nums))
    t.config(state='disabled')

root = Tk()
f = Frame(root)
f.grid(sticky='nwes')
root.title('Collatz Sequence')
Label(f, text='Enter a starting number (greater than 0):').grid(column=0, row=0, columnspan=2)
number = StringVar()
Entry(f, textvariable=number).grid(column=0, row=1, columnspan=2)
Button(f, text='Calculate', command=calculate).grid(column=0, row=2, columnspan=2)
t = Text(f, background='gray90', font='TkDefaultFont', width=25, height=15, state='disabled', wrap='word')
t.grid(column=0, row=3)
b = Scrollbar(f, orient='vertical', command=t.yview)
t['yscrollcommand'] = b.set
b.grid(column=1, row=3, sticky='ns')
Button(f, text='Help', command=help).grid(column=0, row=4, columnspan=2)
root.mainloop()