"""Digital Clock, by Al Sweigart al@inventwithpython.com
Displays a digital clock of the current time with a seven-segment
display. Press Ctrl-C to stop.
More info at https://en.wikipedia.org/wiki/Seven-segment_display
Requires sevseg.py to be in the same folder.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, artistic"""

import sys, time
import pygame as pg
from pygame.locals import *

screen = pg.display.set_mode((282, 190))
pg.display.set_caption('Digital Clock')
clockface = pg.image.load('clockface.png').convert_alpha()
digits = []
for i in range(10):
    digits.append(pg.image.load(f'digit{i}.png').convert_alpha())
colon = pg.image.load('colon.png').convert_alpha()

while True:  # Main program loop.
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    screen.blit(clockface, (0, 0))

    # Get the current time from the computer's clock:
    currentTime = time.localtime()
    # % 12 so we use a 12-hour clock, not 24:
    hours = str(currentTime.tm_hour % 12)
    if hours == '0':
        hours = '12'  # 12-hour clocks show 12:00, not 00:00.
    minutes = str(currentTime.tm_min)
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    # Get the digit strings from the sevseg module:
    for i, j in enumerate(hours + minutes):
        screen.blit(digits[int(j)], (38+(i*50), 39))
    screen.blit(colon, (137, 39))
    pg.display.update()
