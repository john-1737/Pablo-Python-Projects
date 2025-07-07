from tkinter import Entry, Label, Text, Button, simpledialog, messagebox, IntVar, StringVar, Tk
from sys import exit

while True:
    num1 = simpledialog.askinteger('Enter divisor', 'Enter the divisor')
    if num1 > 99:
        messagebox.showwarning(message='Must be less than 100')
    elif num1 == None:
        exit()
    else:
        break
while True:
    num2 = simpledialog.askinteger('Enter dividend', 'Enter the dividend')
    if num2 > 99:
        messagebox.showwarning(message='Must be less than 100')
    elif num2 < num1:
        messagebox.showwarning(message='Must be less than divisor')
    elif num2 == None:
        exit()
    else:
        break

def check_answer():
    global pos
    if num2 // num1 == answer_var.get():
        if pos == 1:
            answer['command'] = 'disabled'
        else:
            pos += 1
            t.delete('1.0', '1.8')
            t.insert('1.3', '   ' + str(answer_var.get()) + (chr(9608)))
    else:
        pass

root = Tk()
answer_var = IntVar()
Label(root, text = f'Try out some numbers to replace the block {chr(9608)}').pack()
Entry(root, textvariable=answer_var).pack()
pos = len(str(num2 // num1)) - 1
answer = Button(root, text='Check Answer', command=check_answer)
answer.pack()
t = Text(root,width=9, height=7)
t.pack()
t.insert('1.0', (((' ' * 9) + '\n') * 6).rstrip('\n'))
t.insert('1.3', (chr(9608) * len(str(num2 // num1))) + '\n')
t.insert('2.0','''  /--
{}|{}'''.format(num1, num2).replace('/', chr(0x250c)).replace('-', chr(0x2500)).replace('|', chr(0x2502)))
root.mainloop()