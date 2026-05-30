"""Rotating Cube, by Al Sweigart al@inventwithpython.com
A rotating cube animation. Press Ctrl-C to stop.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, artistic, math"""

# This program MUST be run in a Terminal/Command Prompt window.

import math, time, sys
import pygame as pg
from pygame.locals import *

# Set up the constants:
PAUSE_AMOUNT = 10  # Pause length of one-tenth of a second.
WIDTH, HEIGHT = 1000, 1000
SCALEX = (WIDTH - 4) // 8
SCALEY = (HEIGHT - 4) // 8
TRANSLATEX = (WIDTH - 4) // 2
TRANSLATEY = (HEIGHT - 4) // 2

# (!) Try changing this to '#' or '*' or some other character:
LINE_CHAR = chr(9608)  # Character 9608 is a solid block.

# (!) Try setting two of these values to zero to rotate the cube only
# along a single axis:
X_ROTATE_SPEED = 0.03
Y_ROTATE_SPEED = 0.08
Z_ROTATE_SPEED = 0.13

# This program stores XYZ coordinates in lists, with the X coordinate
# at index 0, Y at 1, and Z at 2. These constants make our code more
# readable when accessing the coordinates in these lists.
X = 0
Y = 1
Z = 2



def rotatePoint(x, y, z, ax, ay, az):
    """Returns an (x, y, z) tuple of the x, y, z arguments rotated.

    The rotation happens around the 0, 0, 0 origin by angles
    ax, ay, az (in radians).
        Directions of each axis:
         -y
          |
          +-- +x
         /
        +z
    """

    # Rotate around x axis:
    rotatedX = x
    rotatedY = (y * math.cos(ax)) - (z * math.sin(ax))
    rotatedZ = (y * math.sin(ax)) + (z * math.cos(ax))
    x, y, z = rotatedX, rotatedY, rotatedZ

    # Rotate around y axis:
    rotatedX = (z * math.sin(ay)) + (x * math.cos(ay))
    rotatedY = y
    rotatedZ = (z * math.cos(ay)) - (x * math.sin(ay))
    x, y, z = rotatedX, rotatedY, rotatedZ

    # Rotate around z axis:
    rotatedX = (x * math.cos(az)) - (y * math.sin(az))
    rotatedY = (x * math.sin(az)) + (y * math.cos(az))
    rotatedZ = z

    return (rotatedX, rotatedY, rotatedZ)


def adjustPoint(point):
    """Adjusts the 3D XYZ point to a 2D XY point fit for displaying on
    the screen. This resizes this 2D point by a scale of SCALEX and
    SCALEY, then moves the point by TRANSLATEX and TRANSLATEY."""
    return (int(point[X] * SCALEX + TRANSLATEX),
            int(point[Y] * SCALEY + TRANSLATEY))


"""CUBE_CORNERS stores the XYZ coordinates of the corners of a cube.
The indexes for each corner in CUBE_CORNERS are marked in this diagram:
      0---1
     /|  /|
    2---3 |
    | 4-|-5
    |/  |/
    6---7"""
CUBE_CORNERS = [[-1, -1, -1], # Point 0
                [ 1, -1, -1], # Point 1
                [-1, -1,  1], # Point 2
                [ 1, -1,  1], # Point 3
                [-1,  1, -1], # Point 4
                [ 1,  1, -1], # Point 5
                [-1,  1,  1], # Point 6
                [ 1,  1,  1]] # Point 7
# rotatedCorners stores the XYZ coordinates from CUBE_CORNERS after
# they've been rotated by rx, ry, and rz amounts:
rotatedCorners = [None, None, None, None, None, None, None, None]
# Rotation amounts for each axis:
xRotation = 0.0
yRotation = 0.0
zRotation = 0.0

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Rotating Cube')
clock = pg.time.Clock()

def render_text(text, pos, font=font, color=(255, 255, 255), bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

while True:
    start = True
    while start:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    start = False
                elif event.key == K_UP:
                    Y_ROTATE_SPEED += 0.01
                elif event.key == K_DOWN:
                    Y_ROTATE_SPEED -= 0.01
                elif event.key == K_LEFT:
                    X_ROTATE_SPEED -= 0.01
                elif event.key == K_RIGHT:
                    X_ROTATE_SPEED += 0.01
                elif event.key == K_w:
                    Z_ROTATE_SPEED += 0.01
                elif event.key == K_s:
                    Z_ROTATE_SPEED -= 0.01
                elif event.key == K_BACKSPACE:
                    xRotation = 0.0
                    yRotation = 0.0
                    zRotation = 0.0
        X_ROTATE_SPEED = round(X_ROTATE_SPEED, 2)
        Y_ROTATE_SPEED = round(Y_ROTATE_SPEED, 2)
        Z_ROTATE_SPEED = round(Z_ROTATE_SPEED, 2)
        # Rotate the cube along different axes by different amounts:
        for i in range(len(CUBE_CORNERS)):
            x = CUBE_CORNERS[i][X]
            y = CUBE_CORNERS[i][Y]
            z = CUBE_CORNERS[i][Z]
            rotatedCorners[i] = rotatePoint(x, y, z, xRotation,
                yRotation, zRotation)

        # Get the points of the cube lines:
        screen.fill((0, 0, 0))
        for fromCornerIndex, toCornerIndex in ((0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 7), (7, 6), (6, 4)):
            fromX, fromY = adjustPoint(rotatedCorners[fromCornerIndex])
            toX, toY = adjustPoint(rotatedCorners[toCornerIndex])
            pg.draw.line(screen, (255, 255, 255), (fromX, fromY), (toX, toY), 10)
        render_text(f'X rotation speed = {X_ROTATE_SPEED} (change with left/right keys)', (0, 0))
        render_text(f'Y rotation speed = {Y_ROTATE_SPEED} (change with up/down keys)', (0, 50))
        render_text(f'Z rotation speed = {Z_ROTATE_SPEED} (change with W/S keys)', (0, 100))
        render_text('Press SPACE to start.', (0, 150))
        render_text('Press BACKSPACE to reset cube.', (0, 200))
        pg.display.update()

    running = True
    while running:  # Main program loop.
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    running = False
        # Rotate the cube along different axes by different amounts:
        xRotation += X_ROTATE_SPEED
        yRotation += Y_ROTATE_SPEED
        zRotation += Z_ROTATE_SPEED
        for i in range(len(CUBE_CORNERS)):
            x = CUBE_CORNERS[i][X]
            y = CUBE_CORNERS[i][Y]
            z = CUBE_CORNERS[i][Z]
            rotatedCorners[i] = rotatePoint(x, y, z, xRotation,
                yRotation, zRotation)

        # Get the points of the cube lines:
        screen.fill((0, 0, 0))
        for fromCornerIndex, toCornerIndex in ((0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 7), (7, 6), (6, 4)):
            fromX, fromY = adjustPoint(rotatedCorners[fromCornerIndex])
            toX, toY = adjustPoint(rotatedCorners[toCornerIndex])
            pg.draw.line(screen, (255, 255, 255), (fromX, fromY), (toX, toY), 10)
        render_text(f'X rotation speed = {X_ROTATE_SPEED}', (0, 0))
        render_text(f'Y rotation speed = {Y_ROTATE_SPEED}', (0, 50))
        render_text(f'Z rotation speed = {Z_ROTATE_SPEED}', (0, 100))
        render_text('Press SPACE to stop.', (0, 150))
        pg.display.update()
        clock.tick(PAUSE_AMOUNT)  # Pause for a bit.
