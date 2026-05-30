import pygame as pg
from pygame.locals import *

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
        k = 1/1000
        self.acceleration = -k * (self.length - self.original_length)
        v0 = self.velocity
        self.velocity += self.acceleration
        if friction:
            self.velocity += -(self.velocity*0.01)
        self.length += self.velocity
        if (self.velocity >= 0 and v0 < 0):
            self.velocity += 1
        elif (self.velocity < 0 and v0 >= 0):
            self.velocity -= 1
        # self.phase_count += 1
        # if round(self.length, None) == self.release_length and not mousedown:
        #     self.phase = self.phase_count
        #     print(self.phase)
        #     self.phase_count = 0

pg.init()
screen = pg.display.set_mode((750, 500))
pg.display.set_caption('Spring')
book = pg.transform.scale(pg.image.load('feynman-book.png').convert_alpha(), (100, 100))
teacher = pg.transform.scale(pg.image.load('richard2.png').convert_alpha(), (100, 100))
spring = Spring(100, 0, 200, book)
spring_positions = [spring.length for i in range(501)]
spring_velocities = [0 for i in range(501)]
clock = pg.time.Clock()
friction = False
while True:
    mousedown = False
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            y = event.pos[1]
            spring.length = y
            spring.release_length = y
            mousedown = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == K_SPACE:
                spring.length = spring.original_length
                spring.acceleration = 0
                spring.velocity = 0
            elif event.key == K_UP:
                spring.velocity -= 2
            elif event.key == K_DOWN:
                spring.velocity += 2
            elif event.key == K_f:
                friction = not friction
    screen.fill((0, 0, 0))
    screen.blit(teacher, (0, 400))
    pg.draw.line(screen, (0, 0, 255), (0, 200), (750, 200), 2)
    if not mousedown:
        spring.move()
    spring.draw()
    spring_positions.append(spring.length+spring.y)
    spring_velocities.append(spring.velocity)
    del spring_positions[0:-500]
    del spring_velocities[0:-500]
    pg.draw.lines(screen, (255, 0, 0), False, [(i+200, j) for i, j in enumerate(spring_positions)], 2)
    pg.draw.lines(screen, (0, 255, 255), False, [(i+200, 200+j*3) for i, j in enumerate(spring_velocities)], 2)
    pg.display.update()
    clock.tick(60)