"""Flooder, by Al Sweigart al@inventwithpython.com
A colorful game where you try to fill the board with a single color. Has
a mode for colorblind players.
Inspired by the "Flood It!" game.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, bext, game"""

import random, sys

from tkinter import Canvas, Tk, BitmapImage, StringVar, Menu, Toplevel, colorchooser, IntVar, messagebox
from tkinter.ttk import Button, Frame, Label, Radiobutton, Checkbutton

# Set up the constants:
BOARD_WIDTH = 16  # (!) Try changing this to 4 or 40.
BOARD_HEIGHT = 14  # (!) Try changing this to 4 or 20.
MOVES_PER_GAME = 20  # (!) Try changing this to 3 or 300.

# Constants for the different shapes used in colorblind mode:

# All the color/shape tiles used on the board:
TILE_TYPES = (0, 1, 2, 3, 4, 5)


def mainfunc():
    global c, rectangle, square, circle, star, diamond, triangle, red, orange, yellow, green, blue, purple, colors_map, shapes_map, gameBoard,\
    movesLeft, displayMode, control_buttons, moves_var, progress_var, root, color_scheme, main
    root = Tk()
    root.title('Flooder')
    rectangle = BitmapImage(file='rectangle.xbm', foreground='red')
    square    = BitmapImage(file='square.xbm', foreground='orange')
    circle    = BitmapImage(file='circle.xbm', foreground='yellow')
    star      = BitmapImage(file='star.xbm', foreground='green')
    diamond   = BitmapImage(file='diamond.xbm', foreground='blue')
    triangle  = BitmapImage(file='triangle.xbm', foreground='purple')
    red = BitmapImage(file='square.xbm', foreground='red')
    orange = BitmapImage(file='square.xbm', foreground='orange')
    yellow = BitmapImage(file='square.xbm', foreground='yellow')
    green = BitmapImage(file='square.xbm', foreground='green')
    blue = BitmapImage(file='square.xbm', foreground='blue')
    purple = BitmapImage(file='square.xbm', foreground='purple')
    colors_map = {0: red, 1: orange, 2:yellow, 3:green, 4:blue, 5:purple}
    shapes_map = {0: rectangle, 1: square, 2: circle, 3: star, 4: diamond, 5: triangle}
    main = Frame(root)
    main.grid(sticky='nsew')
    c = Canvas(main, width=(BOARD_WIDTH*20)+20, height=(BOARD_HEIGHT*20)+20)
    c.grid(column=0, row=1, columnspan=6)
    control_buttons = []
    for i, j in enumerate(colors_map):
        b = Button(main, image=colors_map[j], command=lambda i=i: next_move(i))
        b.grid(column=i, row=4)
        control_buttons.append(b)
    displayMode = IntVar(value=0)
    color_scheme = IntVar(value=0)
    moves_var = StringVar()
    progress_var = StringVar()
    Label(main, textvariable=moves_var).grid(column=0, row=2, columnspan=6)
    Label(main, textvariable=progress_var).grid(column=0, row=3, columnspan=6)
    Label(main, text='Make the whole board one color by changing the top left tile:').grid(column=0, row=0, columnspan=6)
    m = Menu(root)
    root['menu'] = m
    accessibility_menu = Menu(m)
    m.add_cascade(menu=accessibility_menu, label='Accessibility')
    accessibility_menu.add_command(command=accessibility_settings, label='Configure Accessibility Settings')
    Button(main, text='Reset', command=reset).grid(column=0, row=5, columnspan=6)
    game()
    root.mainloop()

def game():
    global c, rectangle, square, circle, star, diamond, triangle, red, orange, yellow, green, blue, purple, colors_map, shapes_map, gameBoard,\
    movesLeft, displayMode, control_buttons, moves_var, progress_var, root, color_scheme
    
    gameBoard = getNewBoard()
    movesLeft = MOVES_PER_GAME
    moves_var.set(value=f'Moves left: {movesLeft}')
    progress_var.set(value='Select a color to set the top left tile to:')
    displayBoard(gameBoard, displayMode.get())


def reset():
    if messagebox.askyesno(title='Reset', message='Are you sure you want to reset?', detail='This will delete all your progress.'):
        game()

def getNewBoard():
    """Return a dictionary of a new Flood It board."""

    # Keys are (x, y) tuples, values are the tile at that position.
    board = {}

    # Create random colors for the board.
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            board[(x, y)] = random.choice(TILE_TYPES)

    # Make several tiles the same as their neighbor. This creates groups
    # of the same color/shape.
    for i in range(BOARD_WIDTH * BOARD_HEIGHT):
        x = random.randint(0, BOARD_WIDTH - 2)
        y = random.randint(0, BOARD_HEIGHT - 1)
        board[(x + 1, y)] = board[(x, y)]
    return board

def accessibility_settings():
    global win, color_labels, color_buttons
    win = Toplevel(root)
    win.grab_set()
    win.title('Accessibility Settings')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='Colorblind Mode uses distinct shapes instead of colors.', foreground='gray').grid(column=0, row=1, columnspan=2)
    Label(f, text='Set colors for shapes:').grid(column=0, row=2, columnspan=2)
    for i, j in enumerate(('Normal', 'Black/White', 'Custom')):
        Radiobutton(f, text=j, value=i, variable=color_scheme, command=set_color).grid(column=0, row=i+3, columnspan=2)
    color_buttons = []
    l = Label(f, text='Set custom colors:')
    l.grid(row=6, column=0, columnspan=2)
    color_labels = [l]
    Checkbutton(f, text='Colorblind Mode', onvalue=1, offvalue=0, variable=displayMode, command=edit_images).grid(column=0, row=0, columnspan=2)
    for i in range(6):
        if displayMode.get() == 0:
            l = Label(f, image=colors_map[i])
        elif displayMode.get() == 1:
            l = Label(f, image=shapes_map[i])
        l.grid(row=i+7, column=0)
        color_labels.append(l)
        b = Button(f, text='Change', command=lambda i=i: color_image(i))
        b.grid(row=i+7, column=1)
        color_buttons.append(b)
    Button(f, text='Exit', command=close_accessibility, default='active').grid(row=7+6, column=0, columnspan=2)
    win.protocol("WM_DELETE_WINDOW", close_accessibility)
    set_color()

def edit_images():
    for i, j in enumerate(color_labels[1:]):
        if displayMode.get() == 0:
            j.config(image=colors_map[i])
        elif displayMode.get() == 1:
            j.config(image=shapes_map[i])
    displayBoard(gameBoard, displayMode.get())
    for i, j in enumerate(control_buttons):
        if displayMode.get() == 0:
            j.config(image=colors_map[i])
        elif displayMode.get() == 1:
            j.config(image=shapes_map[i])

def set_color():
    if color_scheme.get() == 0:
        for i, j in enumerate(['red', 'orange', 'yellow', 'green', 'blue', 'purple']):
            colors_map[i].config(foreground=j)
            shapes_map[i].config(foreground=j)
    elif color_scheme.get() == 1:
        for i in range(6):
            colors_map[i].config(foreground='black')
            shapes_map[i].config(foreground='black')
    if color_scheme.get() == 0 or color_scheme.get() == 1:
        for i in color_buttons:
            i.grid_remove()
        for i in color_labels:
            i.grid_remove()
    else:
        for i in color_buttons:
            i.grid()
        for i in color_labels:
            i.grid()

def close_accessibility():
    win.grab_release()
    win.destroy()
    displayBoard(gameBoard, displayMode.get())
    for i, j in enumerate(control_buttons):
        if displayMode.get() == 0:
            j.config(image=colors_map[i])
        elif displayMode.get() == 1:
            j.config(image=shapes_map[i])

def color_image(image_num):
    color = colorchooser.askcolor(initialcolor=['red', 'orange', 'yellow', 'green', 'blue', 'purple'][image_num])[1]
    colors_map[image_num].config(foreground=color)
    shapes_map[image_num].config(foreground=color)

def displayBoard(board, displayMode):
    """Display the board on the screen."""
    c.delete('all')
    # Display the top edge of the board:
    c.create_rectangle(5, 5, (BOARD_WIDTH*20)+15, (BOARD_HEIGHT*20)+15, fill='white', outline='black', width=10)

    # Display each row:
    for y in range(BOARD_HEIGHT):

        # Display each tile in this row:
        for x in range(BOARD_WIDTH):
            if displayMode == 0:
                c.create_image((x*20)+20, (y*20)+20, image=colors_map[board[x,y]])
            elif displayMode == 1:
                c.create_image((x*20)+20, (y*20)+20, image=shapes_map[board[x,y]])



def changeTile(tileType, board, x, y, charToChange=None):
    """Change the color/shape of a tile using the recursive flood fill
    algorithm."""
    if x == 0 and y == 0:
        charToChange = board[(x, y)]
        if tileType == charToChange:
            return  # Base Case: Already is the same tile.

    board[(x, y)] = tileType

    if x > 0 and board[(x - 1, y)] == charToChange:
        # Recursive Case: Change the left neighbor's tile:
        changeTile(tileType, board, x - 1, y, charToChange)
    if y > 0 and board[(x, y - 1)] == charToChange:
        # Recursive Case: Change the top neighbor's tile:
        changeTile(tileType, board, x, y - 1, charToChange)
    if x < BOARD_WIDTH - 1 and board[(x + 1, y)] == charToChange:
        # Recursive Case: Change the right neighbor's tile:
        changeTile(tileType, board, x + 1, y, charToChange)
    if y < BOARD_HEIGHT - 1 and board[(x, y + 1)] == charToChange:
        # Recursive Case: Change the bottom neighbor's tile:
        changeTile(tileType, board, x, y + 1, charToChange)

def next_move(tile):
    global movesLeft
    changeTile(tile, gameBoard, 0, 0)
    displayBoard(gameBoard, displayMode.get())
    movesLeft -= 1
    moves_var.set(f'Moves left: {movesLeft}')
    if hasWon(gameBoard):
        for i in control_buttons:
            i.state(['disabled'])
        progress_var.set('You have won!')
    elif movesLeft == 0:
        for i in control_buttons:
            i.state(['disabled'])
        progress_var.set('You have run out of moves!')

def hasWon(board):
    """Return True if the entire board is one color/shape."""
    tile = board[(0, 0)]
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[(x, y)] != tile:
                return False
    return True


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    mainfunc()
