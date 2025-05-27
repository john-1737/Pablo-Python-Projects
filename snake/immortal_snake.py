#Snake
import pygame as pg
import random as ra
import time as t
def render_text(text, pos, font, bold=True, color=(255, 255, 255)):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

W, H, SIZE = 19, 19, 30 #Make sure W and H are ALWAYS odd
game_over = False
pg.font.init()
font = pg.font.SysFont(None, 48)

class snake:
    def __init__(self):
        self.body = [{'pos':(8, 10), 'dir':'e'}, {'pos':(9, 10), 'dir':'e'}, {'pos':(10, 10), 'dir':'e'}]
        #head = pg.sprite.Sprite()
    def draw(self):
        for i in self.body[:-1]:
            pg.draw.rect(screen, (0, 0, 255), pg.Rect((i['pos'][0] % W) * SIZE, (i['pos'][1] % H) * SIZE, SIZE, SIZE))
    def move(self):
        del self.body[0]
        dir = self.body[-1]['dir']
        x, y = self.body[-1]['pos']
        if dir == 'n':
            self.body.append({'pos':(x, y-1), 'dir':dir})
        elif dir == 's':
            self.body.append({'pos':(x, y+1), 'dir':dir})
        elif dir == 'w':
            self.body.append({'pos':(x-1, y), 'dir':dir})
        elif dir == 'e':
            self.body.append({'pos':(x+1, y), 'dir':dir})
    def grow(self):
        dir = self.body[0]['dir']
        x, y = self.body[0]['pos']
        self.body.reverse()
        if dir == 's':
            self.body.append({'pos':(x, y-1), 'dir':dir})
        elif dir == 'n':
            self.body.append({'pos':(x, y+1), 'dir':dir})
        elif dir == 'e':
            self.body.append({'pos':(x-1, y), 'dir':dir})
        elif dir == 'w':
            self.body.append({'pos':(x+1, y), 'dir':dir})
        self.body.reverse()
    def rotate(self, key):
        if self.body[-1]['dir'] == 'n':
            if key == pg.K_LEFT:
                self.body[-1]['dir'] = 'w'
            elif key == pg.K_RIGHT:
                self.body[-1]['dir'] = 'e'
        elif self.body[-1]['dir'] == 's':
            if key == pg.K_RIGHT:
                self.body[-1]['dir'] = 'e'
            elif key == pg.K_LEFT:
                self.body[-1]['dir'] = 'w'
        elif self.body[-1]['dir'] == 'e':
            if key == pg.K_UP:
                self.body[-1]['dir'] = 'n'
            elif key == pg.K_DOWN:
                self.body[-1]['dir'] = 's'
        elif self.body[-1]['dir'] == 'w':
            if key == pg.K_DOWN:
                self.body[-1]['dir'] = 's'
            elif key == pg.K_UP:
                self.body[-1]['dir'] = 'n'
        

class snakehead(pg.sprite.Sprite):
    def __init__(self, s):
        self.s = s
        self.body = self.s.body
        super().__init__()
        self.image = pg.image.load('snakehead2.gif')
        self.direction = self.body[-1]['dir']
        self.image = pg.transform.rotate(self.image, {'n':0, 's':180, 'e':270, 'w':90}[self.body[-1]['dir']])
        self.location = (self.s.body[-1]['pos'][0] * SIZE, self.s.body[-1]['pos'][1] * SIZE)
        self.rect = self.image.get_rect(topleft=self.location)       
    def update(self):
        self.image = pg.image.load('snakehead2.gif')
        self.image = pg.transform.rotate(self.image, {'n':0, 's':180, 'e':270, 'w':90}[self.body[-1]['dir']])        
        self.rect.topleft = ((self.s.body[-1]['pos'][0] % W) * SIZE, (self.s.body[-1]['pos'][1] % H) * SIZE)
    def check_collision(self):
        if pg.sprite.spritecollide(sh, apples, False):
            a.__init__()
            self.s.grow()
            global score
            score += 1

class apple(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('apple.gif')
        self.location = (ra.randint(0, W-1) * SIZE, ra.randint(0, H-1) * SIZE)
        print(self.location)
        self.rect = self.image.get_rect(topleft=self.location)

class game:
    def __init__(self):
        fill = True
        for i in range(W):
            for j in range(H):
                if fill:
                    pg.draw.rect(screen, (0, 255, 0), pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE))
                else:
                    pg.draw.rect(screen, (0, 190, 0), pg.Rect(i * SIZE, j * SIZE, SIZE, SIZE))
                fill = not fill
                pg.draw.rect(screen, (255, 0, 255), pg.Rect(0, H*SIZE, W*SIZE, 96))
    
pg.init()    
screen = pg.display.set_mode((W*SIZE, H*SIZE + 96))
game()
s = snake()
s.draw()
sh = snakehead(s)
a = apple()

# Create a sprite group and add the snake head sprite to it
all_sprites = pg.sprite.Group()
snakeheads = pg.sprite.Group()
apples = pg.sprite.Group()
all_sprites.add(sh)
all_sprites.add(a)
snakeheads.add(sh)
apples.add(a)

pg.display.set_caption('Snake')
pg.display.update()
game_over = False
score = 0
while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key in[pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]:
               s.rotate(event.key)
            if event.key == pg.K_x:
                game_over = True

    game()    
    s.move()
    s.draw()
    sh.update()
    sh.check_collision()
    render_text(f'Score: {score}', (10, H*SIZE), font, bold=True, color=(0,0,0))
    render_text('Press X to end the game', (10, H*SIZE + 48), font, bold=True, color=(0,0,0))    

    # Draw sprites
    all_sprites.draw(screen)

    pg.display.update()  
    t.sleep(0.25)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit
    game()
    render_text('game over!', (10*SIZE, 3*SIZE), font)
    pg.display.update()