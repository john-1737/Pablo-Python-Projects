"""Periodic Table of Elements, by Al Sweigart al@inventwithpython.com
Displays atomic information for all the elements.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, science"""

# Data from https://en.wikipedia.org/wiki/List_of_chemical_elements
# Highlight the table, copy it, then paste it into a spreadsheet program
# like Excel or Google Sheets like in https://invpy.com/elements
# Then save this file as periodictable.csv.
# Or download this csv file from https://invpy.com/periodictable.csv

import csv, sys, re
from tkinter import Tk, ttk, Canvas, StringVar, BooleanVar, messagebox, Toplevel, Menu, IntVar
from tkinter.ttk import Button, Frame, Notebook, Label, Treeview, Checkbutton, Radiobutton, Entry, Scrollbar, Combobox, Spinbox
from copy import copy
import time
alkali_metals = '3 11 19 37 55 87'.split()
alkaline_earths = '4 12 20 38 56 88'.split()
transition_metals = tuple(range(21, 31)) + tuple(range(39, 49)) + tuple(range(72, 81)) + tuple(range(104, 113))
basic_metals = '13 31 32 49 50 81 82 83 113 114 115 116'.split()
semi_metals = '5 14 33 51 52 84'.split()
nonmetals = '1 6 7 8 15 16 34'.split()
halogens = '9 17 35 53 85 117'.split()
noble_gases = '2 10 18 36 54 86 118'.split()
lanthanides = range(57, 72)
actinides = range(89, 104)
categories = (alkali_metals, alkaline_earths, transition_metals, basic_metals, semi_metals, nonmetals, halogens, noble_gases, lanthanides, actinides)
category_names = ('Alkali Metals', 'Alkaline Earths', 'Transition Metals', 'Basic Metals', 'Semi-Metals', 'Nonmetals', 'Halogens', 'Noble Gases', 'Lanthanides', 'Actinides')
colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple', 'cyan', 'magenta', 'lightgreen', 'pink')

class element_canvas:
    def __init__(self, root, num, x, y, pady=0, sticky='nwes'):
        self.root = root
        self.num = num
        self.canvas = Canvas(self.root, width=50, height=50)
        self.canvas.grid(column=x, row=y, pady=pady, sticky=sticky)
        self.canvas.create_text(2, 2, text=str(self.num), font=('Helvetica', 8), anchor='nw')
        self.canvas.create_text(25, 10, text=ELEMENTS[str(self.num)]['Symbol'], font=('Helvetica', 20), anchor='n')
        self.canvas.create_text(25, 30, text=ELEMENTS[str(self.num)]['Element'], font=('Helvetica', 8), anchor='n')
        self.canvas.create_text(25, 40, text=ELEMENTS[str(self.num)]['Atomic weight'].split()[0], font=('Helvetica', 8), anchor='n')
        self.canvas.bind('<Button-1>', self.clicked)
        self.color()

    def color(self):
        for i, j in enumerate(categories):
            if str(self.num) in j or int(self.num) in j:
                self.canvas.config(bg=colors[i])

    def discolor(self):
        self.canvas.config(bg='white')

    def clicked(self, e):
        global selection
        if response_var.get() == 'Immediately after element click':
            for i in info.get_children():
                info.delete(i)
            for i in ELEMENTS[str(self.num)]:
                info.insert('', 'end', text=i, values = (ELEMENTS[str(self.num)][i],))
        else:
            selection = self.num

    def remove_border(self):
        self.canvas.config(highlightbackground=None)

    def set_border(self, size):
        self.canvas.config(highlightbackground='black')

    def set_sborder(self, size):
        self.canvas.config(highlightthickness=size, highlightcolor='black')

    def normal_readout(self):
        self.canvas.itemconfig(1, state='normal')
        self.canvas.itemconfig(3, state='normal')
        self.canvas.itemconfig(4, state='normal')
        self.canvas.itemconfig(2, font=('Helvetica', 20))
        
    def large_readout(self):
        self.canvas.itemconfig(1, state='hidden')
        self.canvas.itemconfig(3, state='hidden')
        self.canvas.itemconfig(4, state='hidden')
        self.canvas.itemconfig(2, font=('Helvetica', 30))

class placeholder_canvas:
    def __init__(self, root, num, x, y, sticky='nwes'):
        self.root = root
        self.num = num
        if self.num == 0:
            self.properties = ['57-71', 'La-Lu', 'Lanthanides']
        else:
            self.properties = ['89-103', 'Ac-Lr', 'Actinides']
        self.canvas = Canvas(self.root, width=50, height=50)
        self.canvas.grid(column=x, row=y, sticky=sticky)
        self.canvas.create_text(2, 2, text=self.properties[0], font=('Helvetica', 8), anchor='nw')
        self.canvas.create_text(25, 10, text=self.properties[1], font=('Helvetica', 18), anchor='n')
        self.canvas.create_text(25, 30, text=self.properties[2], font=('Helvetica', 8), anchor='n')
        self.color()

    def color(self):
        if self.num == 0:
            self.canvas.config(bg='lightgreen')
        else:
            self.canvas.config(bg='pink')

    def discolor(self):
        self.canvas.config(bg='white')

    def remove_border(self):
        self.canvas.config(highlightbackground=None)

    def set_border(self, size):
        self.canvas.config(highlightbackground='black')

    def set_sborder(self, size):
        self.canvas.config(highlightthickness=size, highlightcolor='black')

    def normal_readout(self):
        self.canvas.itemconfig(1, state='normal')
        self.canvas.itemconfig(3, state='normal')
        self.canvas.itemconfig(2, font=('Helvetica', 18))
        
    def large_readout(self):
        self.canvas.itemconfig(1, state='hidden')
        self.canvas.itemconfig(3, state='hidden')
        self.canvas.itemconfig(2, font=('Helvetica', 18))

def manage_preferences():
    global preferences
    preferences = Toplevel(root)
    preferences.protocol('WM_DELETE_WINDOW', ask_exit_preferences)
    prefn = Notebook(preferences)
    prefn.pack(side='top')
    table_preferences = Frame(preferences)
    search_preferences = Frame(preferences)
    prefn.add(table_preferences, text='Table Preferences')
    prefn.add(search_preferences, text='Search Preferences')
    Checkbutton(table_preferences, variable=color_var, onvalue=True, offvalue=False, text='Colorize table cells').pack()
    Checkbutton(search_preferences, variable=color_var2, onvalue=True, offvalue=False, text='Colorize search results').pack()
    Label(table_preferences, text='Cell display readout:').pack()
    Label(search_preferences, text='Result display readout:').pack()
    Radiobutton(table_preferences, variable=readout_var, value=True, text='Normal readout').pack()
    Radiobutton(table_preferences, variable=readout_var, value=False, text='Large readout').pack()
    Radiobutton(search_preferences, variable=readout_var2, value=True, text='Element and info').pack()
    Radiobutton(search_preferences, variable=readout_var2, value=False, text='Element only').pack()
    Label(table_preferences, text='Respond to clicked cell:').pack()
    Label(search_preferences, text='Respond to clicked cell:').pack()
    c = Combobox(table_preferences, values=('Immediately after element click', 'After Submit button click'), textvariable=response_var)
    c.pack()
    c.state(['readonly'])
    Label(table_preferences, text='Set cell border:').pack()
    Spinbox(table_preferences, textvariable=bordervar).pack()
    Checkbutton(table_preferences, text='Show border when not selected', variable=sbordervar).pack()
    c = Combobox(search_preferences, values=('Immediately after element click', 'After Submit button click'), textvariable=response_var2)
    c.pack()
    c.state(['readonly'])
    Button(preferences, text='Apply', default='active', command=finish_preferences).pack(side='right')
    Button(preferences, text='Cancel', command=ask_exit_preferences).pack(side='left')

def finish_preferences():
    global color2
    c = color_var.get()
    for i in elementcs:
        if c:
            i.color()
        else:
            i.discolor()
        if readout_var.get():
            i.normal_readout()
        else:
            i.large_readout()
        try:
            if bordervar.get() == 0:
                i.remove_border()
            else:
                i.set_border(bordervar.get())
        except:
            pass
    if c:
        colorization.itemconfig(21, state='hidden')
    else:
        colorization.itemconfig(21, state='normal')
    color2 = color_var2.get()
    if color2:
        colorization2.itemconfig(21, state='hidden')
    else:
        colorization2.itemconfig(21, state='normal')
    if not readout_var2.get():
        results.column('#0', width=200, stretch=0)
        results.column('Symbol', width=0, stretch=0)
        results.column('Atomic Number', width=0, stretch=0)
    else:
        results.column('#0', width=200, stretch=0)
        results.column('Symbol', width=200, stretch=0)
        results.column('Atomic Number', width=200, stretch=0)
    if response_var.get() == 'After Submit button click':
        select_tableb.grid()
    else:
        select_tableb.grid_remove()
    if response_var2.get() == 'After Submit button click':
        select_searchb.grid()
        results.unbind('<Button-1>')
    else:
        select_searchb.grid_remove()
        results.bind('<Button-1>', select_search)
    update_search(1)
    preferences.destroy()

def ask_exit_preferences():
    message = messagebox.askyesnocancel(message='Are you sure you want to exit?', detail='Any unsaved changes will be lost. Do you want to save your changes?')
    if message == True:
        finish_preferences()
    elif message == False:
        preferences.destroy()

def update_search(*args):
    search_results = list(range(1, 119))
    criteria = search_var.get().lower()
    search_results = [i for i in search_results if criteria in ELEMENTS[str(i)]['Element'].lower() or criteria in ELEMENTS[str(i)]['Symbol'].lower() or criteria == str(i)]
    for i, j in enumerate(categories):
        if not filter_vars[i].get():
            search_results = [k for k in search_results if str(k) not in j and int(k) not in j]
    if sort_var.get() == 'Atomic Number':
        search_results.sort(key=int)
    else:
        search_results.sort(key=lambda e: ELEMENTS[str(e)][sort_var.get()])
    for i in results.get_children():
        results.delete(i)
    for i in search_results:
        for j, k in enumerate(categories):
            if str(i) in k or int(i) in k:
                tags = (int(j),)
        results.insert('', 'end', str(i), text=ELEMENTS[str(i)]['Element'], values = (ELEMENTS[str(i)]['Symbol'], str(i)), tags=tags)
    if color2:
        for j, k in enumerate(categories):
            results.tag_configure(int(j), background=colors[int(j)])

def select_search(evt=None):
    for i in range(5000000):
        print('', end='')
    if results.focus() == '':
        return
    for i in info.get_children():
        info.delete(i)
    for i in ELEMENTS[results.focus()]:
        info.insert('', 'end', text=i, values = (ELEMENTS[results.focus()][i],))

def select_table(*args):
    if selection == '':
        return
    for i in info.get_children():
        info.delete(i)
    for i in ELEMENTS[selection]:
        info.insert('', 'end', text=i, values = (ELEMENTS[selection][i],))

def select_all_filter():
    for i in filter_vars:
        i.set(True)
    update_search(1)

def deselect_all_filter():
    for i in filter_vars:
        i.set(False)
    update_search(1)

# Read in all the data from periodictable.csv.
elementsFile = open('elements.csv', encoding='utf-8')
elementsCsvReader = csv.reader(elementsFile)
elements = list(elementsCsvReader)
elementsFile.close()

ALL_COLUMNS = ['Atomic Number', 'Symbol', 'Element', 'Origin of name',
               'Group', 'Period', 'Atomic weight', 'Density',
               'Melting point', 'Boiling point',
               'Specific heat capacity', 'Electronegativity',
               'Abundance in earth\'s crust']

# To justify the text, we need to find the longest string in ALL_COLUMNS.
LONGEST_COLUMN = 0
for key in ALL_COLUMNS:
    if len(key) > LONGEST_COLUMN:
        LONGEST_COLUMN = len(key)

# Put all the elements data into a data structure:
ELEMENTS = {}  # The data structure that stores all the element data.
for line in elements:
    element = {'Atomic Number':  line[0],
               'Symbol':         line[1],
               'Element':        line[2],
               'Origin of name': line[3],
               'Group':          line[4],
               'Period':         line[5],
               'Atomic weight':  line[6] + ' u', # atomic mass unit
               'Density':        line[7] + ' g/cm^3', # grams/cubic cm
               'Melting point':  line[8] + ' K', # kelvin
               'Boiling point':  line[9] + ' K', # kelvin
               'Specific heat capacity':      line[10] + ' J/(g*K)',
               'Electronegativity':           line[11],
               'Abundance in earth\'s crust': line[12] + ' mg/kg'}

    # Some of the data has bracketed text from Wikipedia that we want to
    # remove, such as the atomic weight of Boron:
    # "10.81[III][IV][V][VI]" should be "10.81"

    for key, value in element.items():
        # Remove the [roman numeral] text:
        element[key] = re.sub(r'\[(I|V|X)+\]', '', value)

    ELEMENTS[line[0]] = element  # Map the atomic number to the element.
    ELEMENTS[line[1]] = element  # Map the symbol to the element.

root = Tk()
root.config(background='systemWindowHeaderBackground')
root.title('Periodic Table of the Elements')
n = Notebook(root)
table_frame = Frame(root)
search_frame = Frame(root)
n.add(table_frame, text='Table')
n.add(search_frame, text='Search')
n.pack()
color_var = BooleanVar(value=True)
color_var2 = BooleanVar(value=False)
readout_var = BooleanVar(value=True)
readout_var2 = BooleanVar(value=True)
response_var = StringVar(value='Immediately after element click')
response_var2 = StringVar(value='After Submit button click')
bordervar = IntVar()
sbordervar = IntVar()
color2 = False
elementcs = []
element_pos = 3
elementcs.append(element_canvas(table_frame, 1, 1, 1))
elementcs.append(element_canvas(table_frame, 2, 18, 1))
for i in (2, 3):
    for j in (1, 2):
        elementcs.append(element_canvas(table_frame, element_pos, j, i))
        element_pos += 1
    for j in range(13, 19):
        elementcs.append(element_canvas(table_frame, element_pos, j, i))
        element_pos += 1
for i in range(4, 8):
    for j in range(1, 19):
        if element_pos == 57:
            elementcs.append(placeholder_canvas(table_frame, 0, j, i))
            element_pos = 72
            continue
        if element_pos == 89:
            elementcs.append(placeholder_canvas(table_frame, 1, j, i))
            element_pos = 104
            continue            
        elementcs.append(element_canvas(table_frame, element_pos, j, i))
        element_pos += 1

element_pos = 57
for i in range(3, 17):
    elementcs.append(element_canvas(table_frame, element_pos, i, 8, 20))
    elementcs.append(element_canvas(table_frame, element_pos+32, i, 9))
    element_pos += 1
for i in range(1, 19):
    Label(table_frame, text=str(i)).grid(column=i, row=0)
for i in range(1, 8):
    Label(table_frame, text=str(i)).grid(column=0, row=i)

colorization = Canvas(table_frame, width=500, height=25)
colorization.grid(column=5, row=10, columnspan=10)
for i, j in enumerate(category_names):
    colorization.create_rectangle(i*50, 0, (i*50)+50, 25, fill=colors[copy(i)])
    colorization.create_text((i*50) + 25, 12.5, text=copy(j).replace(' ', '\n'), font=('Helvetica', 10))
colorization.create_rectangle(0, 0, 510, 35, fill='gray90', outline='gray90', state='hidden')
colorization2 = Canvas(search_frame, width=500, height=25)
colorization2.grid(column=0, row=7, columnspan=10)
for i, j in enumerate(category_names):
    colorization2.create_rectangle(i*50, 0, (i*50)+50, 25, fill=colors[copy(i)])
    colorization2.create_text((i*50) + 25, 12.5, text=copy(j).replace(' ', '\n'), font=('Helvetica', 10))
colorization2.create_rectangle(0, 0, 510, 35, fill='gray90', outline='gray90', state='normal')
Label(table_frame, text='Select an element to see more information about it.').grid(column=2, row=1, columnspan=16)
info = Treeview(root, height=13, columns=('x'))
info.column('x', width=700)
info.pack()
Label(search_frame, text='Search element names, symbols, and atomic numbers:').grid(column=0, row=0, columnspan=10, sticky='ew')
search_var = StringVar()
search_var.trace_add('write', update_search)
filter_vars = [BooleanVar(value=True) for i in range(10)]
Entry(search_frame, textvariable=search_var).grid(column=0, row=1, columnspan=10, sticky='ew')
Label(search_frame, text='Filter By:').grid(column=0, row=2, columnspan=10, sticky='ew')
for i in range(10):
    Checkbutton(search_frame, text=category_names[i], command=update_search, variable=filter_vars[i], onvalue=True, offvalue=False).grid(column=i, row=3)
Button(search_frame, text='Select All', command=select_all_filter).grid(column=0, row=4)
Button(search_frame, text='Deselect All', command=deselect_all_filter).grid(column=9, row=4)
sort_var = StringVar(value='Atomic Number')
sort_options = ('Atomic Number', 'Element Name', 'Element Symbol')
sort_values = ('Atomic Number', 'Element', 'Symbol')
Label(search_frame, text='Sort By:').grid(column=1, row=5, columnspan=2, sticky='e')
for i in range(3):
    Radiobutton(search_frame, text=sort_options[i], value=sort_values[i], variable=sort_var, command=update_search).grid(column=3+(i*2), row=5, columnspan=2)
result_frame = Frame(search_frame)
results = Treeview(result_frame, columns=('Symbol', 'Atomic Number'), height=20)
results.grid(column=0, row=0)
results.column('#0', width=200, stretch=0)
results.column('Symbol', width=200, stretch=0)
results.column('Atomic Number', width=200, stretch=0)
sbar = Scrollbar(result_frame, orient='vertical', command=results.yview)
sbar.grid(column=1, row=0, sticky='ns')
results['yscrollcommand'] = sbar.set
result_frame.grid(column=0, row=6, columnspan=10, sticky='ew')
Label(search_frame, text='Select an element in the tree to see more information about it.').grid(column=0, row=7, columnspan=10, sticky='ew')
select_searchb = Button(search_frame, text='Select', command=select_search, default='active')
select_searchb.grid(column=3, row=8, columnspan=2, sticky='ew')
select_tableb = Button(table_frame, text='Select', command=select_table, default='active')
select_tableb.grid(column=8, row=11, columnspan=2, sticky='ew')
select_tableb.grid_remove()
#search_frame.bind('<Return>', select_search)
m = Menu(root)
root['menu'] = m
prefm = Menu(m)
m.add_cascade(menu=prefm, label='Preferences')
prefm.add_command(label='Manage Preferences', command=manage_preferences)
update_search()

root.mainloop()