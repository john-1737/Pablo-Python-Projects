import tkinter as tk
root = tk.Tk()

x1, x2, y1, y2 = 0,0,0,0

def get_coords(x, y, num, unbind=True):
    global x1, y1, x2, y2
    if num == 2:
        x2 = x
        y2 = y
    else:
        x1 = x
        y1 = y
    if unbind:    
        root.unbind('<Button-1>')

def add_line():
    get_coords(0,0,1, False)
    get_coords(0,0,2, False)
    root.bind('<Button-1>', lambda e:get_coords(e.x, e.y, 1))
    root.bind('<Button-1>', lambda e:get_coords(e.x, e.y, 2))
    while x1==0 or x2==0 or y1==0 or y2==0:
        root.update()
    print(x1, y1, x2, y2)
    c.create_line(x1, y1, x2, y2)


root.option_add('*tearoff', tk.FALSE)
c = tk.Canvas(root, width=500, height=500)
c.pack()
menubar = tk.Menu(root)
root['menu'] = menubar
add_menu = tk.Menu(menubar)
add_menu.add_command(label='Add Line', command=add_line)
menubar.add_cascade(menu=add_menu, label='Add Shape')
root.mainloop()