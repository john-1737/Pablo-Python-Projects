"""Digital Stream, by Al Sweigart al@inventwithpython.com
A screensaver in the style of The Matrix movie's visuals.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, artistic, beginner, scrolling"""

import random, shutil, sys, time
import pygame as pg
from pygame.locals import *

pg.font.init()
font = pg.font.SysFont('Monaco', 20)
def render_text(text, pos, font=font, color=(255, 255, 255), bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

# Set up the constants:
MIN_STREAM_LENGTH = 6  # (!) Try changing this to 1 or 50.
MAX_STREAM_LENGTH = 14  # (!) Try changing this to 100.
PAUSE = 0.1  # (!) Try changing this to 0.0 or 2.0.
STREAM_CHARS = ['0', '1']  # (!) Try changing this to other characters.

# Density can range from 0.0 to 1.0:
DENSITY = 0.02  # (!) Try changing this to 0.10 or 0.30.

# Get the size of the terminal window:
WIDTH = 35
screen = pg.display.set_mode((300, 300))
pg.display.set_caption('Digital Stream')

# For each column, when the counter is 0, no stream is shown.
# Otherwise, it acts as a counter for how many times a 1 or 0
# should be displayed in that column.
columns = [0] * WIDTH
rows = []
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
        # Set up the counter for each column:
    row = ''
    for i in range(WIDTH):
        if columns[i] == 0:
            if random.random() <= DENSITY:
                # Restart a stream on this column.
                columns[i] = random.randint(MIN_STREAM_LENGTH,
                                            MAX_STREAM_LENGTH)

        # Display an empty space or a 1/0 character.
        if columns[i] > 0:
            row += str(random.choice(STREAM_CHARS))
            columns[i] -= 1
        else:
            row += ' '
    screen.fill((0, 0, 0))
    rows.append(row)
    rows = rows[-15:]
    j = 14
    for i in rows[::-1]:
        render_text(i, (0, j*20))
        j -= 1
        
    pg.display.update()
    time.sleep(PAUSE)