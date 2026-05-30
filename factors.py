"""Factor Finder, by Al Sweigart al@inventwithpython.com
Finds all the factors of a number.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, math"""

import math, sys
from tkinter import Tk, Text, StringVar, messagebox, Toplevel
from tkinter.ttk import Frame, Button, Label, Entry, Scrollbar, Progressbar
from tkinter.font import nametofont

def factor():
    number = number_var.get()
    if not number.isdecimal():
        messagebox.showwarning(message='Number must be an integer')
        return
    elif not int(number) > 0:
        messagebox.showwarning(message='Number must be greater than 0')
        return
    number = int(number)

    factors = []
    b.grid()
    t.config(state='normal')
    t.delete('1.0', 'end')
    ns = '\n'*10
    t.insert('1.0', f"{ns}{' ' * 3}Loading...")
    t.config(state='disabled')

    # Find the factors of number:
    for i in range(1, int(math.sqrt(number)) + 1):
        if number % i == 0:  # If there's no remainder, it is a factor.
            factors.append(i)
            factors.append(number // i)
        b.config(value=i/int(math.sqrt(number))*100)
        root.update()

    b.grid_remove()
    root.update()

    # Convert to a set to get rid of duplicate factors:
    factors = list(set(factors))
    factors.sort()

    # Display the results:
    t.config(state='normal')
    t.delete('1.0', 'end')
    for i, factor in enumerate(factors):
        factors[i] = str(factor)
    t.insert('1.0', ', '.join(factors))
    t.config(state='disabled')

def help():
    win = Toplevel(root)
    Label(win, text='''Welcome to Factor Finder!

A number's factors are two numbers that, when multiplied with each
other, produce the number. For example, 2 x 13 = 26, so 2 and 13 are
factors of 26. 1 x 26 = 26, so 1 and 26 are also factors of 26. We
say that 26 has four factors: 1, 2, 13, and 26.

If a number only has two factors (1 and itself), we call that a prime
number. Otherwise, we call it a composite number.

Can you discover some prime numbers?
          
This program is based on Al Sweigart's Factor Finder.''').grid(sticky='nsew')

root = Tk()
root.title('Factor Finder')
f = Frame(root)
f.grid(sticky='nwes')
number_var = StringVar()
Label(f, text='Enter a positive whole number to factor:').grid(column=0, row=0)
Entry(f, textvariable=number_var).grid(column=0, row=1)
Button(f, text='Factor', command=factor).grid(column=0, row=2)
t = Text(f, font=nametofont('TkDefaultFont'), wrap='word', width=25, state='disabled')
t.grid(column=0, row=3)
s = Scrollbar(f, command=t.yview, orient='vertical')
s.grid(column=1, row=3, sticky='ns')
t['yscrollcommand'] = s.set
b = Progressbar(f, orient='horizontal', length=200)
b.grid(column=0, row=3) ; b.grid_remove()
Button(f, text='Help', command=help).grid(column=0, row=4)
root.mainloop()