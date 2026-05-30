import pygame as pg
import math
from pygame.locals import *
GRAVITY = 2

def add_vectors(vector1, vector2):
    vx = vector1[0] + vector2[0]
    vy = vector1[1] + vector2[1]
    return (vx, vy)

class body:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.velocity = [0, 0]
        self.accel = [0, 0]
        self.prevposs = [tuple(self.pos), tuple(self.pos)]
        self.maximum = [0, 0]
    def draw(self):
        previous = self.prevposs[0]
        for i in self.prevposs[1:]:
            pg.draw.line(screen, self.color, previous, i, 2)
            previous = i
        pg.draw.circle(screen, self.color, tuple(self.pos), 10, width=0)
    def gravity(self, other):
        xd = self.pos[0] - other.pos[0]
        yd = self.pos[1] - other.pos[1]
        distance = math.sqrt(xd**2 + yd**2)
        gforce = GRAVITY * (1*1/distance**2)
        return (-(gforce * (xd/distance)), -(gforce * (yd/distance)))
    def move(self, other1, other2=None):
        vector1 = self.gravity(other1)
        if other2:
            vector2 = self.gravity(other2)
            self.accel = add_vectors(vector1, vector2)
        else:
            self.accel = vector1
        self.velocity[0] += self.accel[0]
        self.velocity[1] += self.accel[1]
        # if self.velocity[0] > 3:
        #     self.velocity[0] = 3
        # if self.velocity[0] < -3:
        #     self.velocity[0] = -3
        # if self.velocity[1] > 3:
        #     self.velocity[1] = 3
        # if self.velocity[1] < -3:
        #     self.velocity[1] = -3
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.prevposs.append(tuple(self.pos))

def add_vectors(vector1, vector2):
    rise = vector1[1] + vector2[1]
    run = vector1[0] + vector2[0]
    return (run, rise)

pg.init()
screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
bodies = [body([350, 300], (255, 0, 0)), body([350, 700], (0, 255, 0)), body([650, 700], (0, 0, 255))]
running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            print(bodies[0].maximum)
            print(bodies[1].maximum)
            print(bodies[2].maximum)
            exit()
        if event.type == KEYDOWN:
            running = False
    screen.fill((0, 0, 0))
    bodies[2].move(bodies[1], bodies[0])
    bodies[1].move(bodies[0], bodies[2])
    bodies[0].move(bodies[1], bodies[2])
    for i in bodies:
        i.draw()
    pg.display.update()
    clock.tick(100)
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()