import pygame as pg
from pygame.locals import *
from math import sqrt

class sphere:
    def __init__(self, image, pos, size):
        self.image = pg.transform.scale(pg.image.load(image).convert_alpha(), (size, size))
        self.size = size
        self.pos = pos
    
    def draw(self):
        screen.blit(self.image, (self.pos[0]-self.size/2, self.pos[1]-self.size/2))

class rocket:
    def __init__(self, pos):
        self.image = pg.transform.scale(pg.image.load('rocket.png').convert_alpha(), (50, 50))
        self.size = 50
        self.pos = pos
        self.accel = (0.02, -0.1)
        self.vel = [0, 0]
    
    def draw(self):
        screen.blit(self.image, (self.pos[0]-self.size/2, self.pos[1]-self.size/2))

    def gravity(self):
        xte = -(self.pos[0] - W/2)
        yte = self.pos[1] - H/2
        rte = sqrt(xte**2 + yte**2)
        gforce = (100000000000000)/(rte**2)
        self.forcev = (gforce*(xte/rte), gforce*(yte/rte))

    def move(self):
        self.gravity()
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        self.vel[0] -= self.forcev[0]
        self.vel[1] += self.forcev[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

H, W = 1000, 1000
pg.init()
screen = pg.display.set_mode((H, W))
pg.display.set_caption('Rocket')

earth = sphere('earth.png', (W/2, H/2) ,250)
moon = sphere('moon.png', (W, 0), 125)
rocket1 = rocket([484-25, 463-25])

clock = pg.time.Clock()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    
    screen.fill((0,0,0))
    earth.draw()
    moon.draw()
    rocket1.move()
    rocket1.draw()
    pg.display.update()
    clock.tick(60)