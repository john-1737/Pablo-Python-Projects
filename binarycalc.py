import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from binarycalc2 import bin_anything

def dec_to_bin():
    dec_num = simpledialog.askinteger(title='Convert Decimal Number', prompt='Enter a decimal number to convert to binary:')
    messagebox.showinfo(message=bin_anything(dec_num))

def add(num1='0000', num2='0000'):
    num1, num2 = list(num1)[::-1], list(num2)[::-1]
    places = []
    for i, j in enumerate(num1):
        if j in ("]' "):
            j = 0
        places.append(list((int(j), int(num2[i]))))
    places.append([])
    answer = []
    for i, place in enumerate(places, start=1):
        place_answer = sum(place)
        if place_answer == 2:
            answer.append('0')
            places[i].append(1)
        elif place_answer == 3:
            answer.append('1')
            places[i].append(1)
        else:
            answer.append(str(place_answer))
        
    answer.reverse()
    return ''.join(answer)[-4:].zfill(4)

def subtract(num1='0000', num2='0000'):
    num2 = num2.replace('0', 'i').replace('1', '0').replace('i', '1') #Switch 1s and 0s.
    num2 = add(num2, '0001')
    return add(num1, ''.join(num2))

def calculate():
    num1, num2 = num1_var.get().zfill(4), num2_var.get().zfill(4)
    if len(num1) > 4 or len(num2) > 4:
        messagebox.showinfo(message='Both numbers must be less than 4 characters.', icon='warning')
        return
    if (not num1.strip('-').isdecimal()) or (not num1.strip('-').isdecimal()):
        messagebox.showinfo(message='Both numbers must be integers.', icon='warning')
        return
    if opertype_var.get() == '+':
        answer.set(add(num1, num2))
    else:
        answer.set(subtract(num1, num2))
    
root = tk.Tk()
root.title('Binary Calculator')
win = tk.Toplevel(root)
win.withdraw()
menubar = tk.Menu(win)
win['menu'] = menubar
bin_conversion = tk.Menu(menubar)
for i in range(1, 9):
    bin_conversion.add_command(label=f'{i}:{bin(i)[2:].zfill(4)}')
for i in range(1, 9):
    bin_conversion.add_command(label=f'-{i}:{subtract("0000", bin(i)[2:].zfill(4))}')
bin_conversion.add_command(label='Convert Decimal Number', command=dec_to_bin)
menubar.add_cascade(menu=bin_conversion, label='Binary Conversion')
num1_var = tk.StringVar()
num1_entry = tk.Entry(root, textvariable=num1_var, width=17)
num1_entry.grid(column=1, row=0)
num2_var = tk.StringVar()
num2_entry = tk.Entry(root, textvariable=num2_var, width=17)
num2_entry.grid(column=1, row=1)
opertype_var = tk.StringVar()
opertype_var.set('+')
opertype_box = ttk.Combobox(root, textvariable=opertype_var, values=('+', '-'), width=2)
opertype_box.state(['readonly'])
opertype_box.grid(column=0, row=1)
ttk.Separator(root, orient='horizontal').grid(column=0, row=2, columnspan=2)
answer = tk.StringVar()
tk.Label(root, textvariable=answer).grid(column=1, row=3)
tk.Button(root, text='Calculate', command=calculate).grid(column=1, row=4)
root.mainloop()