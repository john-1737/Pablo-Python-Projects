from turtle import Turtle, Screen, RawTurtle, TurtleScreen
from tkinter import Tk, Canvas, Menu, filedialog, messagebox, simpledialog, IntVar, Label, Scale
from random import choice

def movel(*args):
    moves.append('A')
    t.setheading(180)
    t.forward(10)
def mover(*args):
    moves.append('D')
    t.setheading(0)
    t.forward(10)
def moveu(*args):
    moves.append('W')
    t.setheading(90)
    t.forward(10)
def moved(*args):
    moves.append('S')
    t.setheading(270)
    t.forward(10)

def save():
    path = filedialog.asksaveasfilename()
    if not path:
        return
    with open(path, 'w') as f:
        f.write(''.join(moves))

def view_moves():
    messagebox.showinfo(message='Your moves:\n' + ''.join(moves) + f'\nX: {int(round(t.xcor(), 0))}\tY: {int(round(t.ycor(), 0))}')

def new():
    global moves
    if messagebox.askyesno(message='Are you sure you want to lose your current drawing?', detail='To save it, select File>Save As.'):
        moves = []
        t.reset()

def clear():
    if messagebox.askyesno(message='Are you sure you want to lose your current lines?'):
        moves.append('C')
        t.clear()

def teleport():
    x = round(simpledialog.askinteger('X position','Enter X (horizontal) position:'), -1)
    y = round(simpledialog.askinteger('Y position','Enter Y (vertical) position:'), -1)
    while t.xcor() != x:
        if t.xcor() > x:
            movel(0)
        elif t.xcor() < x:
            mover(0)
    while t.ycor() != y:
        if t.ycor() > y:
            movel(0)
        elif t.ycor() < y:
            mover(0)

def draw_moves(movestr, reset):
    if reset:
        t.reset()
    t.speed(0)
    global moves
    moves = []
    for i in list(movestr): 
        if i == 'W':
            moveu(0)
        elif i == 'A':
            movel(0)
        elif i == 'S':
            moved(0)
        elif i  == 'D':
            mover(0)
        elif i == 'C':
            t.clear()
    t.speed(speed.get())

def enter():
    movestr = simpledialog.askstring(title='Drawing', prompt='Enter WASD key moves for drawing:')
    if bool(movestr) and messagebox.askyesno(message='Are you sure you want to lose your current drawing?', detail='To save it, select File>Save As.'):
        draw_moves(movestr, True)

def random_art(clear):
    movestr = []
    iters = simpledialog.askinteger('Random Drawing', 'Enter the size of your random drawing:')
    if clear:
        fwd = messagebox.askyesno(message='Are you sure you want to lose your current drawing?', detail='To save it, select File>Save As.')
    else:
        fwd = True
    if bool(iters) and fwd:
        for i in range(iters):
            movestr += choice(['W', 'A', 'S', 'D'])
        draw_moves(movestr, clear)

def add_enter():
    movestr = simpledialog.askstring(title='Drawing', prompt='Enter WASD key moves for drawing:')
    if bool(movestr):
        draw_moves(movestr, False)

def open_file():
    path = filedialog.askopenfilename()
    if bool(path) and messagebox.askyesno(message='Are you sure you want to lose your current drawing?', detail='To save it, select File>Save As.'):
        with open(path) as f:
            movestr = f.read()
        draw_moves(movestr, True)

def add_file():
    path = filedialog.askopenfilename()
    if bool(path):
        with open(path) as f:
            movestr = f.read()
        draw_moves(movestr, False)

root = Tk()
root.title('Etching Drawer')
c = Canvas(root, width=500, height=500)
c.pack()
moves = []
speed = IntVar(value=6)
s = TurtleScreen(c)
c.bind_all('<Left>', movel)
c.bind_all('<Right>', mover)
c.bind_all('<Up>', moveu)
c.bind_all('<Down>', moved)
t = RawTurtle(c)
Label(root, text='Set speed:').pack()
Scale(root, orient='horizontal', from_=0, to=10, length=200, variable=speed, command=lambda s: t.speed(float(s))).pack()
Label(root, text='fastest: 0 fast: 10 normal: 6 slow: 3 slowest: 1').pack()
t.speed('normal')
m = Menu(root)
root['menu'] = m
file_menu = Menu(m)
m.add_cascade(menu=file_menu, label='File')
file_menu.add_command(label='Create', command=new)
file_menu.add_command(label='Clear', command=clear)
file_menu.add_command(label='Enter Drawing', command=enter)
file_menu.add_command(label='Add Entered Drawing', command=add_enter)
file_menu.add_command(label='Open File', command=open_file)
file_menu.add_command(label='Add File', command=add_file)
file_menu.add_command(label='Make Random Drawing', command=lambda: random_art(True))
file_menu.add_command(label='Add Random Drawing', command=lambda: random_art(False))
file_menu.add_command(label='Save As', command=save)
file_menu.add_command(label='View Moves', command=view_moves)
edit_menu = Menu(m)
m.add_cascade(menu=edit_menu, label='Edit')
edit_menu.add_command(label='Teleport', command=teleport)
root.mainloop()
