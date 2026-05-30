"""Mancala, by Al Sweigart al@inventwithpython.com
The ancient seed-sowing game.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, board game, game, two-player"""

import sys
import pygame as pg
from pygame.locals import *
pg.init()
pg.font.init()

# A tuple of the player's pits:
PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')

# A dictionary whose keys are pits and values are opposite pit:
OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                   'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                   'K': 'E', 'L': 'F'}

# A dictionary whose keys are pits and values are the next pit in order:
NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
            'G': '2', '2': 'A'}

# Every pit label, in counterclockwise order starting with A:
PIT_LABELS = 'ABCDEF1LKJIHG2'

# How many seeds are in each pit at the start of a new game:
STARTING_NUMBER_OF_SEEDS = 4  # (!) Try changing this to 1 or 10.

WHITE, BLACK, BLUE, RED = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0)


def main():
    global screen, font, smallfont, gameBoard
    font = pg.font.SysFont(None, 48)
    smallfont = pg.font.SysFont(None, 24)
    screen = pg.display.set_mode((800, 450))
    pg.display.set_caption('Mancala')
    start = True
    while start:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_SPACE:
                    start = False
        screen.fill((0, 0, 0))
        render_text('Welcome to Mancala!', (0, 0), font=smallfont)
        render_text('The ancient two-player, seed-sowing game. Grab the seeds from a pit on your side and place one in', (0, 50), font=smallfont)
        render_text('each following pit, going counterclockwise and skipping your opponent\'s store. If your last seed lands', (0, 75), font=smallfont)
        render_text('in an empty pit of yours, move the opposite pit\'s seeds into your store. The goal is to get the most seeds', (0, 100), font=smallfont)
        render_text('in your store on the side of the board. If the last placed seed is in your store, you get a free turn.', (0, 125), font=smallfont)
        render_text('The game ends when all of one player\'s pits are empty. The other player claims the remaining seeds', (0, 175), font=smallfont)
        render_text('for their store, and the winner is the one with the most seeds.', (0, 200), font=smallfont)
        render_text('This game is inspired by Al Sweigart\'s Mancala.', (0, 250), font=smallfont)
        render_text('Press SPACE to start!', (0, 300), font=smallfont)
        pg.display.update()

    while True:
        gameBoard = getNewBoard()
        playerTurn = '1'  # Player 1 goes first.
        while True:  # Run a player's turn.
            
            playerMove = askForPlayerMove(playerTurn, gameBoard)

            # Carry out the player's move:
            playerTurn = makeMove(gameBoard, playerTurn, playerMove)

            # Check if the game ended and a player has won:
            winner = checkForWinner(gameBoard)
            if winner == 'Red' or winner == 'Blue':
                break
            elif winner == 'tie':
                break

        end = True
        while end:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        exit()
                    elif event.key == K_SPACE:
                        end = False
            screen.fill(BLACK)
            displayBoard(gameBoard)
            render_text(f'{winner} player has won!', (0, 300))
            render_text('Press SPACE to play again.', (0, 350))
            pg.display.update()

def getNewBoard():
    """Return a dictionary representing a Mancala board in the starting
    state: 4 seeds in each pit and 0 in the stores."""

    # Syntactic sugar - Use a shorter variable name:
    s = STARTING_NUMBER_OF_SEEDS

    # Create the data structure for the board, with 0 seeds in the
    # stores and the starting number of seeds in the pits:
    return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
            'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}

def render_text(text, pos, center=False, color=(255, 255, 255), font=pg.font.SysFont(None, 48)):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

def displayBoard(board):
    """Displays the game board as ASCII-art based on the board
    dictionary."""

    seedAmounts = []
    # This 'GHIJKL21ABCDEF' string is the order of the pits left to
    # right and top to bottom:
    for pit in 'GHIJKL21ABCDEF':
        numSeedsInThisPit = str(board[pit]).rjust(2)
        seedAmounts.append(numSeedsInThisPit)

    pg.draw.rect(screen, WHITE, pg.Rect(0, 50, 800, 200), 5)
    for i in range(1, 8):
        pg.draw.line(screen, WHITE, (i*100, 50), (i*100, 248), 5)
    pg.draw.line(screen, WHITE, (100, 150), (700, 150), 5)
    for i in range(6):
        render_text(str(seedAmounts[i]), (i*100+150, 100), center=True, color=BLUE)
        render_text(str(seedAmounts[i+8]), (i*100+150, 200), center=True, color=RED)
        render_text(str(seedAmounts[6]), (50, 150), center=True, color=BLUE)
        render_text(str(seedAmounts[7]), (750, 150), center=True, color=RED)
        render_text('Blue Store', (10, 60), font=smallfont, color=BLUE)
        render_text('Red Store', (710, 60), font=smallfont, color=RED)
        render_text('Blue Player', (400, 25), color=BLUE, center=True)
        pg.draw.polygon(screen, BLUE, ((300, 10), (300, 40), (270, 25)))
        pg.draw.polygon(screen, BLUE, ((530, 10), (530, 40), (500, 25)))
        render_text('Red Player', (400, 275), color=RED, center=True)
        pg.draw.polygon(screen, RED, ((270, 260), (270, 290), (300, 275)))
        pg.draw.polygon(screen, RED, ((500, 260), (500, 290), (530, 275)))

def askForPlayerMove(playerTurn, board):
    """Asks the player which pit on their side of the board they
    select to sow seeds from. Returns the uppercase letter label of the
    selected pit as a string."""
    error = ''
    while True:
        pit = None
        while pit == None:  # Keep asking the player until they enter a valid move.
            # Ask the player to select a pit on their side:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.type == K_ESCAPE:
                        pg.quit()
                        exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    pit_num = x // 100
                    if pit_num == 0 or pit_num == 7:
                        break
                    pit_num -= 1
                    if y >= 50 and y <= 150:
                        pit = PLAYER_2_PITS[pit_num]
                    elif y >= 150 and y <= 250:
                        pit = PLAYER_1_PITS[pit_num]
            screen.fill(BLACK)
            displayBoard(board)
            render_text(error, (0, 300))
            if playerTurn == '1':
                render_text('Red player, click on a square on your side to', (0, 350))
            elif playerTurn == '2':
                render_text('Blue player, click on a square on your side to', (0, 350))
            render_text('choose your move.', (0, 400))
            pg.display.update()

        # Make sure it is a valid pit to select:
        if (playerTurn == '1' and pit not in PLAYER_1_PITS) or (
            playerTurn == '2' and pit not in PLAYER_2_PITS
        ):
            error = 'Please pick a letter on your side of the board.'
            continue  # Ask player again for their move.
        if board.get(pit) == 0:
            error = 'Please pick a non-empty pit.'
            continue  # Ask player again for their move.
        return pit


def makeMove(board, playerTurn, pit):
    """Modify the board data structure so that the player 1 or 2 in
    turn selected pit as their pit to sow seeds from. Returns either
    '1' or '2' for whose turn it is next."""

    seedsToSow = board[pit]  # Get number of seeds from selected pit.
    board[pit] = 0  # Empty out the selected pit.

    while seedsToSow > 0:  # Continue sowing until we have no more seeds.
        pit = NEXT_PIT[pit]  # Move on to the next pit.
        if (playerTurn == '1' and pit == '2') or (
            playerTurn == '2' and pit == '1'
        ):
            continue  # Skip opponent's store.
        board[pit] += 1
        seedsToSow -= 1

    # If the last seed went into the player's store, they go again.
    if (pit == playerTurn == '1') or (pit == playerTurn == '2'):
        # The last seed landed in the player's store; take another turn.
        return playerTurn

    # Check if last seed was in an empty pit; take opposite pit's seeds.
    if playerTurn == '1' and pit in PLAYER_1_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['1'] += board[oppositePit]
        board[oppositePit] = 0
    elif playerTurn == '2' and pit in PLAYER_2_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['2'] += board[oppositePit]
        board[oppositePit] = 0

    # Return the other player as the next player:
    if playerTurn == '1':
        return '2'
    elif playerTurn == '2':
        return '1'


def checkForWinner(board):
    """Looks at board and returns either '1' or '2' if there is a
    winner or 'tie' or 'no winner' if there isn't. The game ends when a
    player's pits are all empty; the other player claims the remaining
    seeds for their store. The winner is whoever has the most seeds."""

    player1Total = board['A'] + board['B'] + board['C']
    player1Total += board['D'] + board['E'] + board['F']
    player2Total = board['G'] + board['H'] + board['I']
    player2Total += board['J'] + board['K'] + board['L']

    if player1Total == 0:
        # Player 2 gets all the remaining seeds on their side:
        board['2'] += player2Total
        for pit in PLAYER_2_PITS:
            board[pit] = 0  # Set all pits to 0.
    elif player2Total == 0:
        # Player 1 gets all the remaining seeds on their side:
        board['1'] += player1Total
        for pit in PLAYER_1_PITS:
            board[pit] = 0  # Set all pits to 0.
    else:
        return None  # No one has won yet.

    # Game is over, find player with largest score.
    if board['1'] > board['2']:
        return 'Red'
    elif board['2'] > board['1']:
        return 'Blue'
    else:
        return 'tie'


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
