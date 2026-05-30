import pygame as pg
from pygame.locals import *
from random import randint, choice

def draw_ball(ball):
    pg.draw.circle(screen, ball['color'], (ball['x'], ball['y']), 10, width=0, )

def move_ball(ball):
    ball['x'] += ball['xv']
    ball['y'] += ball['yv']
    if ball['x'] >= 800 or ball['x'] <= 0:
        ball['xv'] = -ball['xv']
    if ball['y'] >= 400 or ball['y'] <= 0:
        ball['yv'] = -ball['yv']

screen = pg.display.set_mode((800, 400))
pg.display.set_caption('Bounce')
balls = []
colors = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'orange', 'purple', 'lightgreen', 'pink']
for i in range(10):
    balls.append({'x': randint(0, 800), 'y': randint(0, 400), 'xv': choice([-3, -2, -1, 1, 2, 3]), 'yv': choice([-3, -2, -1, 1, 2, 3]), 'color': colors[i]})

clock = pg.time.Clock()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    screen.fill((0,0,0))
    for i in balls:
        move_ball(i)
        draw_ball(i)
    pg.display.update()
    clock.tick(60)