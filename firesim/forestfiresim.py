import pygame as pg
import random as ra
from time import sleep
pg.init()

W, H, SIZE, SPEED, INIT_DENSITY, GROW_CHANCE, FIRE_CHANCE = 40, 25, 30, 0.5, 0.2, 0.01, 0.01
fire_img = pg.image.load('fire.png')
tree_img = pg.image.load('tree.png')
pg.font.init()
font = pg.font.SysFont(None, 48)

def render_text(text, pos, font, bold=True, color=(255, 255, 255)):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

def new_forest():
    forest = {}
    for i in range(W):
        for j in range(H):
            if ra.random() <= INIT_DENSITY:
                forest[i, j] = 't'
            else:
                forest[i, j] = 'e'
    return forest

def draw_forest(forest):
    for i in forest:
        if forest[i] == 't':
            screen.blit(tree_img, pg.Rect(i[0]*SIZE, i[1]*SIZE, SIZE, SIZE))
        if forest[i] == 'f':
            screen.blit(fire_img, pg.Rect(i[0]*SIZE, i[1]*SIZE, SIZE, SIZE))
        if forest[i] == 'b':
            pg.draw.rect(screen, (244, 164, 96), pg.Rect(i[0]*SIZE, i[1]*SIZE, SIZE, SIZE))

def update_forest(forest):
    new_forest = {}
    for i in range(W):           
        for j in range(H):
            if (i, j) in new_forest:
                continue
            if forest.get(i, j) == 'b':
                continue
            if forest[i, j] == 'e' and ra.random() <= GROW_CHANCE:
                new_forest[i, j] = 't'
            elif forest[i, j] == 't' and ra.random() <= FIRE_CHANCE:
                new_forest[i, j] = 'f'
            elif forest[i, j] == 'f':
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if forest.get((i+k, j+l)) == 't':
                            new_forest[i+k, j+l] = 'f'
                new_forest[i, j] = 'e'
            else:
                new_forest[i, j] = forest[i, j]
    return new_forest


screen = pg.display.set_mode((W*SIZE, H*SIZE))
screen.fill((112, 66, 20))

forest = {}
for i in range(W):
    for j in range(H):
        forest[i,j] = 'e'
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
                        forest[i, j] = 'e'
            elif event.key == pg.K_SPACE:
                first_run = False
            elif event.key == pg.K_r:
                forest = new_forest()
            elif event.key == pg.K_g:
                if GROW_CHANCE == 0.01:
                    GROW_CHANCE = 0.0
                else:
                    GROW_CHANCE = 0.01
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                pos_x, pos_y = x // SIZE, y // SIZE
                if forest[pos_x, pos_y] in ('t', 'b'):
                    forest[pos_x, pos_y] = 'e'
                else:
                    forest[pos_x, pos_y] = 't'
            elif event.button == 3:
                x, y = event.pos
                pos_x, pos_y = x // SIZE, y // SIZE
                if forest[pos_x, pos_y] in ('t', 'b'):
                    forest[pos_x, pos_y] = 'e'
                else:
                    forest[pos_x, pos_y] = 'b'
    pg.display.set_caption(f'Forest Fire\t\tRandom growth: {bool(GROW_CHANCE)}')
    screen.fill((112, 66, 20))
    draw_forest(forest)
    pg.display.update()

pg.display.set_caption('Forest Fire')
draw_forest(forest)
pg.display.update()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            raise SystemExit
    forest = update_forest(forest)
    screen.fill((112, 66, 20))
    draw_forest(forest)
    pg.display.update()
    sleep(0.5)