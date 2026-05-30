"""Hourglass, by Al Sweigart al@inventwithpython.com
An animation of an hourglass with falling sand. Press Ctrl-C to stop.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, artistic, bext, simulation"""

import random, sys, time
import pygame as pg
from pygame.locals import *

# Set up the constants:
PAUSE_LENGTH = 5  # (!) Try changing this to 0.0 or 1.0.
# (!) Try changing this to any number between 0 and 100:
WIDE_FALL_CHANCE = 50

SCREEN_WIDTH = 79
SCREEN_HEIGHT = 25
X = 0  # The index of X values in an (x, y) tuple is 0.
Y = 1  # The index of Y values in an (x, y) tuple is 1.
SAND = (252, 202, 39)
WHITE = (255, 255, 255)

# Set up the walls of the hour glass:
HOURGLASS = set()  # Has (x, y) tuples for where hourglass walls are.
# (!) Try commenting out some HOURGLASS.add() lines to erase walls:
for i in range(18, 37):
    HOURGLASS.add((i, 1))  # Add walls for the top cap of the hourglass.
    HOURGLASS.add((i, 23))  # Add walls for the bottom cap.
for i in range(1, 5):
    HOURGLASS.add((18, i))  # Add walls for the top left straight wall.
    HOURGLASS.add((36, i))  # Add walls for the top right straight wall.
    HOURGLASS.add((18, i + 19))  # Add walls for the bottom left.
    HOURGLASS.add((36, i + 19))  # Add walls for the bottom right.
for i in range(8):
    HOURGLASS.add((19 + i, 5 + i))  # Add the top left slanted wall.
    HOURGLASS.add((35 - i, 5 + i))  # Add the top right slanted wall.
    HOURGLASS.add((25 - i, 13 + i))  # Add the bottom left slanted wall.
    HOURGLASS.add((29 + i, 13 + i))  # Add the bottom right slanted wall.

# Set up the initial sand at the top of the hourglass:
INITIAL_SAND = set()
for y in range(8):
    for x in range(19 + y, 36 - y):
        INITIAL_SAND.add((x, y + 4))


def main():
    global screen, clock, hourglass
    screen = pg.display.set_mode((190, 345))
    pg.display.set_caption('Hourglass')
    clock = pg.time.Clock()
    hourglass = pg.image.load('hourglass.png').convert_alpha()

    while True:  # Main program loop.
        allSand = list(INITIAL_SAND)

        runHourglassSimulation(allSand)


def runHourglassSimulation(allSand):
    """Keep running the sand falling simulation until the sand stops
    moving."""
    while True:  # Keep looping until sand has run out.
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    return
        random.shuffle(allSand)  # Random order of grain simulation.

        sandMovedOnThisStep = False
        for i, sand in enumerate(allSand):
            if sand[Y] == SCREEN_HEIGHT - 1:
                # Sand is on the very bottom, so it won't move:
                continue

            # If nothing is under this sand, move it down:
            noSandBelow = (sand[X], sand[Y] + 1) not in allSand
            noWallBelow = (sand[X], sand[Y] + 1) not in HOURGLASS
            canFallDown = noSandBelow and noWallBelow

            if canFallDown:
                # Draw the sand in its new position down one space:

                # Set the sand in its new position down one space:
                allSand[i] = (sand[X], sand[Y] + 1)
                sandMovedOnThisStep = True
            else:
                # Check if the sand can fall to the left:
                belowLeft = (sand[X] - 1, sand[Y] + 1)
                noSandBelowLeft = belowLeft not in allSand
                noWallBelowLeft = belowLeft not in HOURGLASS
                left = (sand[X] - 1, sand[Y])
                noWallLeft = left not in HOURGLASS
                notOnLeftEdge = sand[X] > 0
                canFallLeft = (noSandBelowLeft and noWallBelowLeft
                    and noWallLeft and notOnLeftEdge)

                # Check if the sand can fall to the right:
                belowRight = (sand[X] + 1, sand[Y] + 1)
                noSandBelowRight = belowRight not in allSand
                noWallBelowRight = belowRight not in HOURGLASS
                right = (sand[X] + 1, sand[Y])
                noWallRight = right not in HOURGLASS
                notOnRightEdge = sand[X] < SCREEN_WIDTH - 1
                canFallRight = (noSandBelowRight and noWallBelowRight
                    and noWallRight and notOnRightEdge)

                # Set the falling direction:
                fallingDirection = None
                if canFallLeft and not canFallRight:
                    fallingDirection = -1  # Set the sand to fall left.
                elif not canFallLeft and canFallRight:
                    fallingDirection = 1  # Set the sand to fall right.
                elif canFallLeft and canFallRight:
                    # Both are possible, so randomly set it:
                    fallingDirection = random.choice((-1, 1))

                # Check if the sand can "far" fall two spaces to
                # the left or right instead of just one space:
                if random.random() * 100 <= WIDE_FALL_CHANCE:
                    belowTwoLeft = (sand[X] - 2, sand[Y] + 1)
                    noSandBelowTwoLeft = belowTwoLeft not in allSand
                    noWallBelowTwoLeft = belowTwoLeft not in HOURGLASS
                    notOnSecondToLeftEdge = sand[X] > 1
                    canFallTwoLeft = (canFallLeft and noSandBelowTwoLeft
                        and noWallBelowTwoLeft and notOnSecondToLeftEdge)

                    belowTwoRight = (sand[X] + 2, sand[Y] + 1)
                    noSandBelowTwoRight = belowTwoRight not in allSand
                    noWallBelowTwoRight = belowTwoRight not in HOURGLASS
                    notOnSecondToRightEdge = sand[X] < SCREEN_WIDTH - 2
                    canFallTwoRight = (canFallRight
                        and noSandBelowTwoRight and noWallBelowTwoRight
                        and notOnSecondToRightEdge)

                    if canFallTwoLeft and not canFallTwoRight:
                        fallingDirection = -2
                    elif not canFallTwoLeft and canFallTwoRight:
                        fallingDirection = 2
                    elif canFallTwoLeft and canFallTwoRight:
                        fallingDirection = random.choice((-2, 2))

                if fallingDirection == None:
                    # This sand can't fall, so move on.
                    continue

                # Move the grain of sand to its new position:
                allSand[i] = (sand[X] + fallingDirection, sand[Y] + 1)
                sandMovedOnThisStep = True

        screen.fill(WHITE)
        screen.blit(hourglass, (0, 0))
        for i in allSand:
            pg.draw.rect(screen, SAND, pg.Rect(i[0] * 10-180, i[1] * 15-15, 10, 15))
            print('Sand drawn at', i[0], i[1])
        pg.display.update()
        clock.tick(PAUSE_LENGTH)  # Pause after this

        # If no sand has moved on this step, reset the hourglass:
        if not sandMovedOnThisStep:
            time.sleep(2)
            break  # Break out of main simulation loop.


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # When Ctrl-C is pressed, end the program.
