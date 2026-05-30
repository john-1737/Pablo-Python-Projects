import pygame as pg
from pygame.locals import *
dot = {'x': 0, 'y': 500, 'acceleration': 0, 'speed': 0, 'takeoff speed': 27, 'yspeed': 0}
speeds = []
accelerations = []
times = []
xs = []
acceleration = 0.6
'''def plot(base, yvars, colors, img):
    index= 0
    for i, j in zip(yvars, colors):
        for k, l in zip(i[:-1], base[:-1]):
            pg.draw.line(screen, j, ((k*50)))
        index += 1'''

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)

WHITE = (255,255,255)

def render_text(text, pos, font=font, color=WHITE, bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

screen = pg.display.set_mode((1500, 500))
pg.display.set_caption('Boeing 747 Runway')
img = pg.image.load('plane.png').convert_alpha()
clock = pg.time.Clock()
time = 0
flying = False
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not flying:
                dot['acceleration'] = acceleration
                flying = True
            else:
                dot = {'x': 0, 'y': 500, 'acceleration': 0, 'speed': 0, 'takeoff speed': 27, 'yspeed': 0}
                speeds = []
                accelerations = []
                times = []
                xs = []
                time = 0
                flying = False
    dot['speed'] += dot['acceleration']
    dot['x'] += (dot['speed'])
    if dot['speed'] >= dot['takeoff speed']:
        dot['yspeed'] += acceleration
        dot['y'] -= dot['yspeed']
    if dot['x'] >= 1500 or dot['y'] <= 0:
        dot = {'x': 0, 'y': 500, 'acceleration': 0, 'speed': 0, 'takeoff speed': 27, 'yspeed': 0}
        speeds = []
        accelerations = []
        times = []
        xs = []
        time = 0
        flying = False
    else:
        speeds.append(dot['speed'])
        accelerations.append(dot['acceleration'])
        times.append(time)
        xs.append(dot['x'])
        time += 1
    screen.fill((0,0,0))
    if not flying:
        render_text('Click screen to launch Boeing 747.', (0, 0))
    else:
        render_text('Click screen to reset Boeing 747.', (0, 0))
    screen.blit(img, (dot['x'], dot['y']-25))
    pg.display.update()
    clock.tick(10)