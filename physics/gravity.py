import pygame as pg
from pygame.locals import *
from math import sin, cos, radians
from matplotlib.pyplot import subplots, show
from sys import exit
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BACKGROUND = (0,0,0)
WIDTH = 1200
HEIGHT = 600
pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)

def reset_ball():
    global throwing, ball
    ball['x'] = 0
    ball['y'] = HEIGHT
    ball['speed'] = 0
    ball['fall speed'] = 0
    throwing = False

def update_ball():
    global ball
    ball['x'] += cos(radians(ball['angle']-90)) * ball['speed']
    ball['y'] += sin(radians(ball['angle']-90)) * ball['speed']
    ball['y'] -= ball['fall speed']
    ball['fall speed'] -= ball['gravity']
    if throwing:
        vys.append((sin(radians(ball['angle']-90)) * ball['speed']) - ball['fall speed'])
    if ball['y'] > HEIGHT or ball['x'] > WIDTH or ball['y'] < 0 or ball['x'] < 0:
        reset_ball()

def render_text(text, pos, font=font, color=WHITE, bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

def draw_ball():
    pg.draw.circle(screen, MAGENTA, (ball['x'], ball['y']), 10, width=0)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Gravity')
speed = 40
throwing = False
clock = pg.time.Clock()
ball = {'x':0, 'y':HEIGHT, 'angle':45, 'speed':0, 'fall speed':0, 'gravity':1}
vys = []
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and not throwing:
                ball['speed'] = speed
                vys = []
                throwing = True
            elif event.key == K_UP and not ball['angle'] == 0:
                ball['angle'] -= 1
            elif event.key == K_DOWN and not ball['angle'] == 90:
                ball['angle'] += 1
            elif event.key == K_LEFT:
                speed -= 1
            elif event.key == K_RIGHT:
                speed += 1
            elif event.key == K_BACKSPACE:
                reset_ball()
            elif event.key == K_d:
                fig, ax = subplots()
                ax.plot(list(range(len(vys))), vys)
                ax.set_title('Ball velocity')
                ax.set_xlabel('Time (1/60 seconds)')
                ax.set_ylabel('Velocity (pixels per 1/60 seconds)')
                show()
    screen.fill(BACKGROUND)
    update_ball()
    draw_ball()
    if not throwing:
        render_text(f"Angle: {ball['angle']} (0 is totally up, 90 is totally right)", (0, 0))
        render_text(f"Launch speed: {speed}", (0, 50))
        render_text('Change angle with up/down keys', (0, 100))
        render_text('Change speed with left/right keys', (0, 150))
        render_text('Press space to start and press delete to stop', (0, 200))
        #render_text('Press D to show ball velocity', (0, 250))
    pg.display.update()
    clock.tick(60)