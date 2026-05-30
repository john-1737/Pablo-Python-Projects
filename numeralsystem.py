"""Numeral System Counters, by Al Sweigart al@inventwithpython.com
Shows equivalent numbers in decimal, hexadecimal, and binary.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, math"""

from tkinter import Tk, StringVar, messagebox, BooleanVar, Toplevel
from tkinter.ttk import Frame, Button, Label, Notebook, Entry, Treeview, Scrollbar, Checkbutton, Combobox
from pyperclip import copy as clip

def display_nums():
    global start, amount
    if not starting_num.get().isdecimal():
        messagebox.showinfo(message='Please enter an integer for the starting number.')
        return
    if not display_num.get().isdecimal():
        messagebox.showinfo(message='Please enter an integer for the ending number.')
        return
    start = int(starting_num.get())
    amount = int(display_num.get())
    show_nums()

def show_nums():
    for i in t.get_children():
        t.delete(i)
    for number in range(start, start + amount):  # Main program loop.
        # Convert to hexadecimal/binary and remove the prefix:
        if not prefixes.get():
            t.insert('', 'end', text=number, values=(hex(number)[2:].upper(), oct(number)[2:], bin(number)[2:]))
        else:
            t.insert('', 'end', text=number, values=('0x'+hex(number)[2:].upper(), oct(number), bin(number)))

def convert():
    global converted
    num = convert_num.get().lower()
    changed = False
    for i, j in zip(('0b', '0x', '0o'), ('Binary', 'Hexadecimal', 'Octal')):
        if num.startswith(i):
            num = num[2:]
            if change_prefix.get():
                convert_from.set(j)
                changed = True
            break
    if change_prefix.get() and not changed:
        convert_from.set('Decimal')
    try:
        int(num, base={'hexadecimal': 16, 'octal': 8, 'binary': 2, 'decimal': 0}[convert_from.get().lower()])
    except ValueError:
        messagebox.showinfo(message=f'The number provided is not a {convert_from.get().lower()} number.')
        return
    num = eval({'hexadecimal': '0x', 'octal': '0o', 'binary': '0b', 'decimal': ''}[convert_from.get().lower()]+num)
    converted = num
    show_converted()

def show_converted():
    if result_prefix.get() or convert_to.get() == 'Decimal':
        result_num.set({'hexadecimal': hex, 'octal': oct, 'binary': bin, 'decimal': str}[convert_to.get().lower()](converted))
    else:
        result_num.set({'hexadecimal': hex, 'octal': oct, 'binary': bin}[convert_to.get().lower()](converted)[2:])

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    n = Notebook(f)
    n.grid()
    n.add(Label(n, text='''Welcome to Numeral System Counters!
In this app, you can explore multiple number systems, such
as the following:

Decimal: base 10 (digits 0-9)
Hexadecimal: base 16 (digits 0-9, then A-F)
Octal: base 8 (digits 0-8)
Binary: base 2 (digits 0-1)

This app is inspired by Al Sweigart's Numeral System Counters.'''), text='Overview')
    
    n.add(Label(n, text='''In the Numbers window, you can find multiple numbers in their
decimal, hexadecimal, octal, and binary forms. To do this,
simply enter the start and end numbers and press Display
Numbers.

The start and end numbers must be decimal numbers.

The Show Prefixes checkbox shows the prefixes for the numbers,
which are as follows:

Decimal: no prefix
Hexadecimal: 0x
Octal: 0o
Binary: 0b'''), text='Numbers window')
    
    n.add(Label(n, text='''
In the Converter window, you can convert numbers among decimal,
hexadecimal, octal, and binary forms. To do this, simply enter
the number you wish to convert, select the form to convert from
and the form you want to convert to, and press Convert.

The Starting Number Prefix Changes Type checkbox allows you to
change the form you want to convert from by changing the prefix
for the starting number to the following prefixes:
                
Decimal: no prefix
Hexadecimal: 0x
Octal: 0o
Binary: 0b
                
The Show Converted Number Prefix checkbox shows the above
prefixes on the converted number.

The Copy button copies the result to your clipboard.'''), text='Converter window')

def copy():
    clip(result_num.get())
    messagebox.showinfo(message='Copied result to clipboard')

root = Tk()
root.title('Numeral System Counters')
mainframe = Frame(root)
mainframe.grid(sticky='nwes')
n = Notebook(mainframe)
n.grid()
Button(mainframe, text='Help', command=help).grid(column=0, row=1)
count_frame = Frame(n)
n.add(count_frame, text='Numbers')
starting_num = StringVar()
display_num = StringVar()
start, amount = 0, 0
Label(count_frame, text='Enter the starting number (e.g. 0):').grid(column=0, row=0, columnspan=2)
Entry(count_frame, textvariable=starting_num).grid(column=0, row=1, columnspan=2)
Label(count_frame, text='Enter how many numbers to display (e.g. 1000):').grid(column=0, row=2, columnspan=2)
Entry(count_frame, textvariable=display_num).grid(column=0, row=3, columnspan=2)
Button(count_frame, text='Display Numbers', command=display_nums).grid(column=0, row=4, columnspan=2)
t = Treeview(count_frame, columns=('hex', 'oct', 'bin'))
t.grid(column=0, row=5)
for i in ('Hexadecimal', 'Octal', 'Binary'):
    t.column(i[:3].lower(), width=100)
    t.heading(i[:3].lower(), text=i)
t.column('#0', width=100)
t.heading('#0', text='Decimal')
s = Scrollbar(count_frame, orient='vertical', command=t.yview)
s.grid(column=1, row=5, sticky='ns')
t['yscrollcommand'] = s.set
prefixes = BooleanVar()
Checkbutton(count_frame, text='Show Prefixes', variable=prefixes, onvalue=True, offvalue=False, command=show_nums).grid(column=0, row=6, columnspan=2)

convert_frame = Frame(n)
n.add(convert_frame, text='Converter')
convert_num = StringVar()
Label(convert_frame, text='Enter the number to convert:').grid(column=0, row=0, columnspan=2)
Entry(convert_frame, textvariable=convert_num).grid(column=0, row=1, columnspan=2)
Label(convert_frame, text='Convert from:').grid(column=0, row=2)
Label(convert_frame, text='Convert to:').grid(column=1, row=2)
convert_from = StringVar(value='Decimal')
convert_to = StringVar(value='Decimal')
c = Combobox(convert_frame, textvariable=convert_from, values=['Decimal', 'Hexadecimal', 'Octal', 'Binary'])
c.grid(column=0, row=3)
c.state(['readonly'])
c = Combobox(convert_frame, textvariable=convert_to, values=['Decimal', 'Hexadecimal', 'Octal', 'Binary'])
c.grid(column=1, row=3)
c.state(['readonly'])
result_num = StringVar()
Button(convert_frame, text='Convert', command=convert, default='active').grid(column=0, row=4, columnspan=2)
Label(convert_frame, text='Converted number:').grid(column=0, row=5, columnspan=2)
Label(convert_frame, textvariable=result_num).grid(column=0, row=6, columnspan=2)
Button(convert_frame, text='Copy', command=copy).grid(column=0, row=7, columnspan=2)
result_prefix = BooleanVar()
change_prefix = BooleanVar()
Checkbutton(convert_frame, text='Show converted number prefix', variable=result_prefix, onvalue=True, offvalue=False, command=show_converted).grid(column=0, row=8, columnspan=2)
Checkbutton(convert_frame, text='Starting number prefix changes type', variable=change_prefix, onvalue=True, offvalue=False).grid(column=0, row=9, columnspan=2)
root.mainloop()