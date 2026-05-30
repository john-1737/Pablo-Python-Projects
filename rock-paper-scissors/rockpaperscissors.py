import pygame as pg
from pygame.locals import *
from random import choice

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)
screen = pg.display.set_mode((600, 350))
pg.display.set_caption('Rock-Paper-Scissors')
images = (None, pg.image.load('rock.png').convert_alpha(), pg.image.load('paper.png').convert_alpha(), pg.image.load('scissors.png').convert_alpha())
names = (None, 'rock', 'paper', 'scissors')

def render_text(text, pos, font=font, bold=True, color=(255, 255, 255), right=False, center=False):
    text_surface = font.render(text, bold, color)
    width = text_surface.get_rect().width
    if right:
        screen.blit(text_surface, (pos[0]-width, pos[1]))
    elif center:
        screen.blit(text_surface, (pos[0]-(width/2), pos[1]))
    else:
        screen.blit(text_surface, pos)

def get_winner(move1, move2):
    if move1 == move2:
        return 0
    elif move1 == 1 and move2 == 3:
        return 1
    elif move1 == 2 and move2 == 1:
        return 1
    elif move1 == 3 and move2 == 2:
        return 1
    elif move1 == 1 and move2 == 2:
        return 2
    elif move1 == 2 and move2 == 3:
        return 2
    elif move1 == 3 and move2 == 1:
        return 2

start = True
while start:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == K_SPACE:
                start = False
                players = 2
            elif event.key == K_RETURN:
                start = False
                players = 1
    screen.fill((0,0,0))
    render_text('Welcome to Rock-Paper-Scissors!', (0,0))
    #render_text('Rock crushes scissors, scissors', (0, 50))
    #render_text('cut paper, and paper covers rock.', (0, 100))
    render_text('This game is for 1 or 2 players.', (0, 50))
    render_text('Rock crushes scissors, scissors cut paper, and paper covers rock.', (0, 100), smallfont)
    render_text('Player 1, use F for rock, D for paper, and S for scissors.', (0, 125), smallfont)
    render_text('Player 2, use J for rock, K for paper, and L for scissors.', (0, 150), smallfont)
    render_text('Alternatively, you can also play against the computer in one player mode.', (0, 175), smallfont)
    render_text('If you are playing in 2-player mode, do not look at the keyboard while the', (0, 200), smallfont)
    render_text('other player makes their move.', (0, 225), smallfont)
    render_text('Press SPACE for 2-player mode, or', (0, 250))
    render_text('press ENTER for 1-player mode.', (0, 300))
    pg.display.update()
wins = [0,0,0]
while True:
    move1 = None
    if players == 1:
        move2 = choice([1,2,3])
    else:
        move2 = None
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_f:
                    move1 = 1
                elif event.key == K_d:
                    move1 = 2
                elif event.key == K_s:
                    move1 = 3
                elif event.key == K_j and players == 2:
                    move2 = 1
                elif event.key == K_k and players == 2:
                    move2 = 2
                elif event.key == K_l and players == 2:
                    move2 = 3
        if move1 != None and move2 != None:
            break           
        screen.fill((0,0,0))
        render_text('Players, press your keys!', (0, 0))
        render_text('Player 1, use F for rock, D for paper, and S for scissors.', (0, 50), smallfont)
        if players == 2:
            render_text('Player 2, use J for rock, K for paper, and L for scissors.', (0, 75), smallfont)
            render_text('Do not look at the keyboard!', (0, 100))
        pg.display.update()
    results = True
    winner = get_winner(move1, move2)
    wins[winner] += 1
    while results:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    results = False
        screen.fill((0,0,0))
        render_text('Results:', (0, 0))
        render_text('Player 1:', (0, 50))
        render_text('Player 2:', (600, 50), right=True)
        screen.blit(images[move1], (0, 100))
        screen.blit(images[move2], (500, 100))
        render_text(names[move1], (0, 200))
        render_text(names[move2], (600, 200), right=True)
        if winner == 0:
            render_text("It's a tie!", (300, 200), center=True)
        else:
            render_text(f'Player {winner} wins!', (300, 200), center=True)
        render_text(f'Wins: {wins[1]}', (0, 250))
        render_text(f'Wins: {wins[2]}', (600, 250), right=True)
        render_text(f'Ties: {wins[0]}', (300, 250), center=True)
        render_text('Press SPACE to play again.', (0, 300))
        pg.display.update()