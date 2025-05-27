#Long multiplication
from tkinter import Tk, Text, Button, Entry, IntVar, Label, RIGHT
multiplied_nums = []

def standard_solve():
    t['state'] = 'normal'
    t.insert('end', str(num1.get()) + '\n', 'right')
    t.insert('end', str(num2.get()) + '\n', 'right')
    t.insert('end', '---------------' + '\n', 'right')    
    multiplied_nums = []
    for i, j in enumerate(reversed(list(str(num2.get())))):
        num3 = num1.get() * int(j)
        multiplied_nums.append(num3 * (10 ** i))
        t.insert('end', str(num3) + ' '* i, 'right')
        t.insert('end', '\n', 'right')
    t.insert('end', '---------------' + '\n', 'right')
    t.insert('end', str(sum(multiplied_nums)), 'right')
    t['state'] = 'disabled'

tk = Tk()
num1 = IntVar()
num2 = IntVar()
Entry(tk, textvariable=num1).grid(column=1, row=0)
Entry(tk, textvariable=num2).grid(column=1, row=1)
Label(tk, text='×').grid(column=0, row=1)
Label(tk, bg='black', text=' ' * 700, font=('Arial', 1)).grid(column=0, row=2, columnspan=2)
t = Text(tk, state='disabled')
t.grid(column=0, row=3, columnspan=2)
t.tag_configure('right', justify=RIGHT)
Button(tk, text='Solve', command=standard_solve).grid(column=0, row=4, columnspan=2)
tk.mainloop()