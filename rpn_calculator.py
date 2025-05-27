from tkinter import *
from tkinter import messagebox
root = Tk()
nums = ['']
store_mode = False
sel_pos = 0
root.title('RPN calculator')
screen = StringVar()
def solve(nums, ope):
    num1 = nums.pop()
    try:
        num2 = nums.pop()
        nums.append(eval(f'{num1}{ope}{num2}'))
    except:
        nums.append(num1)
    return nums

def respond(key):
    global nums, store_mode, sel_pos
    if key == 'C':
        if messagebox.askyesno(message='Are you sure?\nThis action will clear the entire equation.'):
            nums = ['']
    elif key in '+−×÷':
        nums = solve(nums, key)
    else:
        if store_mode and key != '.':
            sel_pos = int(key)
            store_mode = False
        else:
            nums[-1] += key
    screen.set(nums[-1])

def save():
    nums.append('')
    screen.set(nums[-1])

def count(up):
    try:
        top_num = float(nums[-1])
    except:
        top_num = 0
    if up:
        top_num += 1
    else:
        top_num -= 1
    nums[-1] = str(top_num)
    screen.set(nums[-1])
'''def store():
    global store_mode
    with open('stored_nums.txt', 'r') as f:
        stored_nums = f.readlines()
        store_mode = True
        while True:
            if store_mode == False:
                break
        stored_nums[sel_pos + 1] = nums[-1]
    with open('stored_nums.txt', 'w') as f:
        f.write('\n'.join(stored_nums))'''

Label(root, textvariable=screen).grid(column=0, row=0, columnspan=4)
keys = (tuple('123÷'),
tuple('456×'),
tuple('789−'),
tuple('0.C+'))
key_shortcuts = (('1', '2', '3', '/'),
('4', '5', '6', '*'),
('7', '8', '9', '-'),
('0', '.', 'Delete', '+'))
for i,j in enumerate(keys, start=1):
    for k, l in enumerate(j):
        Button(root, text=l, command=lambda key=l:respond(key)).grid(column=k, row=i)
Button(root, text='enter', command=save).grid(column=0, row=5, columnspan=2)
Button(root, text='?', command=lambda:messagebox.showinfo(message='''A RPN calculator differs from a regular calculator because the operator comes after the operands(numbers).
For example, the equation 1 + 2 can be done by pressing 1, Enter, 2, and + in that order.
The equation 1 + 2 × 3 can be done by pressing the keys 1, Enter, 2, Enter, 3, × and + in that order.''')).grid(column=2, row=5, columnspan=2)
Button(root, text='View Storage', command=lambda: messagebox.showinfo(message='\n'.join(reversed(nums)))).grid(column=0, row=6, columnspan=4)
Button(root, text='Σ+', command=lambda:count(True)).grid(column=0, row=7, columnspan=2)
Button(root, text='Σ−', command=lambda:count(False)).grid(column=2, row=7, columnspan=2)
root.mainloop()