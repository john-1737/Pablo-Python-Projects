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
        display.set(eval(f'{n2}{opertype}{n1}'))
    except ZeroDivisionError:
        display.set('Can\'t divide by 0')



def respond(key):
    global num1, num2, opertype
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
    display.set(num1)

root = Tk()
display = StringVar()
Label(root, textvariable=display).grid(column=0, row=0, columnspan=4)
for y, i in enumerate(keys, start=1):
    for x, j in enumerate(i):
        Button(root, text=j, width=3, height=3, command=lambda key=j:respond(key)).grid(column=x, row=y)
Button(root, text='=', width=10, height=3, command=lambda: solve(num1, num2, opertype)).grid(column=0, row=5, columnspan=3)
Button(root, text='.', width=3, height=3, command=lambda : respond('.')).grid(column=3, row=5)
root.mainloop()