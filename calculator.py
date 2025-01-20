from tkinter import Tk, Button, Label, StringVar
keys = (('C', '+/-', '%', '+'),
tuple('789−'),
tuple('456×'),
tuple('123÷'))
opertype = ''
num1, num2 = '', ''

def solve(num1, num2, opertype):
    n1, n2 = float(num2), float(num1)
    opertype = {'÷':'/','×':'*','−':'-','+':'+'}[opertype]
    try:
        display.set(eval(f'{n1}{opertype}{n2}'))
    except ZeroDivisionError:
        display.set('Can\'t divide by 0')

def set_opertype(opertype_):
    opertype = opertype_
    num1, num2 = '', num1

def respond(key):
    if key == 'C':
        num1 = ''
        num2 = ''
    elif key == '%':
        num1 = str(int(num1) / 100)
    elif key == '+/-':
        num1 = str(-(int(num1)))
    elif key in '+−×÷':
        opertype = key
    else:
        num1 += key
    display.set(num1)

root = Tk()
display = StringVar()
Label(root, textvariable=display).grid(column=0, row=0, columnspan=4)
for y, i in enumerate(keys, start=1):
    for x, j in enumerate(i):
        Button(root, text=j, width=3, height=3, command=lambda key=j:respond(key)).grid(column=x, row=y)
root.mainloop()