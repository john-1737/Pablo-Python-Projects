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

class moon(sphere):
    def __init__(self, image, pos, size, vel):
        sphere.__init__(self, image, pos, size)
        self.pos = pos
        self.vel = vel
        self.forcev = (0, 0)
        self.accel = (0, 0)

    def gravity_to_earth(self):
        global orbiting
        xte = self.pos[0] - W/2
        yte = self.pos[1] - H/2
        rte = sqrt(xte**2 + yte**2)
        gforce = (1e4)/(rte**2)
        self.forcev = (gforce*(xte/rte), gforce*(yte/rte))
        if rte < 125:
            self.forcev = (0, 0)
            self.accel = (0, 0)
            self.vel = [0, 0]
            self.image = pg.transform.scale(pg.image.load('explosion.png').convert_alpha(), (50, 50))
            orbiting = False

    def gravity_to(self, object):
        global orbiting
        xte = self.pos[0] - object.pos[0]
        yte = self.pos[1] - object.pos[1]
        rte = sqrt(xte**2 + yte**2)
        gforce = (1e2)/(rte**2)
        self.forcev2 = (gforce*(xte/rte), gforce*(yte/rte))
        if rte < 125:
            self.forcev2 = (0, 0)
            self.accel = (0, 0)
            self.vel = [0, 0]
            self.image = pg.transform.scale(pg.image.load('explosion.png').convert_alpha(), (50, 50))
            orbiting = False        

    def move(self, gravity, object):
        if gravity:
            self.gravity_to_earth()
            self.gravity_to(object)
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        self.vel[0] -= self.forcev[0]
        self.vel[1] -= self.forcev[1]
        self.vel[0] += self.forcev2[0]
        self.vel[1] += self.forcev2[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

H, W = 1000, 1000
pg.init()
screen = pg.display.set_mode((H, W))
pg.display.set_caption('Rocket')
pg.font.init()
font = pg.font.SysFont(None, 48)
WHITE = (255, 255, 255)

def render_text(text, pos, center=False, color=(255, 255, 255), font=font):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

earth = sphere('earth.png', (W/2, H/2) ,250)
moon1 = moon('moon.png', [W/2, 100], 125, [5.0, 0])
moon2 = moon('moon2.png', [100, H/2], 125, [0, -5.0])
while True:
    orbiting = True
    gravity = False
    clock = pg.time.Clock()
    initvel = 4
    while orbiting:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
        screen.fill((0, 0, 0))
        earth.draw()
        moon1.move(True, moon2)
        moon1.draw()
        moon2.move(True, moon1)
        moon2.draw()
        pg.display.update()
        clock.tick(60)

    gameover = True
    while gameover:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    gameover = False
        screen.fill((0,0,0))
        earth.draw()
        moon1.draw()
        moon2.draw()
        render_text('Your satellite has crashed!', (500, 200), center=True)
        render_text('Press SPACE to play again.', (500, 250), center=True)
        pg.display.update()
    moon1 = moon('moon.png', [W/2, 100], 125, [5.0, 0])
    moon2 = moon('moon2.png', [100, H/2], 125, [0, -5.0])