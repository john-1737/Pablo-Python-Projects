import pygame as pg
from pygame.locals import *
from math import sin, cos, radians, ceil

class vehicle:
    def __init__(self, image, mass, name):
        self.imagename = image
        self.image = pg.image.load(image).convert_alpha()
        self.mass = mass
        self.name = name

    def rotate(self, angle):
        self.image = pg.image.load(self.imagename).convert_alpha()
        self.image = pg.transform.rotate(self.image, angle)

def draw_track():
    pg.draw.line(screen, (255, 255, 255), (300, 50), (1300, 50), 10)
    pg.draw.line(screen, (255, 255, 255), (300, 550), (1300, 550), 10)
    pg.draw.arc(screen, (255, 255, 255), pg.Rect((50, 45), (500, 510)), radians(90), radians(270), 10)
    pg.draw.arc(screen, (255, 255, 255), pg.Rect((1050, 45), (500, 510)), radians(270), radians(90), 10)

def draw_vehicle(pos, v, angle):
    v.rotate(angle)
    imgrect = v.image.get_rect()
    width = imgrect.width/2
    height = imgrect.height/2
    screen.blit(v.image, (pos[0]-width, pos[1]-height))

def render_text(text, pos, font, bold=True, color=(255, 255, 255)):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)
arcstep = 785*2
screen = pg.display.set_mode((1600, 600))
pg.display.set_caption('Racetrack')
truck = vehicle('truck.png', 6, 'truck')
bus = vehicle('bus.png', 4, 'bus')
car = vehicle('car.png', 2, 'car')
motorcycle = vehicle('motorcycle.png', 1, 'motorcycle')
vehicles = [truck, bus, car, motorcycle]
selected_vehicle = 2
second_vehicle = 2

show_second = False
positions = [(i, 50) for i in range(800, 299, -1)] + [(cos(radians(((i/arcstep)*360)+90))*250+300, sin(radians(((i/arcstep)*360)+90))*250+300) for i in range(int(arcstep/2), 0, -1)] +\
[(i, 550) for i in range(300, 1301)] + [(cos(radians(((i/arcstep)*360)+270))*250+1300, sin(radians(((i/arcstep)*360)+270))*250+300) for i in range(int(arcstep/2), 0, -1)]+\
[(i, 50) for i in range(1300, 799, -1)]
angles = [0 for i in range(800, 299, -1)] + [((i/arcstep)*360) for i in range(1, int(arcstep/2)+1)] +\
[180 for i in range(300, 1301)] + [((i/arcstep)*360)+180 for i in range(1, int(arcstep/2)+1)]+\
[0 for i in range(1300, 799, -1)]
position = 0
second_pos = ceil(len(positions)/2)
clock = pg.time.Clock()
joystick = pg.joystick.Joystick(0)
acceleration = 0
speed = 0
angle = 0
force = 0
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == JOYBUTTONDOWN:
            if event.button == 0:
                pg.quit()
                exit()
            elif event.button == 2:
                selected_vehicle += 1
                selected_vehicle %= 4
            elif event.button == 1:
                show_second = not show_second
                second_pos = ceil(len(positions)/2)
            elif event.button == 3:
                second_vehicle += 1
                second_vehicle %= 4
        elif event.type == pg.JOYAXISMOTION:
            if event.axis == 4:
                if abs(event.value) == event.value:
                    force = event.value * 2
                else:
                    force = 0
            elif event.axis == 5:
                if abs(event.value) == event.value:
                    force = -event.value
                else:
                    force = 0
    screen.fill((0,0,0))
    mass = vehicles[selected_vehicle].mass
    draw_track()
    draw_vehicle(positions[int(position)%len(positions)], vehicles[selected_vehicle], angles[int(position)%len(positions)])
    if show_second:
        draw_vehicle(positions[int(second_pos)%len(positions)], vehicles[second_vehicle], angles[int(second_pos)%len(positions)])
        if position >= second_pos-50:
            mass += vehicles[second_vehicle].mass
            second_pos = position+50
    render_text('Vehicle selected:', (300, 75), font)
    draw_vehicle((325, 125), vehicles[selected_vehicle], 0)
    render_text(vehicles[selected_vehicle].name + ' (Change with square button)', (350, 125), font)
    render_text(f'Mass: {vehicles[selected_vehicle].mass} tons    Acceleration from motor/brake: {acceleration:.2f} pixels/frame^2',(300, 175), font)
    render_text(f'Force from motor/brake: {vehicles[selected_vehicle].mass*acceleration:.2f} tons times pixels/frame^2',(300, 225), font)
    render_text(f'Friction (force in the opposite direction): {0.05*vehicles[selected_vehicle].mass:.2f} tons times pixels/frame^2',(300, 275), font)
    if show_second:
        render_text('Second vehicle:', (300, 325), font)
        draw_vehicle((325, 375), vehicles[second_vehicle], 0)
        render_text(vehicles[second_vehicle].name + ' (Change with triangle button)', (350, 375), font)
    acceleration = force/mass
    speed += acceleration
    speed -= 0.05 * vehicles[selected_vehicle].mass
    if speed < 0:
        speed = 0 #Prevent the vehicle from reversing.
    position += speed
    
    pg.display.update()
    clock.tick(60)