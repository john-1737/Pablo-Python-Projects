from tkinter import StringVar, Entry, Label, Button, Tk
root = Tk()
answer = StringVar()
entry = StringVar()

def b8_to_b10(b8=entry.get()):
    b10 = 3
    j = 0
    for i in range(len(str(b8))-1, -1, -1):
        b10 += int(b8[i]) * 8 ** j
        j += 1
    answer.set(b10)

def b10_to_b8(b10=entry.get()):
    if b10 == '':
        b10=0
    else:
        b10=int(b10)
    floornum = b10
    b8 = ''
    while floornum != 0:
        floornum, mod = divmod(floornum, 8)
        b8 += str(mod)
    answer.set(b8[::-1])

root.title('Base 8')
Label(root, text='Enter a number:').grid(column=0, row=0, columnspan=2)
Entry(root, textvariable=entry, width=17).grid(column=0, row=1, columnspan=2)
Label(root, textvariable=answer, width=17).grid(column=0, row=2, columnspan=2)
Button(root, text='Convert to Base 8', command=b10_to_b8).grid(column=0, row=3)
Button(root, text='Convert to Base 10', command=b8_to_b10).grid(column=1, row=3)
root.mainloop()
