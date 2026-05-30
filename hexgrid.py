"""Shining Carpet, by Al Sweigart al@inventwithpython.com
Displays a tessellation of the carpet pattern from The Shining.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, artistic"""

from tkinter import Tk, StringVar, Canvas, BitmapImage, Toplevel
from tkinter.ttk import Frame, Spinbox, Label, Button, Radiobutton
from tkinter import Label as TkLabel
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageOps

def show_image():
    win = Toplevel(root)
    win.title('Image')
    c = Canvas(win, width=int(x_repeat.get())*40, height=int(y_repeat.get())*40)
    c.grid(sticky='nwes')
    img = BitmapImage(file=f'{shape.get()}-{fill.get()}.xbm', foreground=foreground.get(), background=background.get())
    for i in range(int(x_repeat.get())):
        for j in range(int(y_repeat.get())):
            c.create_image(i*40, j*40, image=img, anchor='nw')
    win.mainloop()

def export_image():
    """
    Converts XBM to a colored image.
    fg_color/bg_color can be named colors ('red'), hex ('#FF0000'), or RGB tuples.
    """
    bg = Image.new('RGB', (int(x_repeat.get())*40, int(y_repeat.get())*40), (255, 255, 255))

    img = Image.open(f'{shape.get()}-{fill.get()}.xbm')
    
    img = img.convert('L')

    img = ImageOps.colorize(img, black=background.get(), white=foreground.get())
    
    for i in range(int(x_repeat.get())):
        for j in range(int(y_repeat.get())):
            bg.paste(img, (i*40, j*40))
    filename = asksaveasfilename(title='Select file name', filetypes=(('PNG files', '*.png'),))
    if filename:
        bg.save(filename)

class Color_picker:
    def __init__(self, root, colorvar, message='Colors'):
        self.colorvar = colorvar
        self.message = message
        self.label = TkLabel(root, background=self.colorvar.get(), text='  ', font=('Courier', 20))
        self.label.bind('<Button-1>', self.get_color)
    
    def grid(self, column, row, columnspan=1, rowspan=1):
        self.label.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

    def get_color(self, evt):
        color = askcolor(initialcolor=self.colorvar.get(), title=self.message)
        if color[1]:
            self.colorvar.set(color[1])
            self.label.config(background=self.colorvar.get())

root = Tk()
root.title('Hex Grid')
f = Frame(root)
f.grid(sticky='nwes')
Label(f, text='Tiles to fill horizontally:').grid(column=0, row=0)
x_repeat = StringVar(value=6)
s = Spinbox(f, from_=1, to=200, textvariable=x_repeat, width=3)
s.grid(column=1, row=0)
s.state(['readonly'])
Label(f, text='Tiles to fill vertically:').grid(column=0, row=1)
y_repeat = StringVar(value=4)
s = Spinbox(f, from_=1, to=200, textvariable=y_repeat, width=3)
s.grid(column=1, row=1)
s.state(['readonly'])
foreground = StringVar(value='#000000')
Label(f, text='Foreground color:').grid(column=0, row=2)
Color_picker(f, foreground, 'Set foreground color').grid(column=1, row=2)
background = StringVar(value='#ffffff')
Label(f, text='Background color:').grid(column=0, row=3)
Color_picker(f, background, 'Set background color').grid(column=1, row=3)
shape = StringVar(value='hex')
fill = StringVar(value='filled')
Radiobutton(f, variable=fill, value='filled', text='◼︎ Filled').grid(column=0, row=6, columnspan=2)
Radiobutton(f, variable=fill, value='outlined', text='◻︎ Outlined').grid(column=0, row=7, columnspan=2)
Radiobutton(f, variable=shape, value='hex', text='⬡ Hexagon tiles').grid(column=0, row=4, columnspan=2)
Radiobutton(f, variable=shape, value='brick', text='▭ Rectangle bricks').grid(column=0, row=5, columnspan=2)
Button(f, text='Show Image', command=show_image).grid(column=0, row=8, columnspan=2)
Button(f, text='Export Image', command=export_image).grid(column=0, row=9, columnspan=2)
root.mainloop()