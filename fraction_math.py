from tkinter import Button, Label, Entry, Canvas, Tk, ttk, IntVar, messagebox
from tkinter.ttk import Combobox
o = 10

root = Tk()
def oper_fractions():
    canvas = Canvas(root, width=375 + (o*2), height = 150 + (o*2), highlightthickness=3, highlightcolor='black')
    canvas.grid(column=0, row=5, columnspan=3)
    first_fraction = first_fraction_var[0].get(), first_fraction_var[1].get()
    second_fraction = second_fraction_var[0].get(), second_fraction_var[1].get()
    if first_fraction[1] == 0 or second_fraction[1] == 0:
        messagebox.showwarning(message='One or both of the fractions has a denominator equal to 0, which makes it not a fraction. Please change any denominators equal to 0.')
        return
    #Draw the first rectangle
    canvas.create_rectangle(o, o, 100 + o, 100 + o, outline='black')
    canvas.create_rectangle(o, o, 100 + o, ((100/first_fraction[1]) * first_fraction[0]) + o, fill='red')
    for i in range(first_fraction[1]):
        canvas.create_line(o, ((100/first_fraction[1]) * i) + o, 100 + o, ((100/first_fraction[1]) * i) + o)
    canvas.create_text(o, o+102, text=f'''{first_fraction[0]}
⎼⎼⎼
{first_fraction[1]}''', anchor='nw')
    canvas.create_text(o+112, o+50, text='×')
    #Draw the second rectangle
    xo = 125 + o
    canvas.create_rectangle(xo, o, 100 + xo, 100 + o, outline='black')
    canvas.create_rectangle(xo, o, ((100/second_fraction[1]) * second_fraction[0]) + xo, o+100, fill='blue')
    for i in range(second_fraction[1]):
        canvas.create_line(((100/second_fraction[1]) * i) + xo, o, ((100/second_fraction[1]) * i) + xo, o + 100)
    canvas.create_text(xo, o+102, text=f'''{second_fraction[0]}
⎼⎼⎼
{second_fraction[1]}''', anchor='nw')
    canvas.create_text(xo+112, o+50, text='=')
    #Draw the third rectangle
    xo = 125 + xo
    canvas.create_rectangle(xo, o, 100 + xo, 100 + o, outline='black')
    canvas.create_rectangle(xo, o, ((100/second_fraction[1]) * second_fraction[0]) + xo, ((100/first_fraction[1]) * first_fraction[0]) + o, fill='purple')
    for i in range(second_fraction[1]):
        canvas.create_line(((100/second_fraction[1]) * i) + xo, o, ((100/second_fraction[1]) * i) + xo, o + 100)
    for i in range(first_fraction[1]):
        canvas.create_line(xo, ((100/first_fraction[1]) * i) + o, 100 + xo, ((100/first_fraction[1]) * i) + o)
    canvas.create_text(xo, o+102, text=f'''{second_fraction[0] * first_fraction[0]}
⎼⎼⎼
{second_fraction[1] * first_fraction[1]}''', anchor='nw')
    

first_fraction_var = (IntVar(), IntVar())
Label(root, text='Enter some fractions:').grid(column=0, row=0, columnspan=3)
Entry(root, width=3, textvariable=first_fraction_var[0]).grid(column=0, row=1)
Label(root, text=' '* 75, bg='black', font=('Arial', 2)).grid(column=0, row=2)
Entry(root, width=3, textvariable=first_fraction_var[1]).grid(column=0, row=3)
second_fraction_var = (IntVar(), IntVar())
Entry(root, width=3, textvariable=second_fraction_var[0]).grid(column=2, row=1)
Label(root, text=' '* 75, bg='black', font=('Arial', 2)).grid(column=2, row=2)
Entry(root, width=3, textvariable=second_fraction_var[1]).grid(column=2, row=3)
Button(root, text='Solve', command=oper_fractions).grid(column=0, row=4, columnspan=3)
canvas = Canvas(root, width=375 + (o*2), height = 150 + (o*2), highlightthickness=3, highlightcolor='black')
canvas.grid(column=0, row=5, columnspan=3)
root.mainloop()