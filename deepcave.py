"""Deep Cave, by Al Sweigart al@inventwithpython.com
An animation of a deep cave that goes forever into the earth.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, scrolling, artistic"""


import random, sys, time
import pygame as pg
from pygame.locals import *

# Set up the constants:
WIDTH = 70  # (!) Try changing this to 10 or 30.
PAUSE_AMOUNT = 0.05  # (!) Try changing this to 0 or 1.0.
SEGMENT_HEIGHT = 20

time.sleep(2)

leftWidth = 20
gapWidth = 10
screen = pg.display.set_mode((700, 400))
pg.display.set_caption('Deep Cave')
cave_segments = []
segment_clock = 0
clock = pg.time.Clock()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pg.quit()
            exit()
    if segment_clock == 0:
        cave_segments.append((leftWidth, gapWidth))
        diceRoll = random.randint(1, 6)
        if diceRoll == 1 and leftWidth > 1:
            leftWidth = leftWidth - 1  # Decrease left side width.
        elif diceRoll == 2 and leftWidth + gapWidth < WIDTH - 1:
            leftWidth = leftWidth + 1  # Increase left side width.
        else:
            pass  # Do nothing; no change in left side width.
        # Adjust the gap width:
        # (!) Try uncommenting out all of the following code:
        diceRoll = random.randint(1, 6)
        if diceRoll == 1 and gapWidth > 1:
           gapWidth = gapWidth - 1  # Decrease gap width.
        elif diceRoll == 2 and leftWidth + gapWidth < WIDTH - 1:
           gapWidth = gapWidth + 1  # Increase gap width.
        else:
           pass  # Do nothing; no change in gap width.

    # Display the tunnel segment:
    screen.fill((0, 0, 255))
    for i, j in enumerate(cave_segments[::-1]):
        pg.draw.rect(screen, (150, 75, 0), pg.Rect(0, 400-segment_clock-i*SEGMENT_HEIGHT, 700, SEGMENT_HEIGHT))
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(10*j[0], 400-segment_clock-i*SEGMENT_HEIGHT, 10*j[1], SEGMENT_HEIGHT))
        rightWidth = WIDTH - gapWidth - leftWidth

    segment_clock += 1
    segment_clock %= SEGMENT_HEIGHT

    pg.display.update()
    clock.tick(60)


