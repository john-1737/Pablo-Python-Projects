"""Water Bucket Puzzle, by Al Sweigart al@inventwithpython.com
A water pouring puzzle.
More info: https://en.wikipedia.org/wiki/Water_pouring_puzzle
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, math, puzzle"""

import sys
from tkinter import Tk, Canvas, ttk, StringVar, messagebox, Menu
from tkinter.ttk import Frame, Button, Label, Style

class bucket:
    def __init__(self, root, size, x, y, columnspan=1):
        self.root = root
        self.size = size
        self.canvas = Canvas(root, width=100, height=200)
        self.canvas.grid(column=x, row=y, columnspan=columnspan)
        self.canvas.create_line(2.5, 200-(self.size*25), 2.5, 200, fill='black', width=5, tags='water')
        self.canvas.create_line(97.5, 200-(self.size*25), 97.5, 200, fill='black', width=5, tags='water')
        self.canvas.create_line(0, 197.5, 100, 197.5, fill='black', width=5, tags='water')
        self.canvas.create_rectangle(0, 0, 100, 200-(self.size*25), fill='gray90', outline='gray90')
        for i in range(1, self.size+1):
            self.canvas.create_line(0, 200-(i*25), 20, 200-(i*25), fill='red', width=2, tags='water')
            self.canvas.create_text(10, 200-(i*25), text=str(i), fill='red', anchor='n', tags='water')
    
    def fill(self, amount):
        self.canvas.delete('water')
        self.canvas.create_rectangle(0, 200-(amount*25), 100, 200, fill='#0000ff', tags='water')
        self.canvas.create_line(2.5, 200-(self.size*25), 2.5, 200, fill='black', width=5, tags='water')
        self.canvas.create_line(97.5, 200-(self.size*25), 97.5, 200, fill='black', width=5, tags='water')
        self.canvas.create_line(0, 197.5, 100, 197.5, fill='black', width=5, tags='water')
        for i in range(1, self.size+1):
            self.canvas.create_line(0, 200-(i*25), 20, 200-(i*25), fill='red', width=2, tags='water')
            self.canvas.create_text(10, 200-(i*25), text=str(i), fill='red', anchor='n', tags='water')


GOAL = 4  # The exact amount of water to have in a bucket to win.
steps = 0  # Keep track of how many steps the player made to solve this.


# The amount of water in each bucket:
waterInBucket = {8: 0, 5: 4, 3: 0}

def pour_menu(src_b):
    global pour_buckets, src_bucket
    src_bucket = src_b
    for i in bucket_buttons:
        i.grid_remove()
    for i in pour_buttons:
        i.grid()
    pour_buckets = [8, 5, 3]
    pour_buckets.remove(src_bucket)
    pbucket1.set(pour_buckets[0])
    pbucket2.set(pour_buckets[1])
    pbucket3.set(f'Select bucket to pour bucket {src_bucket} into:')

def pour_click(button):
    pour(src_bucket, pour_buckets[button])

def pour(src_bucket, dst_bucket):
    global steps
    dstBucketSize = int(dst_bucket)
    emptySpaceInDstBucket = dstBucketSize - waterInBucket[dst_bucket]
    waterInSrcBucket = waterInBucket[src_bucket]
    amountToPour = min(emptySpaceInDstBucket, waterInSrcBucket)

    # Pour out water from this bucket:
    waterInBucket[src_bucket] -= amountToPour

    # Put the poured out water into the other bucket:
    waterInBucket[dst_bucket] += amountToPour
    steps += 1
    exit_pour_menu()

def exit_pour_menu():
    for i in pour_buttons:
        i.grid_remove()
    for i in bucket_buttons:
        i.grid()
    show_water()

def exit_goal_menu():
    for i in goal_buttons:
        i.grid_remove()
    for i in bucket_buttons:
        i.grid()

def show_water():
    bucket3.fill(waterInBucket[3])
    bucket5.fill(waterInBucket[5])
    bucket8.fill(waterInBucket[8])
    step_var.set(f'Steps: {steps}')
    goal_var.set('Try to get 4 cups of water into one of these buckets:')
    for waterAmount in waterInBucket.values():
        if waterAmount == GOAL:
            for i in bucket_buttons:
                i.grid_remove()
            for i in goal_buttons:
                i.grid()
            gsteps_var.set('Good job! You solved it in '+ str(steps) + ' steps!')
            goal_var.set('You solved the puzzle! Good job!')

def restart():
    global steps
    if messagebox.askyesno(message='Are you sure?', detail='This will destroy your progress.'):
        waterInBucket[8] = 0
        waterInBucket[5] = 0
        waterInBucket[3] = 0
        steps = 0
        show_water()
        exit_goal_menu()
        exit_pour_menu()


def fill(srcBucket):
    global steps
    # Set the amount of water to the max size.
    srcBucketSize = int(srcBucket)
    waterInBucket[srcBucket] = srcBucketSize
    steps += 1
    show_water()

def empty(srcBucket):
    global steps
    waterInBucket[srcBucket] = 0  # Set water amount to nothing.
    steps += 1
    show_water()

def equal_buckets(buckets):
    abuckets = sorted(list(waterInBucket.values()), reverse=True)
    for i, j in zip(buckets, abuckets):
        if i == None:
            continue
        if i != j:
            return False
    return True

METHOD_1 = ((fill, (3, )), (pour, (3, 5)), (fill, (3, )), (pour, (3, 5)), (empty, (5, )), (pour, (3, 5)), (fill, (3, )), (pour, (3, 5)))
METHOD_2 = ((fill, (5, )), (pour, (5, 3)), (pour, (5, 8)), (empty, (3, )), (fill, (5, )), (pour, (5, 3)), (pour, (5, 8)))
POSS_1 = ((None, 0, 3), (None, 3, 0), (None, 3, 3), (None, 5, 1), (None, 0, 1), (None, 1, 0), (None, 1, 3), (None, 4, 0))
POSS_2 = ((0, 5, 0), (0, 2, 3), (2, 0, 3), (2, 0, 0), (2, 5, 0), (2, 2, 3), (4, 0, 3))

root = Tk()
root.title('Water Bucket Puzzle')
main = Frame(root)
main.grid(sticky='nwes')
bucket8 = bucket(main, 8, 0, 2)
bucket5 = bucket(main, 5, 1, 2, 2)
bucket3 = bucket(main, 3, 3, 2)
Label(main, text='8 cups').grid(column=0, row=3)
Label(main, text='5 cups').grid(column=1, row=3, columnspan=2)
Label(main, text='3 cups').grid(column=3, row=3)
bucket_buttons = []
for i, j in enumerate(((0, 1), (1, 2), (3, 1))):
    for k, l in enumerate(('Fill', 'Empty', 'Pour'), start=4):
        func = {'Fill': fill, 'Empty': empty, 'Pour': pour_menu}[l]
        bucketval = {0:8, 1:5, 2:3}[i]
        b = Button(main, text=l, command=lambda func=func, bucketval=bucketval: func(bucketval))
        b.grid(row=k, column=j[0], columnspan=[1])
        bucket_buttons.append(b)
pour_buttons = []
pbucket1 = StringVar()
pbucket2 = StringVar()
pbucket3 = StringVar()
b = Button(main, textvariable=pbucket1, command=lambda:pour_click(0))
b.grid(column=0, row=5, columnspan=2)
pour_buttons.append(b)
b = Button(main, textvariable=pbucket2, command=lambda:pour_click(1))
b.grid(column=2, row=5, columnspan=2)
pour_buttons.append(b)
b = Button(main, text='Exit', command=exit_pour_menu)
b.grid(column=1, row=6, columnspan=2)
pour_buttons.append(b)
l = Label(main, textvariable=pbucket3)
l.grid(column=0, row=4, columnspan=4)
pour_buttons.append(l)
for i in pour_buttons:
    i.grid_remove()
goal_buttons = []
gsteps_var = StringVar()
l = Label(main, textvariable=gsteps_var)
l.grid(column=0, row=4, columnspan=4)
goal_buttons.append(l)
l = Label(main, text='Press Continue to keep going,\n or press Restart to restart the game.')
l.grid(column=0, row=5, columnspan=4)
goal_buttons.append(l)
b = Button(main, text='Continue', command=exit_goal_menu)
b.grid(column=1, row=6, columnspan=2)
goal_buttons.append(b)
for i in goal_buttons:
    i.grid_remove()
step_var = StringVar(value='Steps: 0')
goal_var = StringVar(value='Try to get 4 cups of water into one of these buckets:')
Label(main, textvariable=step_var).grid(column=0, row=1, columnspan=4)
Label(main, textvariable=goal_var).grid(column=0, row=0, columnspan=4)
Button(main, text='Restart', command=restart).grid(column=1, row=7, columnspan=2)
m = Menu(root)
root['menu'] = m
themes_menu = Menu(m)
s = Style()
for i in s.theme_names():
    themes_menu.add_command(label=i, command=lambda i=i: s.theme_use(i))
m.add_cascade(label='Themes', menu=themes_menu)
root.mainloop()