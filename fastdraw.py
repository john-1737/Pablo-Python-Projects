"""Fast Draw, by Al Sweigart al@inventwithpython.com
Test your reflexes to see if you're the fastest draw in the west.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, game"""

import random, sys, time
import pygame as pg
from pygame.locals import *

WHITE = (255, 255, 255)

screen = pg.display.set_mode((500, 250))
pg.display.set_caption("Fast Draw")

pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)

# Function to render text
def render_text(text, pos, font=font):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, pos)

start = True

while start:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == K_SPACE:
                start = False

    screen.fill((0, 0, 0))
    render_text('Welcome to Fast Draw!', (0, 0), smallfont)
    render_text('Time to test your reflexes and see if you are the fastest', (0, 50), smallfont)
    render_text('draw in the west!', (0, 75), smallfont)
    render_text('When you see "DRAW", you have 0.3 seconds to press SPACE.', (0, 100), smallfont)
    render_text('But you lose if you press SPACE before "DRAW" appears.', (0, 125), smallfont)
    render_text('This game is inspired by Al Sweigart\'s Fast Draw.', (0, 200), smallfont)
    render_text('Press SPACE to start!', (0, 225), smallfont)
    pg.display.update()

while True:
    wait_time = random.randint(20, 50) / 10.0
    space_pressed = False
    start_time = time.time()
    while not space_pressed:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    space_pressed = True
                    timeElapsed = -1
                    
        screen.fill((0, 0, 0))
        render_text('Get ready...', (0, 0))
        if start_time + wait_time <= time.time():
            break
        pg.display.update()

    drawTime = time.time()
    while not space_pressed:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    space_pressed = True
                    timeElapsed = time.time() - drawTime
        screen.fill((0, 0, 0))
        render_text('DRAW!', (0, 0))
        pg.display.update()


    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    running = False
        screen.fill((0, 0, 0))
        if timeElapsed == -1:
            render_text('You drew before "DRAW"', (0, 0))
            render_text('appeared! You lose.', (0, 50))
        elif timeElapsed <= 0.3:
            render_text(f'You took {round(timeElapsed, 4)} seconds', (0, 0))
            render_text('to draw.', (0, 50))
            render_text('You are the fastest draw in the', (0, 100))
            render_text('west! You win!', (0, 150))
        else:
            render_text(f'You took {round(timeElapsed, 4)} seconds', (0, 0))
            render_text('to draw. Too slow!', (0, 50))
        render_text('Press SPACE to play again.', (0, 200))
        pg.display.update()

    # print()
    # print('It is high noon...')
    # time.sleep(random.randint(20, 50) / 10.0)
    # print('DRAW!')
    # drawTime = time.time()
    # input()  # This function call doesn't return until Enter is pressed.
    # timeElapsed = time.time() - drawTime

    # if timeElapsed < 0.01:
    #     # If the player pressed Enter before DRAW! appeared, the input()
    #     # call returns almost instantly.
    #     print('You drew before "DRAW" appeared! You lose.')
    # elif timeElapsed > 0.3:
    #     timeElapsed = round(timeElapsed, 4)
    #     print('You took', timeElapsed, 'seconds to draw. Too slow!')
    # else:
    #     timeElapsed = round(timeElapsed, 4)
    #     print('You took', timeElapsed, 'seconds to draw.')
    #     print('You are the fastest draw in the west! You win!')

    # print('Enter QUIT to stop, or press Enter to play again.')
    # response = input('> ').upper()
    # if response == 'QUIT':
    #     print('Thanks for playing!')
    #     sys.exit()
