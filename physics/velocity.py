import pygame as pg
from math import sin, cos, radians
from pygame.locals import *
from sys import exit
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)
mile_font = pg.font.SysFont(None, 25)

def render_text(text, pos, font=font, color=WHITE, bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

def move_pointer(mileage):
    mileage *= 45
    mileage %= 360
    mileage = radians(mileage)
    xpos = (cos(mileage) + 1) * 300
    ypos = (sin(mileage) + 1) * 300
    pg.draw.circle(screen, CYAN, (310, 310), 305, width=10)
    for i in range(1, 9):
        miletext = i
        miletext *= 45
        miletext %= 360
        miletext = radians(miletext)
        xpos2 = (cos(miletext) * 280) + 310
        ypos2 = (sin(miletext) * 280)+ 310
        render_text(str(i), (xpos2, ypos2), mile_font, YELLOW, False)
    pg.draw.circle(screen, MAGENTA, (xpos+10, ypos+10), 10, width=0)

screen = pg.display.set_mode((620, 620))
pg.display.set_caption('Velocity Example')
mileage = 0
speed = 1
clock = pg.time.Clock()
accelerating = 0
potaccel = 1
acceliter = 0
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                speed -= 0.1
            elif event.key == K_RIGHT:
                speed += 0.1
            elif event.key == K_UP and not accelerating:
                accelerating = potaccel
                acceliter = 1
            elif event.key == K_DOWN and not accelerating:
                accelerating = -potaccel
                acceliter = 1
            elif event.key == K_a:
                potaccel -= 0.1
            elif event.key == K_d:
                potaccel += 0.1
    screen.fill((0,0,0))
    move_pointer(mileage)
    render_text(f'Speed = {speed:.1f} mi/s', (100, 125), font)
    render_text(f'Acceleration = {accelerating:.1f} mi/s²', (100, 175), font)
    render_text(f'Potential mi/s²: = {potaccel:.1f} mi/s²', (100, 225), font)
    render_text('Use left/right keys to change speed', (100, 275), mile_font)
    render_text('Use up/down keys to accelerate/decelerate', (100, 305), mile_font)
    render_text('Use A/D keys to change potential acceleration', (100, 325), mile_font)
    if accelerating:
        acceliter += 1
        if round(accelerating, 2) > 0:
            speed += 1/60
        elif round(accelerating, 1) == 0:
            pass
        elif round(accelerating, 2) < 0:
            speed -= 1/60
        if acceliter == 60:
            speed = round(speed, 1)
            accelerating = 0
            acceliter = 0
    mileage += speed/60
    pg.display.update()
    clock.tick(60)