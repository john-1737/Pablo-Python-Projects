"""Bouncing DVD Logo, by Al Sweigart al@inventwithpython.com
A bouncing DVD logo animation. You have to be "of a certain age" to
appreciate this. Press Ctrl-C to stop.

NOTE: Do not resize the terminal window while this program is running.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, artistic, bext"""

import sys, random, time
import pygame as pg
from pygame.locals import *

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 24)

# Set up the constants:
WIDTH, HEIGHT = 1500, 900
# We can't print to the last column on Windows without it adding a
# newline automatically, so reduce the width by one:

NUMBER_OF_LOGOS = 1000000  # (!) Try changing this to 1 or 100.
PAUSE_AMOUNT = 1000  # (!) Try changing this to 1.0 or 0.0.
# (!) Try changing this list to fewer colors:
COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

UP_RIGHT   = 'ur'
UP_LEFT    = 'ul'
DOWN_RIGHT = 'dr'
DOWN_LEFT  = 'dl'
DIRECTIONS = (UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT)

# Key names for logo dictionaries:
COLOR = 'color'
X = 'x'
Y = 'y'
DIR = 'direction'


def main():
    global screen
    # Generate some logos.
    logos = []
    for i in range(NUMBER_OF_LOGOS):
        logos.append({COLOR: random.choice(COLORS),
                      X: random.randint(1, WIDTH - 70),
                      Y: random.randint(1, HEIGHT - 48),
                      DIR: random.choice(DIRECTIONS)})
        if logos[-1][X] % 2 == 1:
            # Make sure X is even so it can hit the corner.
            logos[-1][X] -= 1
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(f'Bouncing DVD Logo    Corner bounces: 0')
    clock = pg.time.Clock()
    cornerBounces = 0  # Count how many times a logo hits a corner.
    while True:  # Main program loop.
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        for logo in logos:  # Handle each logo in the logos list.

            originalDirection = logo[DIR]

            # See if the logo bounces off the corners:
            if logo[X] == 0 and logo[Y] == 0:
                logo[DIR] = DOWN_RIGHT
                cornerBounces += 1
            elif logo[X] == 0 and logo[Y] == HEIGHT - 1:
                logo[DIR] = UP_RIGHT
                cornerBounces += 1
            elif logo[X] == WIDTH - 3 and logo[Y] == 0:
                logo[DIR] = DOWN_LEFT
                cornerBounces += 1
            elif logo[X] == WIDTH - 3 and logo[Y] == HEIGHT - 1:
                logo[DIR] = UP_LEFT
                cornerBounces += 1

            # See if the logo bounces off the left edge:
            elif logo[X] == 0 and logo[DIR] == UP_LEFT:
                logo[DIR] = UP_RIGHT
            elif logo[X] == 0 and logo[DIR] == DOWN_LEFT:
                logo[DIR] = DOWN_RIGHT

            # See if the logo bounces off the right edge:
            # (WIDTH - 3 because 'DVD' has 3 letters.)
            elif logo[X] == WIDTH - 3 and logo[DIR] == UP_RIGHT:
                logo[DIR] = UP_LEFT
            elif logo[X] == WIDTH - 3 and logo[DIR] == DOWN_RIGHT:
                logo[DIR] = DOWN_LEFT

            # See if the logo bounces off the top edge:
            elif logo[Y] == 0 and logo[DIR] == UP_LEFT:
                logo[DIR] = DOWN_LEFT
            elif logo[Y] == 0 and logo[DIR] == UP_RIGHT:
                logo[DIR] = DOWN_RIGHT

            # See if the logo bounces off the bottom edge:
            elif logo[Y] == HEIGHT - 1 and logo[DIR] == DOWN_LEFT:
                logo[DIR] = UP_LEFT
            elif logo[Y] == HEIGHT - 1 and logo[DIR] == DOWN_RIGHT:
                logo[DIR] = UP_RIGHT

            if logo[DIR] != originalDirection:
                # Change color when the logo bounces:
                logo[COLOR] = random.choice(COLORS)

            # Move the logo. (X moves by 2 because the terminal
            # characters are twice as tall as they are wide.)
            if logo[DIR] == UP_RIGHT:
                logo[X] += 1
                logo[Y] -= 1
            elif logo[DIR] == UP_LEFT:
                logo[X] -= 1
                logo[Y] -= 1
            elif logo[DIR] == DOWN_RIGHT:
                logo[X] += 1
                logo[Y] += 1
            elif logo[DIR] == DOWN_LEFT:
                logo[X] -= 1
                logo[Y] += 1

        # Display number of corner bounces:
        pg.display.set_caption(f'Bouncing DVD Logo    Corner bounces: {cornerBounces}')

        for logo in logos:
            # Draw the logos at their new location:
            render_text('DVD', (logo['x'], logo['y']), color=logo[COLOR])

        sys.stdout.flush()  # (Required for bext-using programs.)
        pg.display.update()
        clock.tick(PAUSE_AMOUNT)

def render_text(text, pos, font=font, color=(255, 255, 255), bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()