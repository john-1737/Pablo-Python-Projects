#v1.1
import pygame as pg
from pygame.locals import *
from sys import exit
from pygame.sprite import Sprite, Group
import random as ra
from tkinter import messagebox
import math as ma

pg.mixer.init()

if messagebox.askyesno(message='Are you playing on a laptop?'):
    H = 700
else:
    H = 1000

green_ships = pg.sprite.Group()
red_ships = pg.sprite.Group()
all_ships = pg.sprite.Group()

pg.font.init()
font = pg.font.SysFont(None, 36)

clock = pg.time.Clock()

green_ship_image = pg.image.load('greenship2.png')
red_ship_image = pg.image.load('redship2.png')
player_image = pg.image.load('blueship2.png')
background = pg.image.load('space.png')
collision_sound = pg.mixer.Sound('collision.wav')
pop_sound = pg.mixer.Sound('pop.wav')

def render_text(text, pos, font, color=(255, 255, 255)):
    _text = font.render(text, True, color)
    screen.blit(_text, pos)

def deg_to_rad(deg):
    distance = 2*ma.pi
    return (deg / 360) * distance

class Ship(Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        if self.color == 'green':
            green_ships.add(self)
            self.image = green_ship_image
        else:
            red_ships.add(self)
            self.image = red_ship_image
        self.angle = ra.randint(250, 290)
        self.rad = deg_to_rad(self.angle)
        all_ships.add(self)
        self.location = (ra.randint(0, 790), -50)
        self.rect = self.image.get_rect(topleft=self.location)
        
    def update(self):
        self.rect.y += abs(ma.sin(self.rad) * 3)
        self.rect.x += abs(ma.cos(self.rad) * 3)
        if self.rect.y >= H + 50:
            self.kill()


class Player_ship(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(f'blueship2.png')
        self.location = (450, H - 100)
        self.rect = self.image.get_rect(topleft=self.location)
        all_ships.add(self)

    def update(self):
        self.speed_x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.speed_x = -3
        if keys[pg.K_RIGHT]:
            self.speed_x = 3
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 900:
            self.rect.right = 900

pg.init()
lives = 5
score = 0
screen = pg.display.set_mode((900, H))
pg.display.set_caption('Alien Battle')
player = Player_ship()
print(all_ships)
while True:
    start_loop = True
    while start_loop:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    start_loop = False
        screen.blit(background, (0,0))
        render_text('Welcome to Alien Battle!', (50, 50), font)
        render_text('Use the left and right arrow keys to steer your ship (the blue one)', (50, 100), font)
        render_text('When you hit a green ship, you win a point.', (50, 150), font)
        render_text('When you hit a red ship, you lose a life.', (50, 200), font)
        render_text('When you lose all 5 lives, the game ends.', (50, 250), font)
        render_text('Press P during the game to pause.', (50, 300), font)
        render_text('Press ESC at any time to exit.', (50, 350), font)
        render_text('Press space to start!', (50, 400), font)
        pg.display.flip()
    score, lives = 0, 5
    paused = False
    while lives:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_p:
                    paused = not paused
        if not paused:                    
            if ra.randint(1, max(2, 100 - score * 3)) == 1:
                ship = Ship(ra.choice(['green', 'red']))
            screen.blit(background, (0,0))
            all_ships.update()
            all_ships.draw(screen)
            if pg.sprite.spritecollide(player, red_ships, True):
                collision_sound.play()
                lives -= 1
            if pg.sprite.spritecollide(player, green_ships, True):
                pop_sound.play()
                score += 1
            render_text(f'Score: {score}    Lives: {lives}', (10, 10), font)
        else:
            render_text('Paused', (10, 100), font)
            render_text('Click P to restart', (10, 150), font)    
        clock.tick(60)
        pg.display.flip()
    game_over_font = pg.font.SysFont(None, 70)
    restart = False
    for ship in red_ships:
        ship.kill()
    for ship in green_ships:
        ship.kill()        
    while not restart:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    restart = True
        screen.blit(background, (0,0))
        render_text('game over!', (100, H/2 - 100), game_over_font)
        render_text(f'Your score was {score}', (100, H/2), font)        
        render_text('Press space to play again', (100, H/2 + 50), font)
        pg.display.flip()
