"""Three-Card Monte, by Al Sweigart al@inventwithpython.com
Find the Queen of Hearts after cards have been swapped around.
(In the real-life version, the scammer palms the Queen of Hearts so you
always lose.)
More info at https://en.wikipedia.org/wiki/Three-card_Monte
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, card game, game"""

import random, time
import pygame as pg
from pygame.locals import *
pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)
swapfont = pg.font.SysFont(None, 35)

def draw_card(card, pos):
    if card == 'backside':
        screen.blit(backside, pos)
        return
    pg.draw.rect(screen, (255, 255, 255), pg.Rect(pos[0], pos[1], 100, 150))
    if card[0] in ('J', 'Q', 'K'):
        for i in ((25,75), (75,75)):
            screen.blit({HEARTS: heart, DIAMONDS: diamond, SPADES: spade, CLUBS: club}[card[1]], (i[0]+pos[0]-13, i[1]+pos[1]-13))
        screen.blit({'J': jack, 'Q': queen, 'K': king}[card[0]], (50+pos[0]-13, 75+pos[1]-13))
    else:
        for i in card_poss[card[0]]:
            screen.blit({HEARTS: heart, DIAMONDS: diamond, SPADES: spade, CLUBS: club}[card[1]], (i[0]+pos[0]-13, i[1]+pos[1]-13))
    render_text(card[0], (pos[0], pos[1]), color=(0,0,0), font=card_font)
    render_text(card[0], (pos[0]+100, pos[1]+150), color=(0,0,0), font=card_font, seanchor=True)

def render_text(text, pos, font=font, seanchor=False, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if seanchor:
        width = rect.width
        height = rect.height
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

def getRandomCard():
    """Returns a random card that is NOT the Queen of Hearts."""
    while True:  # Make cards until you get a non-Queen of hearts.
        rank = random.choice(list('23456789JQKA') + ['10'])
        suit = random.choice([HEARTS, DIAMONDS, SPADES, CLUBS])

        # Return the card as long as it's not the Queen of Hearts:
        if rank != 'Q' and suit != HEARTS:
            return (rank, suit)

# Set up the constants:
NUM_SWAPS = 16   # (!) Try changing this to 30 or 100.
DELAY     = 0.8  # (!) Try changing this 2.0 or 0.0.

# The card suit characters:
HEARTS   = chr(9829)  # Character 9829 is '♥'
DIAMONDS = chr(9830)  # Character 9830 is '♦'
SPADES   = chr(9824)  # Character 9824 is '♠'
CLUBS    = chr(9827)  # Character 9827 is '♣'
card_poss = {'A': ((50, 75),), '2': ((50, 37.5), (50, 112.5),), '3': ((50, 25),(50, 75),(50, 125)), '4': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5)), '5': ((50, 75),(25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5)),
'6': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75)), '7': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75), (50, 75)), '8': ((25, 37.5), (50, 37.5), (25, 112.5), (50, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75)),
 '9': ((25, 18.75), (25, 93.75), (25, 131.25), (75, 93.75),(75, 18.75), (75, 131.25), (25, 56.25), (75, 56.25), (50, 75)), '10': ((25, 18.75), (25, 93.75), (25, 131.25), (75, 93.75),(75, 18.75), (75, 131.25), (25, 56.25), (75, 56.25), (50, 37.5), (50, 112.5))}

# A list of chr() codes is at https://inventwithpython.com/chr

# The indexes of a 3-card list:
LEFT   = 0
MIDDLE = 1
RIGHT  = 2

screen = pg.display.set_mode((340, 350))
pg.display.set_caption('Three-Card Monte')
heart = pg.transform.scale(pg.image.load('heart.png').convert_alpha(), (26, 26))
club = pg.transform.scale(pg.image.load('club.png').convert_alpha(), (26, 26))
diamond = pg.transform.scale(pg.image.load('diamond.png').convert_alpha(), (26, 26))
spade = pg.transform.scale(pg.image.load('spade.png').convert_alpha(), (26, 26))
jack = pg.transform.scale(pg.image.load('jack.png').convert_alpha(), (26, 26))
queen = pg.transform.scale(pg.image.load('queen.png').convert_alpha(), (26, 26))
king = pg.transform.scale(pg.image.load('king.png').convert_alpha(), (26, 26))
backside = pg.image.load('backside.png').convert_alpha()
card_font = pg.font.SysFont('Arial', 15)

running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == K_SPACE:
                running = False
    screen.fill((0, 0, 0))
    render_text('Welcome to Three-Card Monte!', (0, 0), smallfont)
    render_text('Find the red lady (the Queen of Hearts)!', (0, 25), smallfont)
    render_text('Keep an eye on how the cards move.', (0, 50), smallfont)
    render_text('Press SPACE to start!', (0, 150), smallfont)
    render_text('This game is inspired by Al Sweigart\'s', (0, 75), smallfont)
    render_text('Three-Card Monte. Similar games can be', (0, 100), smallfont)
    render_text('found at some sporting events.', (0, 125), smallfont)
    pg.display.update()

winmode = False
losemode = False
while True:
    cards = [('Q', HEARTS), getRandomCard(), getRandomCard()]
    random.shuffle(cards)  # Put the Queen of Hearts in a random place.
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    running = False
                elif event.key == K_w:
                    winmode = not winmode
                    losemode = False
                elif event.key == K_l:
                    losemode = not losemode
                    winmode = False
        screen.fill((0, 0, 0))
        render_text('Here are the cards:', (0, 0))
        for i, card in enumerate(cards):
            draw_card(card, (i*120, 50))
        render_text('Press SPACE when you are ready to begin.', (0, 200), smallfont)
        pg.display.update()

    for i in range(NUM_SWAPS):
        swap = random.choice(['l-m', 'm-r', 'l-r'])
        if swap == 'l-m':
            cards[LEFT], cards[MIDDLE] = cards[MIDDLE], cards[LEFT]
        elif swap == 'm-r':
            cards[MIDDLE], cards[RIGHT] = cards[RIGHT], cards[MIDDLE]
        elif swap == 'l-r':
            cards[LEFT], cards[RIGHT] = cards[RIGHT], cards[LEFT]
        clock = pg.time.Clock()
        for i in range(int(DELAY*100)):
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        exit()
            screen.fill((0, 0, 0))
            if swap == 'l-m':
                render_text('swapping left and middle...', (0, 0), swapfont)
                draw_card('backside', (2*120, 50))
                draw_card('backside', ((i*120/DELAY*100)/10000, 50))
                draw_card('backside', (120-(i*120/DELAY*100)/10000, 50))
            elif swap == 'm-r':
                render_text('swapping middle and right...', (0, 0), swapfont)
                draw_card('backside', (0, 50))
                draw_card('backside', (120+(i*120/DELAY*100)/10000, 50))
                draw_card('backside', (240-(i*120/DELAY*100)/10000, 50))
            elif swap == 'l-r':
                render_text('swapping left and right...', (0, 0), swapfont)
                draw_card('backside', (120, 50))
                draw_card('backside', ((i*240/DELAY*100)/10000, 50))
                draw_card('backside', (240-(i*240/DELAY*100)/10000, 50))
            
            pg.display.update()
            clock.tick(100)
        
    guess = None
    while guess == None:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 50 and y <= 200:
                    if x <= 100:
                        guess = 0
                    elif x >= 120 and x <= 220:
                        guess = 1
                    elif x >= 240:
                        guess = 2
        screen.fill((0, 0, 0))
        render_text('Which card has the Queen of Hearts?', (0, 0), pg.font.SysFont(None, 27))
        for i in range(3):
            draw_card('backside', (i*120, 50))
        pg.display.update()
    
    if losemode and cards[guess] == ('Q', HEARTS):
        # Player has won, so let's move the queen.
        possibleNewIndexes = [0, 1, 2]
        possibleNewIndexes.remove(guess)  # Remove the queen's index.
        newInd = random.choice(possibleNewIndexes)  # Choose a new index.
        # Place the queen at the new index:
        cards[guess], cards[newInd] = cards[newInd], cards[guess]

    elif winmode and cards[guess] != ('Q', HEARTS):
        newInd = cards.index(('Q', HEARTS))
        # Place the queen at the new index:
        cards[guess], cards[newInd] = cards[newInd], cards[guess]

    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    running = False
        screen.fill((0, 0, 0))
        for i, card in enumerate(cards):
            draw_card(card, (i*120, 50))
        if cards[guess] == ('Q', HEARTS):
            render_text('You won!', (0, 200), swapfont)
            render_text('Thanks for playing!', (0, 250), swapfont)
        else:
            render_text('You lost!', (0, 200), swapfont)
            render_text('Thanks for playing, sucker!', (0, 250), swapfont)
        render_text('Press SPACE to play again.', (0, 300), swapfont)
        pg.display.update()

# # (!) Uncomment this code to make the player always lose:
# #if cards[guessIndex] == ('Q', HEARTS):
# #    # Player has won, so let's move the queen.
# #    possibleNewIndexes = [0, 1, 2]
# #    possibleNewIndexes.remove(guessIndex)  # Remove the queen's index.
# #    newInd = random.choice(possibleNewIndexes)  # Choose a new index.
# #    # Place the queen at the new index:
# #    cards[guessIndex], cards[newInd] = cards[newInd], cards[guessIndex]
