import pygame as pg
from copy import deepcopy
from sys import exit
from time import sleep


SIZE = 15
W, H, ALIVE, DEAD = 80, 50, (255, 255, 0), (0, 0, 255)

clock = pg.time.Clock()

def draw_cells(cells):
    for i in range(W):
        for j in range(H):
            pg.draw.rect(screen, cells[i, j], pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE))
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE), 1)

pg.font.init()
font = pg.font.SysFont(None, 48)

# Function to render text
def render_text(text, pos):
    text_surface = font.render(text, True, (255, 255, 255))
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

while True:
    first_run = True
    while first_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == pg.K_BACKSPACE:
                    for i in range(W):
                        for j in range(H):
                            drawn_cells[i, j] = DEAD
                elif event.key == pg.K_SPACE:
                    first_run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    pos_x, pos_y = x // SIZE, y // SIZE
                    if drawn_cells[pos_x, pos_y] == ALIVE:
                        drawn_cells[pos_x, pos_y] = DEAD
                    else:
                        drawn_cells[pos_x, pos_y] = ALIVE
        draw_cells(drawn_cells)
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
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    second_run = False
                elif event.key == pg.K_PLUS:
                    fps += 1
                    if fps == 61:
                        fps = 1
                elif event.key == pg.K_MINUS:
                    fps -= 1
                    if fps == 0:
                        fps = 60
        next_cells = generate_next_cells(cells)
        screen.fill((0, 0, 0))
        render_text(f'FPS: {fps}', (0, (H * SIZE) + 50))
        draw_cells(next_cells)
        pg.display.update()
        clock.tick(fps)
