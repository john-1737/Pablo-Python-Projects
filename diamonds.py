r"""Diamonds, by Al Sweigart al@inventwithpython.com
Draws diamonds of various sizes.
View this code at https://nostarch.com/big-book-small-python-projects
                           /\       /\
                          /  \     //\\
            /\     /\    /    \   ///\\\
           /  \   //\\  /      \ ////\\\\
 /\   /\  /    \ ///\\\ \      / \\\\////
/  \ //\\ \    / \\\///  \    /   \\\///
\  / \\//  \  /   \\//    \  /     \\//
 \/   \/    \/     \/      \/       \/
Tags: tiny, beginner, artistic"""
from tkinter import Tk, Canvas, IntVar, colorchooser, BooleanVar, Toplevel
from tkinter.ttk import Frame, Label, Spinbox, Button, Scrollbar, Checkbutton, Notebook

def help():
    win = Toplevel(root)
    win.title('Help')
    n = Notebook(win)
    n.grid(sticky='nwes')

    n.add(Label(n, text='''Welcome to Diamonds!
This program draws diamonds of various sizes and colors.
Inspired by Al Sweigart's Diamonds.'''), text='About')
    
    n.add(Label(n, text='''
The Add Diamond at Top button adds a diamond at the top of the diamonds.
The Add Diamond at Bottom button adds a diamond at the bottom of the diamonds.
The Help button opens the help menu.
                
You can click on a diamond in the canvas to select it. The following controls
are only present when a diamond is selected.

The Add Diamond Above button adds a diamond above the selected diamond.
The Add Diamond Below button adds a diamond below the selected diamond.
The Fill checkbox determines whether the selected diamond is filled.
It is checked by default.
The Outline checkbox determines whether the selected diamond is
outlined. It is checked by default.
The color picker (which looks like a colored box) below the Fill
checkbox determines the fill color of the diamond. The default is red.
The color picker (which looks like a colored box) below the Outline
checkbox determines the outline color of the diamond. The default is
black.
The Size picker determines the size of the diamond. You can pick any
size between 10 and 200 in 10-pixel units. The default is 100.
The Delete Diamond button deletes the selected diamond.'''), text='Controls')

class color_label:
    def __init__(self, root, default='black', title='', command=None):
        self.root = root
        self.color = default
        self.command = command
        self.widget = Label(self.root, text='██', foreground=self.color)
        self.title = title
        self.widget.bind('<Button-1>', self.change_color)

    def grid(self, column=0, row=0, columnspan=1, rowspan=1):
        self.widget.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

    def change_color(self, evt):
        self.color = colorchooser.askcolor(initialcolor=self.color, title=self.title)[1]
        self.widget.config(foreground=self.color)
        if self.command != None:
            self.command()

    def set_color(self, color):
        self.color = color
        self.widget.config(foreground=self.color)

def main():
    global diamonds, c, tag, selected_frame, selected, cl1, cl2, fill, outline, size, sizebox, root
    root = Tk()
    root.title('Diamonds')
    diamonds = {}
    tag = 0
    selected = None
    f = Frame(root)
    f.grid(sticky='nwes')
    c = Canvas(f, width=200, height=300)
    c.grid(column=0, row=3)
    s = Scrollbar(f, orient='vertical', command=c.yview)
    c['yscrollcommand'] = s.set
    c.tag_bind('all', '<Button-1>', select_diamond)
    c.configure(scrollregion=c.bbox("all"))
    s.grid(column=1, row=3, sticky='ns')
    Button(f, text='Add Diamond at Top', command=add_diamond_to_top).grid(column=0, row=0)
    Button(f, text='Add Diamond at Bottom', command=add_diamond_to_bottom).grid(column=0, row=1)
    selected_frame = Frame(f)
    selected_frame.grid(column=0, row=2, columnspan=2); selected_frame.grid_remove()
    Button(selected_frame, text='Add Diamond Above', command=lambda: add_diamond_above(selected)).grid(column=0, row=0, columnspan=3)
    Button(selected_frame, text='Add Diamond Below', command=lambda: add_diamond_below(selected)).grid(column=0, row=1, columnspan=3)
    fill = BooleanVar(value=False)
    outline = BooleanVar(value=False)
    Checkbutton(selected_frame, text='Fill', variable=fill, onvalue=True, offvalue=False, command=lambda: change_fill(selected)).grid(column=0, row=2)
    Checkbutton(selected_frame, text='Outline', variable=outline, onvalue=True, offvalue=False, command=lambda: change_outline(selected)).grid(column=1, row=2)
    cl1 = color_label(selected_frame, command=lambda: change_fill(selected))
    cl1.grid(column=0, row=3)
    cl2 = color_label(selected_frame, command=lambda: change_outline(selected))
    cl2.grid(column=1, row=3)
    Label(selected_frame, text='Size:').grid(column=2, row=2)
    size = IntVar()
    sizebox = Spinbox(selected_frame, width=3, textvariable=size, from_=10, to=200, increment=10, wrap=True, command=lambda: change_size(selected))
    sizebox.state(['readonly'])
    sizebox.grid(column=2, row=3)
    Button(selected_frame, text='Delete Diamond', command=lambda: delete_diamond(selected)).grid(column=0, row=4, columnspan=3)
    Button(f, text='Help', command=help).grid(column=0, row=4, columnspan=2)
    root.mainloop()

def delete_diamond(s):
    global selected
    selected = s
    del diamonds[int(selected)]
    for i in diamonds:
        if i > int(selected):
            diamonds[i][0] -= 1
    selected = None
    selected_frame.grid_remove()
    draw_diamonds()

def add_diamond_above(selected):
    global tag
    for i in diamonds:
        if i >= int(selected):
            diamonds[i][0] += 1
    diamonds[tag] = [int(selected), 100, 'red', 'black']
    tag += 1
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

def add_diamond_below(selected):
    global tag
    for i in diamonds:
        if i > int(selected):
            diamonds[i][0] += 1
    diamonds[tag] = [int(selected)+1, 100, 'red', 'black']
    tag += 1
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

def add_diamond_to_bottom():
    global tag
    diamonds[tag] = [len(diamonds), 100, 'red', 'black']
    tag += 1
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

def add_diamond_to_top():
    global tag
    for i in diamonds:
        diamonds[i][0] += 1
    diamonds[tag] = [0, 100, 'red', 'black']
    tag += 1
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

def select_diamond(evt):
    global selected
    tag = c.gettags('current')[0]
    if tag == 'selected':
        return
    c.delete('selected')
    selected_frame.grid()
    selected = tag
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(tag):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20
    c.configure(scrollregion=c.bbox("all"))
    cl1.set_color(diamonds[int(tag)][2])
    cl2.set_color(diamonds[int(tag)][3])
    fill.set(diamonds[int(tag)][2] != '')
    outline.set(diamonds[int(tag)][3] != '')
    size.set(diamonds[int(tag)][1])

def draw_diamonds():
    vertical_space = 0
    c.delete('all')
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill=j[2], outline=j[3], tags=i)
        vertical_space += j[1]*2+20
    c.configure(scrollregion=c.bbox("all"))

def change_fill(selected):
    if fill.get() == False:
        diamonds[int(selected)][2] = ''
    else:
        diamonds[int(selected)][2] = cl1.color
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

def change_outline(selected):
    if outline.get() == False:
        diamonds[int(selected)][3] = ''
    else:
        diamonds[int(selected)][3] = cl2.color
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

def change_size(selected):
    diamonds[int(selected)][1] = size.get()
    draw_diamonds()
    vertical_space = 0
    for i, j in sorted(list(diamonds.items()), key=lambda i:i[1][0]):
        if str(i)==str(selected):
            c.create_polygon((100, vertical_space, 100-j[1]/2, vertical_space+j[1], 100, vertical_space+j[1]*2, 100+j[1]/2, vertical_space+j[1]), fill='', outline='blue', dash=(4, 4), tags='selected', width=5)
        vertical_space += j[1]*2+20

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()
