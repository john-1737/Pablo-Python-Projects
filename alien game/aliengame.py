#v1.0
import pygame as pg
from pygame.locals import *
from sys import exit
from pygame.sprite import Sprite, Group
import random as ra

H = 700

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

def render_text(text, pos, font):
    _text = font.render(text, True, (255, 255, 255))
    screen.blit(_text, pos)

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
        all_ships.add(self)
        self.location = (ra.randint(0, 790), -50)
        self.rect = self.image.get_rect(topleft=self.location)
        
    def update(self):
        self.rect.y += 3
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
player = Player_ship()
print(all_ships)
while lives:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    if ra.randint(1, 100) == 1:
        ship = Ship(ra.choice(['green', 'red']))
    screen.blit(background, (0,0))
    all_ships.update()
    all_ships.draw(screen)
    if pg.sprite.spritecollide(player, red_ships, True):
        lives -= 1
    if pg.sprite.spritecollide(player, green_ships, True):
        score += 1
    render_text(f'Score: {score}    Lives: {lives}', (10, 10), font)    
    clock.tick(60)
    pg.display.flip()
game_over_font = pg.font.SysFont(None, 70)
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    screen.blit(background, (0,0))
    render_text(f'game over!', (100, H/2 - 100), game_over_font)
    pg.display.flip()
