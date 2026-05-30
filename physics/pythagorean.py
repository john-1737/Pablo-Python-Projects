import pygame as pg
from pygame.locals import *

screen = pg.display.set_mode((600, 300))
pg.display.set_caption('The Proof Of The Pythagorean Theorem')

x, y = 0, 0
running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            y1 = event.pos[1]
            x1 = y1
            if y1 <= 300 and event.pos[0] <= 300:
                x, y = x1, y1
    screen.fill((0, 0, 0))
    pg.draw.polygon(screen, (255, 0, 0), [(0, y), (x, 300), (0, 300)])
    pg.draw.polygon(screen, (0, 255, 0), [(0, y), (300-x, 0), (0, 0)])
    pg.draw.polygon(screen, (0, 0, 255), [(300, 300-y), (300-x, 0), (300, 0)])
    pg.draw.polygon(screen, (255, 255, 0), [(300, 300-y), (x, 300), (300, 300)])
    pg.draw.polygon(screen, (255, 0, 0), [(300+x, 300-y), (300, 0), (300, 300-y)])
    pg.draw.polygon(screen, (0, 255, 0), [(300+300, 300-y), (x+300, 300), (x+300, 300-y)])
    pg.draw.polygon(screen, (0, 0, 255), [(300+x, 300-y), (300+x, 0), (300, 0)])
    pg.draw.polygon(screen, (255, 255, 0), [(300+300, 300-y), (x+300, 300), (300+300, 300)])
    pg.display.update()