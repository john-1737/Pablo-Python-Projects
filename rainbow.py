"""Rainbow, by Al Sweigart al@inventwithpython.com
Shows a simple rainbow animation. Press Ctrl-C to stop.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, artistic, bext, beginner, scrolling"""

import time, sys

import pygame as pg
from pygame.locals import *
screen = pg.display.set_mode((400, 400))
pg.display.set_caption('Rainbow')

indent = 0  # How many spaces to indent.
indentIncreasing = True  # Whether the indentation is increasing or not.
spaces = []
for i in range(20):
    spaces.append(indent)
    if indentIncreasing:
        # Increase the number of spaces:
        indent = indent + 1
        if indent == 28:  # (!) Change this to 10 or 30.
            # Change direction:
            indentIncreasing = False
    else:
        # Decrease the number of spaces:
        indent = indent - 1
        if indent == 0:
            # Change direction:
            indentIncreasing = True

while True:  # Main program loop.
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
        
    spaces.append(indent)
    screen.fill((0, 0, 0))
    for i, j in enumerate(spaces[-20:]):
        for k, l in enumerate(('red', 'yellow', 'green', 'blue', 'cyan', 'purple')):
            pg.draw.rect(screen, l, pg.Rect(j*10+k*20, i*20, 20, 20))
    pg.display.update()

    if indentIncreasing:
        # Increase the number of spaces:
        indent = indent + 1
        if indent == 28:  # (!) Change this to 10 or 30.
            # Change direction:
            indentIncreasing = False
    else:
        # Decrease the number of spaces:
        indent = indent - 1
        if indent == 0:
            # Change direction:
            indentIncreasing = True

    time.sleep(0.02)  # Add a slight pause.
