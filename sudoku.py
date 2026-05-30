"""Sudoku Puzzle, by Al Sweigart al@inventwithpython.com
The classic 9x9 number placement puzzle.
More info at https://en.wikipedia.org/wiki/Sudoku
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, object-oriented, puzzle"""

import copy, random, sys
from tkinter import Tk, StringVar, Toplevel, PhotoImage
from tkinter import Label as img_label
from tkinter.ttk import Frame, Separator, Entry, Label, Button
from tkinter.font import Font, nametofont

# This game requires a sudokupuzzle.txt file that contains the puzzles.
# Download it from https://inventwithpython.com/sudokupuzzles.txt
# Here's a sample of the content in this file:
# ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
# 2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3
# ......9.7...42.18....7.5.261..9.4....5.....4....5.7..992.1.8....34.59...5.7......
# .3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.

# Set up the constants:
EMPTY_SPACE = ' '
GRID_LENGTH = 9
BOX_LENGTH = 3
FULL_GRID_SIZE = GRID_LENGTH * GRID_LENGTH


class SudokuGrid:
    def __init__(self, originalSetup):
        # originalSetup is a string of 81 characters for the puzzle
        # setup, with numbers and periods (for the blank spaces).
        # See https://inventwithpython.com/sudokupuzzles.txt
        self.originalSetup = originalSetup.replace('.', ' ')

        # The state of the sudoku grid is represented by a dictionary
        # with (x, y) keys and values of the number (as a string) at
        # that space.
        self.grid = {}
        self.original = {}
        self.moves = []  # Tracks each move for the undo feature.
        for x in range(1, GRID_LENGTH + 1):
            for y in range(1, GRID_LENGTH + 1):
                self.original[(x, y)] = EMPTY_SPACE

        assert len(self.originalSetup) == FULL_GRID_SIZE
        i = 0  # i goes from 0 to 80
        y = 0  # y goes from 0 to 8
        for y in range(1, GRID_LENGTH+1):
            for x in range(1, GRID_LENGTH+1):
                self.original[(x, y)] = self.originalSetup[i]
                i += 1
            if i > FULL_GRID_SIZE:
                break
        self.resetGrid() 

    def resetGrid(self):
        """Reset the state of the grid, tracked by self.grid, to the
        state in self.originalSetup."""
        for x in range(1, GRID_LENGTH + 1):
            for y in range(1, GRID_LENGTH + 1):
                self.grid[(x, y)] = EMPTY_SPACE

        assert len(self.originalSetup) == FULL_GRID_SIZE
        i = 0
        for y in range(1, GRID_LENGTH+1):
            for x in range(1, GRID_LENGTH+1):
                self.grid[(x, y)] = self.originalSetup[i]
                i += 1
        self.display(root=grid_frame)

    def makeMove(self, space):
        has_won.set('')
        if len(self.num_vars[space].get()) > 1:
            self.num_vars[space].set(self.num_vars[space].get()[0])
            error.set('All boxes must have 1 digit')
            return
        if (not self.num_vars[space].get().isdigit()) and (not self.num_vars[space].get() == ''):
            self.num_vars[space].set('')
            error.set('All boxes must have numbers')
            return
        if not self.is_grid_valid():
            self.num_vars[space].set('')
            return
        
        for i in self.grid:
            self.grid[i] = self.num_vars[i].get()
        x, y = space
        number = self.grid[space]
        """Place the number at the column (a letter from A to I) and row
        (an integer from 1 to 9) on the grid."""
        try:
            for i in self.grid:
                self.grid[i] = self.num_vars[i].get()
        except KeyError:
            pass
        # Check if the move is being made on a "given" number:
        if self.originalSetup[(y-1) * GRID_LENGTH + (x-1)] != EMPTY_SPACE:
            return False

        self.grid[(x, y)] = number  # Place this number on the grid.

        # We need to store a separate copy of the dictionary object:
        self.moves.append(copy.copy(self.grid))
        if self.isSolved():
            has_won.set('You have solved the puzzle!')
        return True

    def undo(self):
        """Set the current grid state to the previous state in the
        self.moves list."""
        if self.moves == []:
            return  # No states in self.moves, so do nothing.
        self.moves.pop(-1)
        # last_item = self.moves[-1]
        # while self.moves[-1] == last_item:
        #     self.moves.pop(-1)  # Remove the current state.

        if self.moves == []:
            self.resetGrid()
        else:
            # set the grid to the last move.
            self.grid = copy.copy(self.moves[-1])
        for i in self.num_vars:
            self.num_vars[i].set(self.grid[i])
        self.display(root=grid_frame)

    def display(self, root, interactive=True):
        """Display the current state of the grid on the screen."""
        if interactive:
            self.num_vars = {}
            self.num_traces = {}
        for i in root.winfo_children():
            i.grid_forget()
        Separator(root, orient='horizontal').grid(row=3, column=0, columnspan=11, sticky='ew')
        Separator(root, orient='horizontal').grid(row=7, column=0, columnspan=11, sticky='ew')
        Separator(root, orient='vertical').grid(row=0, column=3, rowspan=11, sticky='ns')
        Separator(root, orient='vertical').grid(row=0, column=7, rowspan=11, sticky='ns')
        for y in range(1, 10):
            for x in range(1, 10):
                grid_item = self.original[(x, y)]
                xp, yp = x, y
                if x > 6:
                    xp += 2
                elif x > 3:
                    xp += 1
                if y > 6:
                    yp += 2
                elif y > 3:
                    yp += 1
                if grid_item == EMPTY_SPACE:
                    if interactive:
                        s = StringVar(value=self.grid[(x, y)])
                        self.num_vars[x, y] = s
                        if s.get() == ' ':
                            s.set('')
                            e = Entry(root, textvariable=s, width=1)
                        else:
                            e = Entry(root, textvariable=s, width=1)
                        e.grid(column=xp-1, row=yp-1)
                        #s.trace_add('write', lambda a, b, c, x=x, y=y: self.makeMove((x, y)))
                        e.bind('<KeyRelease>', lambda event, x=x, y=y: self.makeMove((x, y)))                
                    else:
                        Label(root, text='.', width=1).grid(column=xp-1, row=yp-1)
                else:
                    if interactive:
                        self.num_vars[x, y] = StringVar(value=grid_item)
                    Label(root, text=grid_item, width=1).grid(column=xp-1, row=yp-1)

    def _isCompleteSetOfNumbers(self, numbers):
        """Return True if numbers contains the digits 1 through 9."""
        return sorted(numbers) == list('123456789')

    def is_valid(self, numbers):
        for i in '123456789':
            if numbers.count(i) > 1:
                return False
        return True

    def isSolved(self):
        """Returns True if the current grid is in a solved state."""
        # Check each row:
        for row in range(1, GRID_LENGTH+1):
            rowNumbers = []
            for x in range(1, GRID_LENGTH+1):
                number = self.grid[(x, row)]
                rowNumbers.append(number)
            if not self._isCompleteSetOfNumbers(rowNumbers):
                return False

        # Check each column:
        for column in range(1, GRID_LENGTH+1):
            columnNumbers = []
            for y in range(1, GRID_LENGTH+1):
                number = self.grid[(column, y)]
                columnNumbers.append(number)
            if not self._isCompleteSetOfNumbers(columnNumbers):
                return False

        # Check each box:
        for boxx in (0, 3, 6):
            for boxy in (0, 3, 6):
                boxNumbers = []
                for x in range(BOX_LENGTH):
                    for y in range(BOX_LENGTH):
                        number = self.grid[(boxx + x, boxy + y)]
                        boxNumbers.append(number)
                if not self._isCompleteSetOfNumbers(boxNumbers):
                    return False

        return True
    
    def is_grid_valid(self):
        """Returns True if the current grid is in a solved state."""
        # Check each row:
        for row in range(1, GRID_LENGTH+1):
            rowNumbers = []
            for x in range(1, GRID_LENGTH+1):
                number = self.num_vars[(x, row)].get()
                rowNumbers.append(number)
            if not self.is_valid(rowNumbers):
                error.set('Rows cannot contain duplicates')
                return False

        # Check each column:
        for column in range(1, GRID_LENGTH+1):
            columnNumbers = []
            for y in range(1, GRID_LENGTH+1):
                number = self.num_vars[(column, y)].get()
                columnNumbers.append(number)
            if not self.is_valid(columnNumbers):
                error.set('Columns cannot contain duplicates')
                return False

        # Check each box:
        for boxx in (1, 4, 7):
            for boxy in (1, 4, 7):
                boxNumbers = []
                for x in range(BOX_LENGTH):
                    for y in range(BOX_LENGTH):
                        number = self.num_vars[(boxx + x, boxy + y)].get()
                        boxNumbers.append(number)
                if not self.is_valid(boxNumbers):
                    error.set('Boxes cannot contain duplicates')
                    return False
        error.set('')
        return True
    
def get_original_grid():
    win = Toplevel(root)
    win.title('The original grid looked like this:')
    f = Frame(win)
    f.grid(sticky='nsew')
    SudokuGrid(grid.originalSetup).display(root=f, interactive=False)

def instructions():
    global img
    win = Toplevel(root)
    win.title('Instructions')
    f = Frame(win)
    f.grid(sticky='nsew')
    Label(f, text='''Sudoku is a number placement logic puzzle game. A Sudoku grid is a 9x9
grid of numbers. Try to place numbers in the grid such that every row,
column, and 3x3 box has the numbers 1 through 9 once and only once.

For example, here is a starting Sudoku grid and its solved form:
''').grid(column=0, row=0, columnspan=3)
    grid1 = Frame(f)
    grid1.grid(column=0, row=1)
    grid2 = Frame(f)
    grid2.grid(column=2, row=1)
    SudokuGrid('534678912672195348198342567859761423426853791713924856961537284287419635345286179').display(grid2, False)
    SudokuGrid('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79').display(grid1, False)
    img = PhotoImage(file='right_arrow.png')
    img_label(f, image=img).grid(column=1, row=1)
    Label(f, text='\nThis program is based on Al Sweigart\'s Sudoku Puzzle.').grid(column=0, row=2, columnspan=3)

root = Tk()
root.title('Sudoku')
f = Frame(root)
f.grid(sticky='nsew')
grid_frame = Frame(f)
grid_frame.grid(column=0, row=0, columnspan=2)


# Load the sudokupuzzles.txt file:
with open('sudokupuzzles.txt') as puzzleFile:
    puzzles = puzzleFile.readlines()

# Remove the newlines at the end of each puzzle:
for i, puzzle in enumerate(puzzles):
    puzzles[i] = puzzle.strip()
error = StringVar()
has_won = StringVar()

def new_grid():
    global grid
    grid = SudokuGrid(random.choice(puzzles))
    grid.display(root=grid_frame)
    error.set('')
    font_dict = nametofont('TkDefaultFont').actual()
    font_dict['weight'] = 'bold'
    bold_font = Font(**font_dict)
    Label(f, textvariable=error, foreground='red', font=bold_font).grid(column=0, row=1, columnspan=2)
    Label(f, textvariable=has_won).grid(column=0, row=1, columnspan=2)
    Button(f, text='Reset', command=grid.resetGrid).grid(column=0, row=2)
    Button(f, text='New', command=new_grid).grid(column=1, row=2)
    Button(f, text='Undo', command=grid.undo).grid(column=0, row=3)
    Button(f, text='Original', command=get_original_grid).grid(column=1, row=3)
    Button(f, text='About', command=instructions).grid(column=0, row=4, columnspan=2)

new_grid()
root.mainloop()

"""

# Check if the puzzle is solved.
if grid.isSolved():
    print('Congratulations! You solved the puzzle!')
    print('Thanks for playing!')
    sys.exit()

# Get the player's action:
while True:  # Keep asking until the player enters a valid action.
    print()  # Print a newline.
    print('Enter a move, or RESET, NEW, UNDO, ORIGINAL, or QUIT:')
    print('(For example, a move looks like "B4 9".)')

    action = input('> ').upper().strip()

    if len(action) > 0 and action[0] in ('R', 'N', 'U', 'O', 'Q'):
        # Player entered a valid action.
        break

    if len(action.split()) == 2:
        space, number = action.split()
        if len(space) != 2:
            continue

        column, row = space
        if column not in list('ABCDEFGHI'):
            print('There is no column', column)
            continue
        if not row.isdecimal() or not (1 <= int(row) <= 9):
            print('There is no row', row)
            continue
        if not (1 <= int(number) <= 9):
            print('Select a number from 1 to 9, not ', number)
            continue
        break  # Player entered a valid move.

print()  # Print a newline.

if action.startswith('R'):
    # Reset the grid:
    grid.resetGrid()
    

if action.startswith('N'):
    # Get a new puzzle:
    grid = SudokuGrid(random.choice(puzzles))
    

if action.startswith('U'):
    # Undo the last move:
    grid.undo()
    

if action.startswith('O'):
    # View the original numbers:
    originalGrid = SudokuGrid(grid.originalSetup)
    print('The original grid looked like this:')
    originalGrid.display()
    input('Press Enter to continue...')

if action.startswith('Q'):
    # Quit the game.
    print('Thanks for playing!')
    sys.exit()

# Handle the move the player selected.
if grid.makeMove(column, row, number) == False:
    print('You cannot overwrite the original grid\'s numbers.')
    print('Enter ORIGINAL to view the original grid.')
    input('Press Enter to continue...')"""
