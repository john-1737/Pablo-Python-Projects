"""Langton's Ant, by Al Sweigart al@inventwithpython.com
A cellular automata animation. Press Ctrl-C to stop.
More info: https://en.wikipedia.org/wiki/Langton%27s_ant
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, artistic, bext, simulation"""

import copy, random, sys, time
import pygame as pg
from pygame.locals import *

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

# Set up the constants:
WIDTH, HEIGHT = 80, 50
# We can't print to the last column on Windows without it adding a
# newline automatically, so reduce the width by one:
WIDTH -= 1
HEIGHT -= 1  # Adjustment for the quit message at the bottom.

NUMBER_OF_ANTS = 10  # (!) Try changing this to 1 or 50.
PAUSE_AMOUNT = 0.1  # (!) Try changing this to 1.0 or 0.0.

# (!) Try changing these to make the ants look different:
ANT_UP = '^'
ANT_DOWN = 'v'
ANT_LEFT = '<'
ANT_RIGHT = '>'

# (!) Try changing these colors to one of 'black', 'red', 'green',
# 'yellow', 'blue', 'purple', 'cyan', or 'white'. (These are the only
# colors that the bext module supports.)
BLACK_TILE = (0, 0, 0)
WHITE_TILE = (255, 0, 0)

NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'


def main():
    global screen, ANT_UP, ANT_DOWN, ANT_LEFT, ANT_RIGHT, font, smallfont
    # Create a new board data structure:
    board = {'width': WIDTH, 'height': HEIGHT}

    # Create ant data structures:
    ants = []

    # Keep track of which tiles have changed and need to be redrawn on
    # the screen:
    changedTiles = []
    pg.init()
    screen = pg.display.set_mode((WIDTH*15, HEIGHT*15+100))
    pg.display.set_caption('Langton\'s Ant')
    ANT_UP = pg.image.load('arrow.png').convert_alpha()
    ANT_RIGHT = pg.transform.rotate(ANT_UP, 90)
    ANT_DOWN = pg.transform.rotate(ANT_UP, 180)
    ANT_LEFT = pg.transform.rotate(ANT_UP, 270)
    pg.font.init()
    font = pg.font.SysFont(None, 48)
    smallfont = pg.font.SysFont(None, 24)
    clock = pg.time.Clock()
    fps = 10
    while True:
        running = True
        while running:
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
                    elif event.key == K_BACKSPACE:
                        board = {'width': WIDTH, 'height': HEIGHT}
                        ants = []
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if y <= HEIGHT*15:
                            try:
                                board[x//15, y//15] = not board[x//15, y//15]
                            except:
                                board[x//15, y//15] = True
                    elif event.pos[1] <= HEIGHT*15:
                        x, y = event.pos
                        ant_is_here = False
                        for i in ants:
                            if i['x'] == x//15 and i['y'] == y//15:
                                ant_is_here = True
                                ant_here = i
                            else:
                                ant_is_here = False
                        if event.button == 2:
                            if ant_is_here:
                                ants.remove(ant_here)
                            else:
                                ants.append({
            'x': x//15,
            'y': y//15,
            'direction': NORTH,
        })
                        elif event.button == 4 and ant_is_here:
                            dir = ant_here['direction']
                            ant_here['direction'] = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}[dir]
                        elif event.button == 5 and ant_is_here:
                            dir = ant_here['direction']
                            ant_here['direction'] = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}[dir]

            screen.fill((0, 0, 0))
            displayBoard(board, ants, changedTiles)
            render_text('Click square with left mouse button to change tile color.', (0, HEIGHT*15), True)
            render_text('Click square with scroll wheel to add or remove ant.', (0, HEIGHT*15+25), True)
            render_text('Use scroll wheel to change ant direction.', (0, HEIGHT*15+50), True)
            render_text('Press SPACE to start simulation.', (0, HEIGHT*15+75), True)
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
                    elif event.key == pg.K_UP:
                        fps += 1
                        if fps == 61:
                            fps = 1
                    elif event.key == pg.K_DOWN:
                        fps -= 1
                        if fps == 0:
                            fps = 60
            screen.fill((0, 0, 0))
            displayBoard(board, ants, changedTiles)
            render_text(f'FPS: {fps}', (0, HEIGHT*15))
            render_text('Use up/down keys to change FPS.', (0, HEIGHT*15+50), True)
            render_text('Press SPACE to stop simulation.', (0, HEIGHT*15+75), True)
            pg.display.update()
            clock.tick(fps)
            changedTiles = []

            # nextBoard is what the board will look like on the next step in
            # the simulation. Start with a copy of the current step's board:
            nextBoard = copy.copy(board)

            # Run a single simulation step for each ant:
            for ant in ants:
                if board.get((ant['x'], ant['y']), False) == True:
                    nextBoard[(ant['x'], ant['y'])] = False
                    # Turn clockwise:
                    if ant['direction'] == NORTH:
                        ant['direction'] = EAST
                    elif ant['direction'] == EAST:
                        ant['direction'] = SOUTH
                    elif ant['direction'] == SOUTH:
                        ant['direction'] = WEST
                    elif ant['direction'] == WEST:
                        ant['direction'] = NORTH
                else:
                    nextBoard[(ant['x'], ant['y'])] = True
                    # Turn counter clockwise:
                    if ant['direction'] == NORTH:
                        ant['direction'] = WEST
                    elif ant['direction'] == WEST:
                        ant['direction'] = SOUTH
                    elif ant['direction'] == SOUTH:
                        ant['direction'] = EAST
                    elif ant['direction'] == EAST:
                        ant['direction'] = NORTH
                changedTiles.append((ant['x'], ant['y']))

                # Move the ant forward in whatever direction it's facing:
                if ant['direction'] == NORTH:
                    ant['y'] -= 1
                if ant['direction'] == SOUTH:
                    ant['y'] += 1
                if ant['direction'] == WEST:
                    ant['x'] -= 1
                if ant['direction'] == EAST:
                    ant['x'] += 1

                # If the ant goes past the edge of the screen,
                # it should wrap around to other side.
                ant['x'] = ant['x'] % WIDTH
                ant['y'] = ant['y'] % HEIGHT

                changedTiles.append((ant['x'], ant['y']))

            board = nextBoard

def render_text(text, pos, small=False):
    if small:
        text_surface = smallfont.render(text, True, (255, 255, 255))
    else:
        text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, pos)

def displayBoard(board, ants, changedTiles):
    """Displays the board and ants on the screen. The changedTiles
    argument is a list of (x, y) tuples for tiles on the screen that
    have changed and need to be redrawn."""

    # Draw the board data structure:
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board.get((x, y), False):
                pg.draw.rect(screen, BLACK_TILE, pg.Rect(x*15, y*15, 15, 15))
            else:
                pg.draw.rect(screen, WHITE_TILE, pg.Rect(x*15, y*15, 15, 15))
            pg.draw.rect(screen, (100, 100, 100), pg.Rect(x * 15, y * 15, 15, 15), 1)

            for ant in ants:
                if (x, y) == (ant['x'], ant['y']):
                    if ant['direction'] == NORTH:
                        screen.blit(ANT_UP, (x*15, y*15))
                    elif ant['direction'] == SOUTH:
                        screen.blit(ANT_DOWN, (x*15, y*15))
                    elif ant['direction'] == EAST:
                        screen.blit(ANT_RIGHT, (x*15, y*15))
                    elif ant['direction'] == WEST:
                        screen.blit(ANT_LEFT, (x*15, y*15))
                    break


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Langton's Ant, by Al Sweigart al@inventwithpython.com")
        sys.exit()  # When Ctrl-C is pressed, end the program.