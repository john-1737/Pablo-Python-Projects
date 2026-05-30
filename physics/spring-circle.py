import pygame as pg
from pygame.locals import *
from math import sin, cos, radians

class Spring:
    def __init__(self, x, y, length, object):
        self.x = x
        self.y = y
        self.length = length
        self.original_length = length
        self.release_length = 0
        self.object = object
        self.acceleration = 0
        self.velocity = 0

    def draw(self):
        segment_length = self.length/10
        for i in range(10):
            pg.draw.line(screen, (160, 160, 160), (self.x-15, segment_length*i), (self.x+15, segment_length*(i+0.5)), 2)
            pg.draw.line(screen, (160, 160, 160), (self.x+15, segment_length*(i+0.5)), (self.x-15, segment_length*(i+1)), 2)
        image_width = self.object.get_rect().width
        screen.blit(self.object, (self.x-(image_width/2), self.y+self.length))

    def move(self):
        global ball_pos
        k = 1/1000
        self.acceleration = -k * (self.length - self.original_length)
        self.velocity += self.acceleration
        self.length += self.velocity
        ball_pos += 1/200*360
        ball_pos %= 360

pg.init()
screen = pg.display.set_mode((950, 500))
pg.display.set_caption('Spring')
book = pg.transform.scale(pg.image.load('feynman-book.png').convert_alpha(), (100, 100))
teacher = pg.transform.scale(pg.image.load('richard2.png').convert_alpha(), (100, 100))
spring = Spring(100, 0, 200, book)
spring_positions = [spring.length for i in range(501)]
spring_velocities = [0 for i in range(501)]
clock = pg.time.Clock()
spring.release_length = 300
spring.length = 300
ball_pos = 0
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
    screen.fill((0, 0, 0))
    screen.blit(teacher, (0, 400))
    pg.draw.line(screen, (0, 0, 255), (0, 200), (750, 200), 2)
    spring.move()
    spring.draw()
    spring_positions.append(spring.length+spring.y)
    spring_velocities.append(spring.velocity)
    del spring_positions[0:-500]
    del spring_velocities[0:-500]
    pg.draw.lines(screen, (255, 0, 0), False, [(i+200, j) for i, j in enumerate(spring_positions)], 2)
    pg.draw.lines(screen, (0, 255, 255), False, [(i+200, 200+j*3) for i, j in enumerate(spring_velocities)], 2)
    pg.draw.circle(screen, (0, 255, 0), (850, 200), 100, width=2)
    pg.draw.circle(screen, (255, 0, 255), (cos(radians((ball_pos)+90%360))*100+850, sin(radians((ball_pos)+90%360))*100+200), 10)
    pg.draw.line(screen, 'white', (700, spring_positions[-1]), (950, spring_positions[-1]), 2)
    pg.display.update()
    clock.tick(60)