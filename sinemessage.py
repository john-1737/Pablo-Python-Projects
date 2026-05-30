"""Sine Message, by Al Sweigart al@inventwithpython.com
Create a sine-wavy message.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, artistic"""

import math, shutil, sys, time
import pygame as pg
from pygame.locals import *

# Get the size of the terminal window:
WIDTH, HEIGHT = shutil.get_terminal_size()
# We can't print to the last column on Windows without it adding a
# newline automatically, so reduce the width by one:
WIDTH -= 1

screen = pg.display.set_mode((500, 500))
pg.display.set_caption('Sine Message')
pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)
clock = pg.time.Clock()

def render_text(text, pos, font=smallfont, color=(255, 255, 255), bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

step = 0.0  # The "step" determines how far into the sine wave we are.
bottom = 0
message = ''
steps = []
cosine = False
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == K_BACKSPACE:
                message = message[:-1]
            elif event.key == K_LEFT:
                cosine = False
            elif event.key == K_RIGHT:
                cosine = True
        elif event.type == TEXTINPUT:
            message += event.text
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if y >= 75 and y <= 100:
                x = x // 125
                if x == 2:
                    cosine = False
                elif x == 3:
                    cosine = True
    screen.fill((0, 0, 0))
    if bottom == 25:
        bottom = 0
    if bottom == 0:
        step += 0.25
        steps.insert(0, step)
    bottom += 1
    while len(steps) > 24:
        del steps[-1]
    for i, j in enumerate(steps):
        sinOfStep = math.cos(j) if cosine else math.sin(j)
        # Sine goes from -1.0 to 1.0, so we need to change it by a multiplier:
        multiplier = min((250 - smallfont.render(message, True, (255, 255, 255)).get_rect().width / 2), 500)
        padding = int((sinOfStep + 1) * multiplier)
        render_text(message, (padding, 600-bottom-i*25))
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, 0, 500, 100))
    render_text('Enter your message:', (0, 0))
    render_text(message, (0, 25))
    render_text('|', (smallfont.render(message, True, (255, 255, 255)).get_rect().width, 25), color=(0, 0, 255))
    if len(message) == 0:
        render_text('You must type something for your message to display.', (0, 50), color=(255, 0, 0))
    elif smallfont.render(message, True, (255, 255, 255)).get_rect().width > 500:
        render_text('Your message is too long. It will not display properly.', (0, 50), color=(255, 0, 0))
    render_text('Select message format:', (0, 75))
    pg.draw.rect(screen, (0, 0, 255), pg.Rect(375 if cosine else 250, 75, 125, 25))
    render_text('Sine (key: <)', (250, 75))
    render_text('Cosine (key: >)', (375, 75))
    pg.display.update()
    clock.tick(60)