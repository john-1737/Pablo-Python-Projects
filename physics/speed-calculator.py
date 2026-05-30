from tkinter import Tk, ttk, StringVar, IntVar
from tkinter.ttk import Combobox, Entry, Label, Frame, Button
CONVERSIONS = {('cm', 'm') : 100, ('m', 'km') : 1000, ('m', 'cm') : 1/100, ('km', 'm') : 1/1000, ('s', 'min') : 60, ('min', 'h') : 60, ('min', 's') : 1/60, ('h', 'min') : 1/60}
def change_units(box):
    if box == 1:
        val = entry1.get()
        val2 = entry2.get()
        b = vbox1
        bval = ventry1
    else:
        val = entry2.get()
        val2 = entry1.get()
        b = vbox2
        bval = ventry2
    if val == 'Distance':
        b.config(values=['km', 'm', 'cm'])
        bval.set('km')
    elif val == 'Speed':
        b.config(values=['km/h', 'm/h', 'cm/h', 'km/min', 'm/min', 'cm/min', 'km/s', 'm/s', 'cm/s'])
        bval.set('km/h')
    elif val == 'Time':
        b.config(values=['h', 'min', 's'])
        bval.set('h')
    """if val == val2:
        entry3.set('ERROR: Selected inputs cannot be equal.')
    elif val == 'Distance' and val2 == 'Speed') or:
        entry3.set('Time')"""
    
def calculate():
    given1 = entry1.get()
    given2 = entry2.get()
    unit1 = ventry1.get()
    unit2 = ventry2.get()
    val1 = value1.get()
    val2 = value2.get()
    values = []
    for i, j, k in ((unit1, given1, val1), (unit2, given2, val2)):
        if j == 'Distance':
            if i == 'm':
                values.append(k)
                continue
            values.append(k * CONVERSIONS[i, 'm'])
        elif j == 'Time':
            if i == 'min':
                values.append(k)
                continue
            values.append(k * CONVERSIONS[i, 'min'])
        else:
            if i == 'm/min':
                values.append(k)
                continue
            l, m = i.split('/')
            values.append((k * float(CONVERSIONS[l, 'm'])) / (1 * float(CONVERSIONS[m, 'min'])))
    if given1 == 'Speed':
        given1, unit1, val1, given2, unit2, val2 = given2, unit2, val2, given1, unit1, val1
    if given1 == 'Time' and given2 == 'Distance':
        given1, unit1, val1, given2, unit2, val2 = given2, unit2, val2, given1, unit1, val1
    if given1 == 'Distance':
        if given2 == 'Speed':
            val3.set(val1/val2)
        elif given2 == 'Time':
            val3.set(val1/val2)
    elif given1 == 'Time':
        val3.set(val1*val2)

root = Tk()
main = Frame(root)
main.grid(sticky='nwes')
entry1 = StringVar(value='Distance')
c = Combobox(main, values=['Distance', 'Speed', 'Time'], textvariable=entry1, width=17)
c.grid(column=0, row=0, columnspan=2)
c.bind('<<ComboboxSelected>>', lambda e: change_units(1))
c.state(['readonly'])
entry2 = StringVar(value='Speed')
c = Combobox(main, values=['Distance', 'Speed', 'Time'], textvariable=entry2, width=17)
c.grid(column=2, row=0, columnspan=2)
c.bind('<<ComboboxSelected>>', lambda e: change_units(2))
c.state(['readonly'])
ventry1 = StringVar(value='km')
vbox1 = Combobox(main, values=['km', 'm', 'cm'], width=5, textvariable=ventry1)
vbox1.grid(column=1, row=1)
vbox1.state(['readonly'])
ventry2 = StringVar(value='km/h')
vbox2 = Combobox(main, values=['km/h', 'm/h', 'cm/h', 'km/min', 'm/min', 'cm/min', 'km/s', 'm/s', 'cm/s'], width=5, textvariable=ventry2)
vbox2.grid(column=3, row=1)
vbox2.state(['readonly'])
value1, value2 = IntVar(), IntVar()
Entry(main, textvariable=value1, width=10).grid(column=0, row=1)
Entry(main, textvariable=value2, width=10).grid(column=2, row=1)
entry3 = StringVar(value='Time:')
Label(main, textvariable=entry3).grid(column=0, row=2, columnspan=4)
val3 = StringVar()
Label(main, textvariable=val3).grid(column=0, row=4, columnspan=3)
b = Button(main, default='active', command=calculate, text='Calculate').grid(column=0, row=5, columnspan=4)
root.mainloop()