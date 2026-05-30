"""Sound Mimic, by Al Sweigart al@inventwithpython.com
A pattern-matching game with sounds. Try to memorize an increasingly
longer and longer pattern of letters. Inspired by the electronic game,
Simon.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, beginner, game"""

import random, sys, time
import pygame as pg
from pygame.locals import *

pg.init()
sounds = []
for i in 'ASDF':
    sounds.append(pg.mixer.Sound(f'sound{i}.wav'))
colors = [(255, 0, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255)]

pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)

def replace_color(surface, color):
    with pg.PixelArray(surface) as pixel_array:
        # Replace all pixels of find_color with replace_color
        pixel_array.replace((255, 255, 255), color[::-1])
    # Delete the PixelArray to unlock the surface for blitting
    del pixel_array
    return surface

def render_text(text, pos, font=font):
    pos_counter = 0
    for i in text:
        for j in i[0]:
            if j.lower() in 'abcdefghijklmnopqrstuvwxyz!?\', 1234567890.%:;()':
                text_surface = font.render(j, True, i[1])
                screen.blit(text_surface, (pos[0] + pos_counter, pos[1]))
                pos_counter += text_surface.get_rect().width
            elif j == '#':
                pg.draw.rect(screen, i[1], pg.Rect(pos[0] + pos_counter, pos[1], 35, 35))
                pos_counter += 35

            else:
                continue

def render_text_basic(text, pos, font=font, color=(255, 255, 255)):
    render_text(((text, color),), pos, font)

def render_text_center(text, pos, color=(255, 255, 255), font=font):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    width = rect.width/2
    height = rect.height/2
    screen.blit(text_surface, (pos[0]-width,  pos[1]-height))

screen = pg.display.set_mode((500, 200))
pg.display.set_caption('Sound Mimic')
block = pg.image.load('block.png')
start = True
while start:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == K_SPACE:
                start = False
    screen.fill((0, 0, 0))
    render_text_basic('Welcome to Sound Mimic!', (0, 0))
    render_text_basic('Try to memorize a pattern of red, yellow, green, and blue squares', (0, 50), smallfont)
    render_text_basic('(each with its own sound) as it gets longer and longer.', (0, 75), smallfont)
    render_text_basic('You can use the buttons or keyboard to enter the pattern.', (0, 100), smallfont)
    render_text_basic('Press SPACE to start!', (0, 125))
    render_text_basic('This game is inspired by Al Sweigart\'s Sound Mimic.', (0, 175), smallfont)
    pg.display.update()

while True:
    correct = False
    pattern = []
    while True:
        pattern.append(random.randint(0, 3))
        for k, i in enumerate(pattern):
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pg.quit()
                    exit()
            screen.fill((0, 0, 0))
            render_text_basic(('Correct!' if correct else ''), (0, 0))
            render_text_basic('Pattern:', (0, 50 if correct else 0))
            sounds[i].play()
            render_text([('#', colors[j]) for j in (pattern[:k+1])[-14:]], (0, 100 if correct else 50))
            pg.display.update()
            time.sleep(sounds[i].get_length())

        clock = pg.time.Clock()
        for i in range(60):
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pg.quit()
                    exit()
            screen.fill((0, 0, 0))
            render_text_basic(('Correct!' if correct else ''), (0, 0))
            render_text_basic('Pattern:', (0, 50 if correct else 0))
            render_text([('#', colors[j]) for j in pattern[-14:]], (0, 100 if correct else 50))
            pg.display.update()
            clock.tick(60)

        entered_pattern = []
        entering = True
        while entering:
            x_zone = -1
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        exit()
                    elif event.key in (K_a, K_b, K_c, K_d):
                        entered_pattern.append([K_a, K_b, K_c, K_d].index(event.key))
                        x_zone = [K_a, K_b, K_c, K_d].index(event.key)
                    elif event.key == K_BACKSPACE:
                        try:
                            entered_pattern.pop()
                        except:
                            pass
                    elif event.key == K_RETURN:
                        entering = False
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y >= 100:
                        x_zone = x // 100
                        if x_zone in range(4):
                            entered_pattern.append(x_zone)
                        elif x_zone == 4:
                            y_zone = y // 50 - 2
                            if y_zone == 0:
                                try:
                                    entered_pattern.pop()
                                except:
                                    pass
                            elif y_zone == 1:
                                entering = False
            screen.fill((0, 0, 0))
            render_text_basic('Enter the pattern:', (0, 0))
            render_text([('#', colors[j]) for j in entered_pattern[-14:]], (0, 50))
            for i in range(4):
                pg.draw.rect(screen, colors[i], pg.Rect(i*100, 100, 100, 100))
                pg.draw.rect(screen, (255, 255, 255), pg.Rect(i*100, 100, 100, 100), width=5)
                render_text_center('ABCD'[i], (i*100+50, 150), color=(0, 0, 0))
            pg.draw.rect(screen, (255, 255, 255), pg.Rect(400, 100, 100, 50), width=5)
            pg.draw.rect(screen, (255, 255, 255), pg.Rect(400, 150, 100, 50), width=5)
            render_text_basic('Delete', (400, 110))
            render_text_basic('Enter', (400, 160))
            pg.display.update()
            if x_zone in range(4):
                sounds[x_zone].play()
                time.sleep(sounds[x_zone].get_length())
            clock.tick(60)

        if entered_pattern != pattern:
            break
        else:
            correct = True

    end = True
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    end = False
        screen.fill((0, 0, 0))
        render_text_basic('Incorrect!', (0, 0))
        render_text_basic(f'You scored {len(pattern) - 1} points.', (0, 50))
        render_text_basic('Press SPACE to play again.', (0, 100))
        pg.display.update()