"""Maze 3D, by Al Sweigart al@inventwithpython.com
Move around a maze and try to escape... in 3D!
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: extra-large, artistic, maze, game"""

import copy, sys, os
from tkinter import Tk, Canvas, Button, Label, filedialog, messagebox, PhotoImage, StringVar, DISABLED, Menu, Toplevel

# Set up the constants:
WALL = '#'
EMPTY = ' '
START = 'S'
EXIT = 'E'
BLOCK = chr(9617)  # Character 9617 is '░'
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'


def wallStrToWallDict(wallStr):
    """Takes a string representation of a wall drawing (like those in
    ALL_OPEN or CLOSED) and returns a representation in a dictionary
    with (x, y) tuples as keys and single-character strings of the
    character to draw at that x, y location."""
    wallDict = {}
    height = 0
    width = 0
    for y, line in enumerate(wallStr.splitlines()):
        if y > height:
            height = y
        for x, character in enumerate(line):
            if x > width:
                width = x
            wallDict[(x, y)] = character
    wallDict['height'] = height + 1
    wallDict['width'] = width + 1
    return wallDict

EXIT_DICT = {(0, 0): 'E', (1, 0): 'X', (2, 0): 'I',
             (3, 0): 'T', 'height': 1, 'width': 4}

# The way we create the strings to display is by converting the pictures
# in these multiline strings to dictionaries using wallStrToWallDict().
# Then we compose the wall for the player's location and direction by
# "pasting" the wall dictionaries in CLOSED on top of the wall dictionary
# in ALL_OPEN.
root = Tk()
ALL_OPEN = PhotoImage(file='allopen.gif')

CLOSED = {}
CLOSED['A'] = PhotoImage(file='closeda.gif')
CLOSED['B'] = PhotoImage(file='closedb.gif')
CLOSED['C'] = PhotoImage(file='closedc.gif')
CLOSED['D'] = PhotoImage(file='closedd.gif')
CLOSED['E'] = PhotoImage(file='closede.gif')
CLOSED['F'] = PhotoImage(file='closedf.gif')

EXITS = {}
EXITS['A'] = PhotoImage(file='exita.gif')
EXITS['B'] = PhotoImage(file='exitb.gif')
EXITS['C'] = PhotoImage(file='exitc.gif')
EXITS['D'] = PhotoImage(file='exitd.gif')
EXITS['E'] = PhotoImage(file='exite.gif')
EXITS['F'] = PhotoImage(file='exitf.gif')

def displayWallStructure(wallStruc):
    """Display a wall dictionary, as returned by wallStrToWallDict(), on
    the screen."""
    c.delete('all')
    for image in wallStruc:
        c.create_image(0, 0, image=get_image(image), anchor='nw', tags='all')

def get_image(image):
    return image

def pasteWallDict(srcWallDict, dstWallDict, left, top):
    """Copy the wall representation dictionary in srcWallDict on top of
    the one in dstWallDict, offset to the position given by left, top."""
    dstWallDict = copy.copy(dstWallDict)
    for x in range(srcWallDict['width']):
        for y in range(srcWallDict['height']):
            dstWallDict[(x + left, y + top)] = srcWallDict[(x, y)]
    return dstWallDict


def makeWallStructure(maze, playerx, playery, playerDirection, exitx, exity):
    """From the player's position and direction in the maze (which has
    an exit at exitx, exity), create the wall representation dictionary
    by pasting wall dictionaries on top of ALL_OPEN, then return it."""

    # The A-F "sections" (which are relative to the player's direction)
    # determine which walls in the maze we check to see if we need to
    # paste them over the wall representation dictionary we're creating.

    if playerDirection == NORTH:
        # Map of the sections, relative  A
        # to the player @:              BCD (Player facing north)
        #                               E@F
        offsets = (('A', 0, -2), ('B', -1, -1), ('C', 0, -1),
                   ('D', 1, -1), ('E', -1, 0), ('F', 1, 0))
    if playerDirection == SOUTH:
        # Map of the sections, relative F@E
        # to the player @:              DCB (Player facing south)
        #                                A
        offsets = (('A', 0, 2), ('B', 1, 1), ('C', 0, 1),
                   ('D', -1, 1), ('E', 1, 0), ('F', -1, 0))
    if playerDirection == EAST:
        # Map of the sections, relative EB
        # to the player @:              @CA (Player facing east)
        #                               FD
        offsets = (('A', 2, 0), ('B', 1, -1), ('C', 1, 0),
                   ('D', 1, 1), ('E', 0, -1), ('F', 0, 1))
    if playerDirection == WEST:
        # Map of the sections, relative  DF
        # to the player @:              AC@ (Player facing west)
        #                                BE
        offsets = (('A', -2, 0), ('B', -1, 1), ('C', -1, 0),
                   ('D', -1, -1), ('E', 0, 1), ('F', 0, -1))

    section = {}
    for sec, xOff, yOff in offsets:
        section[sec] = maze.get((playerx + xOff, playery + yOff), WALL)
        if (playerx + xOff, playery + yOff) == (exitx, exity):
            section[sec] = EXIT

    wallStructure = [ALL_OPEN]
    for sec in 'ABD':
        if section[sec] in (WALL, EXIT):
            wallStructure.append(CLOSED[sec])
    for sec in 'ABD':
        if section[sec] == EXIT:
            wallStructure.append(EXITS[sec])
    for sec in 'EFC':
        if section[sec] in (WALL, EXIT):
            wallStructure.append(CLOSED[sec])
    for sec in 'EFC':
        if section[sec] == EXIT:
            wallStructure.append(EXITS[sec])


    return wallStructure

def start():
    root.withdraw()
    global win
    for i in ctrlbuttons:
        i['command'] = DISABLED
    for i in [('Left', 'A'), ('Up', 'W'), ('Right', 'D')]:
        root.unbind(f'<{i[0]}>')
    win = Tk()
    win.title('Maze Runner 3D')
    Label(win, text='Welcome to Maze Runner 3D!\nUse the up, left, and right keys or arrow keys to\nmove your character around the maze and reach the exit.\nClick Start to start!').pack()
    Button(win, text='Start', command=get_file).pack()

def get_file():
    try:
        win.destroy()
    except:
        pass
    global maze, px, py, exitx, exity, pDir
    filename = filedialog.askopenfilename(title='Select maze file', filetypes=(("Text files", "*.txt"),))
    if not filename:
        start()
    # Load the maze from a file:
    mazeFile = open(filename)
    maze = {}
    lines = mazeFile.readlines()
    mazeFile.close()
    px = None
    py = None
    exitx = None
    exity = None
    y = 0
    brk = False
    for line in lines:
        WIDTH = len(line.rstrip())
        for x, character in enumerate(line.rstrip()):
            if not character in (WALL, EMPTY, START, EXIT, '\n'): 
                messagebox.showwarning(message='Invalid character at column {}, line {}'.format(x + 1, y + 1))
                get_file()
            if character in (WALL, EMPTY):
                maze[(x, y)] = character
            elif character == START:
                px, py = x, y
                maze[(x, y)] = EMPTY
            elif character == EXIT:
                exitx, exity = x, y
                maze[(x, y)] = EMPTY
        y += 1
    HEIGHT = y

    if not px != None and py != None:
        messagebox.showwarning(message='No start point in file.')
        get_file()
    if not exitx != None and exity != None:
        messagebox.showwarning(message='No exit point in file.')
        get_file()
    pDir = NORTH
    motions = {0:'A', 1:'W', 2:'D'}
    root.deiconify()
    posvar.set(f'Location: ({px}, {py})    Direction: {pDir}')
    displayWallStructure(makeWallStructure(maze, px, py, pDir, exitx, exity))
    ctrlbuttons[0]['command'] = lambda: move(motions[0])
    ctrlbuttons[1]['command'] = lambda: move(motions[1])
    ctrlbuttons[2]['command'] = lambda: move(motions[2])
    root.bind(f'<Left>', lambda e: move(motions[0]))
    root.bind(f'<Right>', lambda e: move(motions[2]))
    root.bind(f'<Up>', lambda e: move(motions[1]))

def move(dir):
    global px, py, pDir
    if dir == 'F' or dir == 'W':
        if pDir == NORTH and maze[(px, py - 1)] == EMPTY:
            py -= 1
        if pDir == SOUTH and maze[(px, py + 1)] == EMPTY:
            py += 1
        if pDir == EAST and maze[(px + 1, py)] == EMPTY:
            px += 1
        if pDir == WEST and maze[(px - 1, py)] == EMPTY:
            px -= 1
    elif dir == 'L' or dir == 'A':
        pDir = {NORTH: WEST, WEST: SOUTH,
                SOUTH: EAST, EAST: NORTH}[pDir]
    elif dir == 'R' or dir == 'D':
        pDir = {NORTH: EAST, EAST: SOUTH,
                SOUTH: WEST, WEST: NORTH}[pDir]
    posvar.set(f'Location: ({px}, {py})    Direction: {pDir}')
    displayWallStructure(makeWallStructure(maze, px, py, pDir, exitx, exity))
    if (px, py) == (exitx, exity):
        for i in ctrlbuttons:
            i['command'] = DISABLED
        for i in [('Left', 'A'), ('Up', 'W'), ('Right', 'D')]:
            root.unbind(f'<{i[0]}>')
        c.delete('all')
        c.create_text(10, 10, text='You have reached the exit! Good job!', tags='all', anchor='nw')
        c.create_text(10, 60, text='You can play again by pressing Restart.', tags='all', anchor='nw')


def help():
    win2 = Toplevel(root)
    Label(win2, text='Welcome to Maze Runner 3D!\nUse the up, down, and left keys or arrow keys to\n\
move your character around the maze and reach the exit.\n\
You can use this program to explore mazes you create in a text editor.\n\
When creating your maze, use # for walls, a space for empty areas,\n\
an S for a start and an X for an exit. You must save your mazes as\n\
a .txt (text) file.\n\
At any time during the game, press Restart to choose a new maze.').pack()
    Button(win2, text='Back', command=win2.destroy).pack()
    
root.title('Maze Runner 3D')
c = Canvas(root, width=340, height=440)
c.grid(column=0, row=0, columnspan=3)
posvar = StringVar()
Label(root, textvariable=posvar).grid(column=0, row=1, columnspan=3)
ctrlbuttons = []
for i, j in enumerate(('←', '↑', '→')):
    b=Button(root, width=3, height=3, text=j, command=DISABLED)
    b.grid(column=i, row=2)
    ctrlbuttons.append(b)
Button(root, text='Restart', command=start).grid(column=0, row=3, columnspan=3)
Button(root, text='Help', command=help).grid(column=0, row=4, columnspan=3)

root.withdraw()
start()
root.mainloop()