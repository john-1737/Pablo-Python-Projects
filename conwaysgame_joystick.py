import pygame as pg
from copy import deepcopy
from sys import exit
from time import sleep
from tkinter import messagebox
if not messagebox.askokcancel(message='This game requires a joystick controller connected by USB to the computer. It is designed to work with a Sony PS4 joytick. If you do not have a joystick, press Cancel. You can also play the version\
 that uses a computer keyboard.'):
    exit()

FRAME_RATE = 60
SIZE = 15
W, H, ALIVE, DEAD = 80, 50, (255, 255, 0), (0, 0, 255)

clock = pg.time.Clock()

def draw_cells(cells, cursor):
    for i in range(W):
        for j in range(H):
            pg.draw.rect(screen, cells[i, j], pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE))
            if [i, j] == cursor:
                pg.draw.rect(screen, (255, 0, 0), pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE), 1)    
            else:
                pg.draw.rect(screen, (0, 0, 0), pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE), 1)

def handle_joyevent(event):
    if event.type == pg.JOYBUTTONDOWN:
        if event.button == 8:
            pos_x, pos_y = cursor
            if drawn_cells[pos_x, pos_y] == ALIVE:
                drawn_cells[pos_x, pos_y] = DEAD
            else:
                drawn_cells[pos_x, pos_y] = ALIVE
    if event.type == pg.JOYAXISMOTION:
        if abs(round(event.value, 2)) == 1:        
            if event.axis == 2:
                if event.value <= 0:
                    if cursor[0] != 0:
                        cursor[0] -= 1
                else:
                    if cursor[0] != W:
                        cursor[0] += 1                 
            elif event.axis == 3:
                if event.value <= 0:
                    if cursor[1] != 0:
                        cursor[1] -= 1               
                else:
                    if cursor[1] != H:
                        cursor[1] += 1

pg.font.init()
font = pg.font.SysFont(None, 48)

# Function to render text
def render_text(text, pos):
    text_surface = font.render(text, False, (255, 255, 255))
    screen.blit(text_surface, pos)            

def generate_next_cells(cells):
    return_cells = deepcopy(cells)
    for x in range(W):
        for y in range(H):
            l = (x-1) % W
            r = (x+1) % W
            a = (y+1) % H
            b = (y-1) % H

            neighbors = 0
            neighbor_cells = [(l, a), (r, a), (l, b), (r, b), (l, y), (r, y), (x, a), (x, b)]
            for i in neighbor_cells:
                if cells[i] == ALIVE:
                    neighbors += 1
            if cells[x, y] == ALIVE and (neighbors == 2 or neighbors == 3):
                return_cells[x, y] = ALIVE
            elif cells[x, y] == DEAD and neighbors == 3:
                return_cells[x, y] = ALIVE
            else:
                return_cells[x, y] = DEAD
    return return_cells            

pg.init()
screen = pg.display.set_mode((W * SIZE, (H * SIZE) + 100))
pg.display.set_caption("Conway's Game Of Life")
drawn_cells = {}
for i in range(W):
    for j in range(H):
        drawn_cells[i, j] = DEAD

#Initialize/connect joystick
joystick = pg.joystick.Joystick(0)
joysticks = {}

#Set the original start cursor
cursor = [30, 30]

while True:
    first_run = True
    while first_run:
        for event in pg.event.get():
            #print('Event handling')
            handle_joyevent(event)
            #print(joy_pos)
            
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:
                    pg.quit()
                    exit()
                elif event.button == 1:
                    for i in range(W):
                        for j in range(H):
                            drawn_cells[i, j] = DEAD
                if event.button == 10:
                    first_run = False
        
            
            if event.type == pg.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joystick = pg.joystick.Joystick(event.device_index)
                joysticks[joystick.get_instance_id()] = joystick
                #print(f"Joystick {joystick.get_instance_id()} connencted")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                #print(f"Joystick {event.instance_id} disconnected")
        
        render_text('Use right joystick to move cursor (in red). Press right joystick to select.', (0, (H * SIZE)))
        render_text('Press R1 to start simulation.', (0, (H * SIZE) + 50))
        clock.tick(FRAME_RATE)
        draw_cells(drawn_cells, cursor)
        pg.display.update()

    next_cells = generate_next_cells(drawn_cells)
    second_run = True
    fps = 2
    while second_run:
        cells = deepcopy(next_cells)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:
                    pg.quit()
                    exit()                
                elif event.button == 10:
                    second_run = False
                elif event.button == 14:
                    fps += 1
                    if fps == 61:
                        fps = 1
                elif event.button == 13:
                    fps -= 1
                    if fps == 0:
                        fps = 60
        next_cells = generate_next_cells(cells)
        screen.fill((0, 0, 0))
        render_text(f'FPS: {fps}', (0, (H * SIZE)))
        render_text('Use left/right arrow buttons to change FPS', (0, (H * SIZE) + 50))
        draw_cells(next_cells, [-1, -1])
        pg.display.update()
        clock.tick(fps)
