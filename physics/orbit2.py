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

class satellite:
    def __init__(self, pos, motion, vmotion):
        self.image = pg.transform.scale(pg.image.load('satellite.png').convert_alpha(), (50, 50))
        self.size = 50
        self.pos = pos
        self.accel = (0, 0)
        self.vel = [0, 0]
        self.forcev = (0, 0)
        self.accel = (0, 0)
        self.vel = [motion, vmotion]
    
    def draw(self):
        screen.blit(self.image, (self.pos[0]-self.size/2, self.pos[1]-self.size/2))

    def gravity(self):
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

    def move(self, gravity):
        if gravity:
            self.gravity()
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        self.vel[0] -= self.forcev[0]
        self.vel[1] -= self.forcev[1]
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
moon = sphere('moon.png', (W, 0), 125)
s = satellite([500, 350], 0, 0)
initvel = 4.0
vinitvel = 4.0
while True:
    orbiting = True
    gravity = False
    clock = pg.time.Clock()
    while orbiting:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    gravity = not gravity
                    s = satellite([500, 350], int(gravity)*initvel, -(int(gravity)*vinitvel))
                elif event.key == K_LEFT:
                    if not (gravity and initvel <= 0) :
                        initvel -= 0.1
                elif event.key == K_RIGHT:
                    if not gravity:
                        initvel += 0.1
                elif event.key == K_DOWN:
                    if not (gravity and vinitvel <= 0) :
                        vinitvel -= 0.1
                elif event.key == K_UP:
                    if not gravity:
                        vinitvel += 0.1
        initvel = round(initvel, 1)
        vinitvel = round(vinitvel, 1)
        screen.fill((0,0,0))
        earth.draw()
        moon.draw()
        if not gravity:
            render_text(f'Horizontal velocity of satellite: {initvel} (change with left/right keys)', (500, 475), center=True)
            render_text(f'Vertical velocity of satellite: {vinitvel} (change with up/down keys)', (500, 525), center=True)
            render_text('Press SPACE to start/stop', (500, 575), center=True)
        s.move(gravity)
        s.draw()
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
        moon.draw()
        s.draw()
        render_text('Your satellite has crashed!', (500, 200), center=True)
        render_text('Press SPACE to play again.', (500, 250), center=True)
        pg.display.update()
    s = satellite([500, 350], 0, 0)