"""Fibonacci Sequence, by Al Sweigart al@inventwithpython.com
Calculates numbers of the Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13...
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, math"""

import sys
from tkinter import Text, Tk, StringVar, messagebox, Toplevel
from tkinter.ttk import Frame, Entry, Label, Button, Scrollbar

def write(text):
    t.config(state='normal')
    t.insert('end', text)
    t.config(state='disabled')

def calculate():
    response = number.get()
    if not response.isdecimal() or int(response) == 0:
        error.set('Please enter a number greater than 0, or QUIT.')
        return
    nth = int(response)
    t.config(state='normal')
    t.delete('1.0', 'end')
    t.config(state='disabled')

    # Handle the special cases if the user entered 1 or 2:
    if nth == 1:
        write('0')
        result.set('The #1 Fibonacci number is 0.')
        return
    elif nth == 2:
        write('0, 1')
        result.set('The #2 Fibonacci number is 1.')
        return

    # Display warning if the user entered a large number:
    if nth >= 10000:
        messagebox.showwarning(message='''WARNING: This will take a while to display on the
screen. If you want to quit this program before it is
done, press Ctrl-C.''')
        root.update()

    # Calculate the Nth Fibonacci number:
    secondToLastNumber = 0
    lastNumber = 1
    fibNumbersCalculated = 2
    write('0, 1, ')  # Display the first two Fibonacci numbers.

    # Display all the later numbers of the Fibonacci sequence:
    while True:
        nextNumber = secondToLastNumber + lastNumber
        fibNumbersCalculated += 1

        # Display the next number in the sequence:
        write(str(nextNumber))

        # Check if we've found the Nth number the user wants:
        if fibNumbersCalculated == nth:
            result.set(f'The #{fibNumbersCalculated} Fibonacci number is {nextNumber}')
            return

        # Print a comma in between the sequence numbers:
        write(', ')
        root.update()

        # Shift the last two numbers:
        secondToLastNumber = lastNumber
        lastNumber = nextNumber

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Fibonacci Sequence!
          
The Fibonacci sequence begins with 0 and 1, and the next number is the
sum of the previous two numbers. The sequence continues forever:

0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987....
Based on Al Sweigart's Fibonacci Sequence.''').grid()
    
root = Tk()
root.title('Fibonacci Sequence')
f = Frame(root)
f.grid(sticky='nwes')
Label(f, text='Enter the Nth Fibonacci number you wish to\ncalculate (such as 5, 50, 1000, 9999).').grid(column=0, row=0, columnspan=2)
error = StringVar()
number = StringVar()
Label(f, textvariable=error).grid(column=0, row=1, columnspan=2)
Entry(f, textvariable=number).grid(column=0, row=2, columnspan=2)
Button(f, text='Calculate', command=calculate, default='active').grid(column=0, row=3, columnspan=2)
t = Text(f, width=35, font='TkTextFont', wrap='word')
t.grid(column=0, row=4)
s = Scrollbar(f, orient='vertical', command=t.yview)
t['yscrollcommand'] = s.set
s.grid(column=1, row=4, sticky='ns')
result = StringVar()
Label(f, textvariable=result).grid(column=0, row=5, columnspan=2)
Button(f, text='Help', command=help).grid(column=0, row=6, columnspan=2)
root.mainloop()