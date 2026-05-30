from tkinter import Tk, StringVar, Button
from tkinter.ttk import Frame, Label, Notebook
from math import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, asinh, acosh, atanh, log10, e, pi, floor, ceil
keys = (('C', '+/-', '%', '+'),
tuple('789−'),
tuple('456×'),
tuple('123÷'))
opertype = ''
num1, num2 = '', ''

def solve(num1, num2, opertype):
    try:
        n1, n2 = float(num2), float(num1)
        opertype = {'÷':'/','×':'*','−':'-','+':'+'}[opertype]
        try:
            display.set(eval(f'{n2}{opertype}{n1}'))
        except ZeroDivisionError:
            display.set('Can\'t divide by 0')
    except:
        pass



def respond(key):
    global num1, num2, opertype
    try:
        if key == 'C':
            num1 = ''
            num2 = ''
        elif key == '%':
            num1 = str(float(num1) / 100)
        elif key == '+/-':
            num1 = str(-(float(num1)))
        elif key in '+−×÷':
            opertype = key
            num1, num2 = '', num1
        elif key == '.':
            if '.' not in num1:
                num1 += '.'
        else:
            num1 += key
    except:
        pass
    display.set(num1)


root = Tk()
n = Notebook(root)
n.grid(sticky='nwes')
normal = Frame(n)
n.add(normal, text='Normal')
scientific = Frame(n)
n.add(scientific, text='Scientific')
display = StringVar()
Label(normal, textvariable=display).grid(column=0, row=0, columnspan=4)
for y, i in enumerate(keys, start=1):
    for x, j in enumerate(i):
        Button(normal, text=j, width=3, height=3, command=lambda key=j:respond(key)).grid(column=x, row=y)
Button(normal, text='=', width=10, height=3, command=lambda: solve(num1, num2, opertype)).grid(column=0, row=5, columnspan=3)
Button(normal, text='.', width=3, height=3, command=lambda : respond('.')).grid(column=3, row=5)
Label(scientific, textvariable=display).grid(column=0, row=0, columnspan=4)
for y, i in enumerate(keys, start=1):
    for x, j in enumerate(i):
        Button(scientific, text=j, width=3, height=3, command=lambda key=j:respond(key)).grid(column=x, row=y)
Button(scientific, text='=', width=10, height=3, command=lambda: solve(num1, num2, opertype)).grid(column=0, row=5, columnspan=3)
Button(scientific, text='.', width=3, height=3, command=lambda : respond('.')).grid(column=3, row=5)
Button(scientific, text='sin')
root.mainloop()