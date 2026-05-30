"""Mondrian Art Generator, by Al Sweigart al@inventwithpython.com
Randomly generates art in the style of Piet Mondrian.
More info at: https://en.wikipedia.org/wiki/Piet_Mondrian
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, artistic, bext"""

import sys, random

from tkinter import Tk, Canvas, filedialog, messagebox
from tkinter.ttk import Frame, Button
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up the constants:
MIN_X_INCREASE = 6
MAX_X_INCREASE = 16
MIN_Y_INCREASE = 3
MAX_Y_INCREASE = 6
WHITE = 'white'
BLACK = 'black'
RED = 'red'
YELLOW = 'yellow'
BLUE = 'blue'

# Setup the screen:
width, height = 40, 20

def generate_art():  # Main application loop.
    # Pre-populate the canvas with blank spaces:
    canvas = {}
    for x in range(width):
        for y in range(height):
            canvas[(x, y)] = WHITE

    # Generate vertical lines:
    numberOfSegmentsToDelete = 0
    x = random.randint(MIN_X_INCREASE, MAX_X_INCREASE)
    while x < width - MIN_X_INCREASE:
        numberOfSegmentsToDelete += 1
        for y in range(height):
            canvas[(x, y)] = BLACK
        x += random.randint(MIN_X_INCREASE, MAX_X_INCREASE)

    # Generate horizontal lines:
    y = random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)
    while y < height - MIN_Y_INCREASE:
        numberOfSegmentsToDelete += 1
        for x in range(width):
            canvas[(x, y)] = BLACK
        y += random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)

    numberOfRectanglesToPaint = numberOfSegmentsToDelete - 3
    numberOfSegmentsToDelete = int(numberOfSegmentsToDelete * 1.5)

    # Randomly select points and try to remove them.
    for i in range(numberOfSegmentsToDelete):
        while True:  # Keep selecting segments to try to delete.
            # Get a random start point on an existing segment:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)
            if canvas[(startx, starty)] == WHITE:
                continue

            # Find out if we're on a vertical or horizontal segment:
            if (canvas[(startx - 1, starty)] == WHITE and
                canvas[(startx + 1, starty)] == WHITE):
                orientation = 'vertical'
            elif (canvas[(startx, starty - 1)] == WHITE and
                canvas[(startx, starty + 1)] == WHITE):
                orientation = 'horizontal'
            else:
                # The start point is on an intersection,
                # so get a new random start point:
                continue

            pointsToDelete = [(startx, starty)]

            canDeleteSegment = True
            if orientation == 'vertical':
                # Go up one path from the start point, and
                # see if we can remove this segment:
                for changey in (-1, 1):
                    y = starty
                    while 0 < y < height - 1:
                        y += changey
                        if (canvas[(startx - 1, y)] == BLACK and
                            canvas[(startx + 1, y)] == BLACK):
                            # We've found a four-way intersection.
                            break
                        elif ((canvas[(startx - 1, y)] == WHITE and
                               canvas[(startx + 1, y)] == BLACK) or
                              (canvas[(startx - 1, y)] == BLACK and
                               canvas[(startx + 1, y)] == WHITE)):
                            # We've found a T-intersection; we can't
                            # delete this segment:
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((startx, y))

            elif orientation == 'horizontal':
                # Go up one path from the start point, and
                # see if we can remove this segment:
                for changex in (-1, 1):
                    x = startx
                    while 0 < x < width - 1:
                        x += changex
                        if (canvas[(x, starty - 1)] == BLACK and
                            canvas[(x, starty + 1)] == BLACK):
                            # We've found a four-way intersection.
                            break
                        elif ((canvas[(x, starty - 1)] == WHITE and
                               canvas[(x, starty + 1)] == BLACK) or
                              (canvas[(x, starty - 1)] == BLACK and
                               canvas[(x, starty + 1)] == WHITE)):
                            # We've found a T-intersection; we can't
                            # delete this segment:
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((x, starty))
            if not canDeleteSegment:
                continue  # Get a new random start point.
            break  # Move on to delete the segment.

        # If we can delete this segment, set all the points to white:
        for x, y in pointsToDelete:
            canvas[(x, y)] = WHITE

    # Add the border lines:
    for x in range(width):
        canvas[(x, 0)] = BLACK  # Top border.
        canvas[(x, height - 1)] = BLACK  # Bottom border.
    for y in range(height):
        canvas[(0, y)] = BLACK  # Left border.
        canvas[(width - 1, y)] = BLACK  # Right border.

    # Paint the rectangles:
    for i in range(numberOfRectanglesToPaint):
        while True:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)

            if canvas[(startx, starty)] != WHITE:
                continue  # Get a new random start point.
            else:
                break

        # Flood fill algorithm:
        colorToPaint = random.choice([RED, YELLOW, BLUE, BLACK])
        pointsToPaint = set([(startx, starty)])
        while len(pointsToPaint) > 0:
            x, y = pointsToPaint.pop()
            canvas[(x, y)] = colorToPaint
            if canvas[(x - 1, y)] == WHITE:
                pointsToPaint.add((x - 1, y))
            if canvas[(x + 1, y)] == WHITE:
                pointsToPaint.add((x + 1, y))
            if canvas[(x, y - 1)] == WHITE:
                pointsToPaint.add((x, y - 1))
            if canvas[(x, y + 1)] == WHITE:
                pointsToPaint.add((x, y + 1))
    
    return canvas

def draw(canvas):
    # Draw the canvas data structure:
    for y in range(height):
        for x in range(width):
            c.create_rectangle(x*20, y*20, x*20+20, y*20+20, fill=canvas[x,y], width=0)

def generate():
    global canvas
    canvas = generate_art()
    draw(canvas)

def save_image():
    if canvas == None:
        messagebox.showwarning(message='An image has not been generated. Press the Generate Art button to generate an image.')
        return
    fig, ax = plt.subplots()

    # Create a Rectangle patch (x, y, width, height)
    for y in range(height):
        for x in range(width):
            square = patches.Rectangle((x, y), 1, 1, linewidth=0, facecolor=canvas[x, y])

            # Add the patch to the Axes
            ax.add_patch(square)

    # Set axis limits and aspect ratio for a clear view
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal', adjustable='box')
    ax.set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.savefig(filedialog.asksaveasfilename(title='Select image file name', filetypes=(('PNG files', '*.png'),)), bbox_inches='tight', pad_inches=0)

root = Tk()
f = Frame(root)
f.grid(sticky='nwes')
c = Canvas(f, width=width*20, height=height*20)
c.grid(column=0, row=0, columnspan=2)
Button(f, text='Generate Art', command=generate).grid(column=0, row=1)
Button(f, text='Save Art', command=save_image).grid(column=1, row=1)
root.mainloop()