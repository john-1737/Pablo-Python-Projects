import tkinter as tk
from tkinter import ttk, messagebox

#B stands for bits.
B = 4

def bin_positive(dec=0):
    binstr = ['' for i in range(B)]
    for i in range(B):
        highest_spot = 2 ** (B - i - 1)
        if dec >= highest_spot:
            binstr[i] = '1'
            dec -= highest_spot
        else:
            binstr[i] = '0'
    return ''.join(binstr)

def bin_anything(dec=0):
    if dec > 0:
        return bin_positive(dec)
    else:
        dec = bin_positive(abs(dec))
        dec = dec.replace('0', 'i').replace('1', '0').replace('i', '1') #Switch 1s and 0s.
        return add(dec, '0001')

def bin_to_dec(bina):
    dec = 0
    for i in range(1, B + 1):
        if bina[-i] == 1:
            dec += (2 ** (i-1)) 
            

def add(num1='0000', num2='0000'):
    carry = False
    num1, num2 = list(num1)[::-1], list(num2)[::-1]
    answer = []
    for i in range(len(num1)):
        place_answer = 0
        if num1[i] == num2[i]:
            if carry:
                answer.append('1')
            else:
                answer.append('0')
            if num1[i]=='1':
                carry = True
            else:
                carry = False
        else:
            if carry:
                answer.append('0')
                carry = True
            else:
                answer.append('1')
    answer.reverse()
    return ''.join(answer).zfill(4)

def subtract(num1='0000', num2='0000'):
    
    num2 = add(num2[::-1], '0001')
    return add(num1, num2)

def calculate():
    num1, num2 = num1_var.get().zfill(4), num2_var.get().zfill(4)
    if len(num1) >= 4 or len(num2) >= 4:
        messagebox.showinfo('Both numbers must be less than 4 characters.')

def ask_number():
    while True:
        string = input('Enter a number: ')
        if string.strip('-').isdigit() and abs(int(string)) < 2 ** B:
            return int(string)
        print('Invalid')
    
'''root = tk.Tk()
root.title('Binary Calculator')
num1_var = tk.StringVar()
num1_entry = tk.Entry(root, textvariable=num1_var, width=17)
num1_entry.grid(column=1, row=0)
num2_var = tk.StringVar()
num2_entry = tk.Entry(root, textvariable=num2_var, width=17)
num2_entry.grid(column=1, row=1)
opertype_var = tk.StringVar()
opertype_box = ttk.Combobox(root, textvariable=opertype_var, values=('+', '-'), width=2)
opertype_box.state(['readonly'])
opertype_box.grid(column=0, row=1)
ttk.Separator(root, orient='horizontal').grid(column=0, row=2, columnspan=2)
answer = tk.StringVar()
tk.Label(root, textvariable=answer).grid(column=1, row=3)
tk.Button(root, text='Calculate').grid(column=1, row=4)
root.mainloop()'''
print(add('00000010', '11111110'))