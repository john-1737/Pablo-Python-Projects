import pygame as pg
from pygame.locals import *
from math import sin, cos, tan, radians
pg.init()
WIDTH = 800
HEIGHT = 800
screen = pg.display.set_mode((WIDTH+50, HEIGHT))
pg.display.set_caption('Ski Slope')
skier = pg.image.load('skier.png').convert_alpha()
skier = pg.transform.scale(skier, (100, 100))
angle = 36.86989765
skier = pg.transform.rotate(skier, -angle)
xpos = -50
ypos = (HEIGHT-50)-((tan(radians(angle)))*WIDTH)
speed = 0

def move_skier(xpos, ypos, speed):
    if ypos >= HEIGHT:
        return (-50, (HEIGHT-50)-((tan(radians(angle)))*WIDTH), 0)
    speed += 1
    return(xpos+(4*speed), ypos+(3*speed), speed)

clock = pg.time.Clock()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    screen.fill((0,0,0))
    pg.draw.polygon(screen, (255, 255, 255), ((0, HEIGHT), (WIDTH, HEIGHT), (0, HEIGHT-((tan(radians(angle)))*WIDTH))))
    xpos, ypos, speed = move_skier(xpos, ypos, speed)
    screen.blit(skier, (xpos, ypos))
    pg.display.update()
    clock.tick(10)