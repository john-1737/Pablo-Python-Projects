"""Gullible, by Al Sweigart al@inventwithpython.com
How to keep a gullible person busy for hours. (This is a joke program.)
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, humor"""

from tkinter import messagebox

while True:  # Main program loop.
    if not messagebox.askyesno('Gullible', 'Do you want to know how to keep a gullible person busy for hours?'):
        break

messagebox.showinfo('Gullible', 'Thank you. Have a nice day!')