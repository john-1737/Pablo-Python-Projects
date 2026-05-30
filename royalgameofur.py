"""The Royal Game of Ur, by Al Sweigart al@inventwithpython.com
A 5,000 year old board game from Mesopotamia. Two players knock each
other back as they race for the goal.
More info https://en.wikipedia.org/wiki/Royal_Game_of_Ur
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, board game, game, two-player
"""

import random, sys
import pygame as pg
from pygame.locals import *
pg.init()

X_PLAYER = 'X'
O_PLAYER = 'O'
EMPTY = ' '
WHITE, RED, BLUE, BLACK, YELLOW = (255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 0, 0), (255, 255, 0)

pg.font.init()
small_font = pg.font.SysFont(None, 25)
font = pg.font.SysFont(None, 50)

# Set up constants for the space labels:
X_HOME = 'x_home'
O_HOME = 'o_home'
X_GOAL = 'x_goal'
O_GOAL = 'o_goal'

# The spaces in left to right, top to bottom order:
ALL_SPACES = 'hgfetsijklmnopdcbarq'
SPACE_POSITIONS = 'hgfe  tsijklmnopdcba  rq'
X_TRACK = 'HefghijklmnopstG'  # (H stands for Home, G stands for Goal.)
O_TRACK = 'HabcdijklmnopqrG'

FLOWER_SPACES = ('h', 't', 'l', 'd', 'r')


def render_text(text, pos, font=font, color=WHITE, bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

def main():
    global flower
    gameBoard = getNewBoard()
    global screen
    screen = pg.display.set_mode((1000, 750))
    hints_mode = False
    path_mode = False
    pg.display.set_caption('Royal Game Of Ur')
    flower = pg.image.load('flower.png').convert_alpha()
    start_screen = True
    while start_screen:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    start_screen = False
                elif event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
        screen.fill(BLACK)
        displayBoard(gameBoard, sides=False)
        show_path()
        render_text('Welcome to Royal Game of Ur!', pos=(0, 0), font=small_font)
        render_text('Inspired by Al Sweigart\'s Royal Game Of Ur at https://nostarch.com/big-book-small-python-programming', pos=(0,25), font=small_font)

        render_text('This is a 5,000 year old game. Two players must move their tokens', pos=(0, 425), font=small_font)
        render_text('from their home to their goal. On your turn you roll four dice and can', pos=(0,450), font=small_font)
        render_text('move one token a number of spaces equal to the points you got.', pos=(0, 475), font=small_font)

        render_text('Ur is a racing game; the first player to move all seven of their tokens to their goal wins.', pos=(0, 500), font=small_font)
        render_text('To do this, tokens must travel from their home to their goal using the above path.', pos=(0, 525), font=small_font)

        render_text('If you land on an opponent\'s token in the middle track, it gets sent', pos=(0, 550), font=small_font)
        render_text('back home. The flower spaces let you take another turn. Tokens in', pos=(0, 575), font=small_font)
        render_text('the middle flower space are safe and cannot be landed on.', pos=(0, 600), font=small_font)
        render_text('Press Space to start!', pos=(0, 625), font=small_font)
        pg.display.update()
    turn = O_PLAYER
    status = 'normal'
    flips = []
    flipTally = 0
    for i in range(4):
        result = random.randint(0, 1)
        flips.append(result)
        flipTally += result
    lost_turn = False
    while True:  # Main game loop.
        # Set up some variables for this turn:
        if turn == X_PLAYER:
            opponent = O_PLAYER
            home = X_HOME
            track = X_TRACK
            goal = X_GOAL
            opponentHome = O_HOME
        elif turn == O_PLAYER:
            opponent = X_PLAYER
            home = O_HOME
            track = O_TRACK
            goal = O_GOAL
            opponentHome = X_HOME
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_h:
                    hints_mode = not hints_mode
                elif event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and not status == 'win':
                if lost_turn == True:
                    turn = opponent
                    flips = []
                    flipTally = 0
                    for i in range(4):
                        result = random.randint(0, 1)
                        flips.append(result)
                        flipTally += result
                    status='normal'
                    lost_turn = False
                    break
                x, y = event.pos
                x //= 100
                y //= 100
                if x in (8, 9):
                    break
                # Perform the selected move on the board:
                if y in (0, 4) and x in (0, 1, 2, 3) and 'home' in validMoves:
                    # Subtract tokens at home if moving from home:
                    gameBoard[home] -= 1
                    nextTrackSpaceIndex = flipTally
                    nextBoardSpace = track[nextTrackSpaceIndex]
                    # Check if the opponent has a tile there:
                    if gameBoard[nextBoardSpace] == opponent:
                        gameBoard[opponentHome] += 1
                    gameBoard[nextBoardSpace] = turn
                    flips = []
                    flipTally = 0
                    for i in range(4):
                        result = random.randint(0, 1)
                        flips.append(result)
                        flipTally += result
                    status='normal'
                    if nextBoardSpace in FLOWER_SPACES:
                        status = 'flower land'
                    else:
                        turn = opponent
                    break
                else:
                    pos = ((y*8)+x)-8
                    if pos < 0 or pos > 23:
                        break
                    move = SPACE_POSITIONS[pos]
                    if move not in validMoves:
                        break
                    gameBoard[move] = EMPTY  # Set the "from" space to empty.
                    nextTrackSpaceIndex = track.index(move) + flipTally

                movingOntoGoal = nextTrackSpaceIndex == len(track) - 1
                if movingOntoGoal:
                    gameBoard[goal] += 1
                    # Check if the player has won:
                    if gameBoard[goal] == 1:
                        displayBoard(gameBoard)
                        status = 'win'
                        break
                    nextBoardSpace = 'z'
                else:
                    nextBoardSpace = track[nextTrackSpaceIndex]
                    # Check if the opponent has a tile there:
                    if gameBoard[nextBoardSpace] == opponent:
                        gameBoard[opponentHome] += 1
                    gameBoard[nextBoardSpace] = turn

                # Check if the player landed on a flower space and can go again:
            
                if nextBoardSpace in FLOWER_SPACES:
                    status = 'flower land'
                else:
                    turn = opponent
                    status='normal'

                flips = []
                flipTally = 0
                for i in range(4):
                    result = random.randint(0, 1)
                    flips.append(result)
                    flipTally += result

        screen.fill(BLACK)
        displayBoard(gameBoard)
        color = {'X': 'red', 'O': 'blue'}
        if status == 'win':
            render_text(f'{color[turn]} wins!', (0, 500))
            pg.display.update()
            continue
        if status == 'flower land':
            render_text(f'{color[turn]} landed on a flower space. Rolls:', (0, 500), font)
        else:
            render_text('It is ' + color[turn] + '\'s turn. Rolls:', (0, 500), font)
        for i in range(4): 
            pg.draw.polygon(screen, WHITE, ((((i*100)+50), 550), (((i*100)+25), 600), (((i*100)+75), 600)))
            if flips[i] == 1:
                pg.draw.circle(screen, BLACK, (((i*100)+50), 582.5), 12.5, width=0)
        if flipTally == 0:
            render_text('You didn\'t roll any points, so you lose a turn.', (0, 600), font)
            lost_turn = True
            pg.display.update()
            continue

        # Ask the player for their move:
        validMoves = getValidMoves(gameBoard, turn, flipTally)
        if hints_mode:
            show_hints(turn, validMoves)
        if path_mode:
            show_path()

        if validMoves == []:
            render_text('There are no possible moves, so you lose a turn.', (0, 600), font)
            lost_turn = True
            pg.display.update()
            continue
    
        render_text('Click token or home to move '+ str(flipTally)+ ' spaces.', (0,600), font)
        render_text('Press H to show/hide all possible moves.', (0, 650), font)
        pg.display.update()
        # Swap turns to the other player.

def getNewBoard():
    """
    Returns a dictionary that represents the state of the board. The
    keys are strings of the space labels, the values are X_PLAYER,
    O_PLAYER, or EMPTY. There are also counters for how many tokens are
    at the home and goal of both players.
    """
    board = {X_HOME: 7, X_GOAL: 0, O_HOME: 7, O_GOAL: 0}
    # Set each space as empty to start:
    for spaceLabel in ALL_SPACES:
        board[spaceLabel] = EMPTY
    return board

def show_path():
    for i in (100, 200, 300, 400, 500, 600, 700):
        pg.draw.polygon(screen, RED, ((i-15, 210), (i-15, 240), (i+15, 225)))
        pg.draw.polygon(screen, BLUE, ((i-15, 260), (i-15, 290), (i+15, 275)))
        if i not in (400, 500, 600):
            pg.draw.polygon(screen, RED, ((i+15, 135), (i+15, 165), (i-15, 150)))
            pg.draw.polygon(screen, BLUE, ((i+15, 335), (i+15, 365), (i-15, 350)))
    pg.draw.polygon(screen, RED, ((35, 185), (65, 185), (50, 215)))
    pg.draw.polygon(screen, RED, ((735, 215), (765, 215), (750, 185)))
    pg.draw.polygon(screen, BLUE, ((35, 315), (65, 315), (50, 285)))
    pg.draw.polygon(screen, BLUE, ((735, 285), (765, 285), (750, 315)))

def displayBoard(board, sides=True):
    """Display the board on the screen."""
    for i in ((0, 100), (600, 100), (0, 300), (600, 300), (300, 200)):
        screen.blit(flower, i)
    for i in range(0, 9):
        if i == 5:
            pg.draw.line(screen, WHITE, (500, 200), (500, 300), 5)
        else:
            pg.draw.line(screen, WHITE, ((i*100), 100), ((i*100), 400), 5)
    for i in range(1, 5):
        if i in (2, 3):
            pg.draw.line(screen, WHITE, (0, (i*100)), (800, (i*100)), 5)
        else:
            pg.draw.line(screen, WHITE, (0, (i*100)), (400, (i*100)), 5)
            pg.draw.line(screen, WHITE, (600, (i*100)), (800, (i*100)), 5)
    if not sides:
        return
    for i in range(7):
        pg.draw.circle(screen, WHITE, ((50+(i*50)), 50), 25, width=5)
        pg.draw.circle(screen, WHITE, ((50+(i*50)), 450), 25, width=5)
        pg.draw.circle(screen, WHITE, ((650+(i*50)), 50), 25, width=5)
        pg.draw.circle(screen, WHITE, ((650+(i*50)), 450), 25, width=5)
    for i in range(7):
        if i < board[X_HOME]:
            pg.draw.circle(screen, RED, ((50+(i*50)), 50), 25, width=0)
        if i < board[O_HOME]:
            pg.draw.circle(screen, BLUE, ((50+(i*50)), 450), 25, width=0)
        if i < board[X_GOAL]:
            pg.draw.circle(screen, RED, ((650+(i*50)), 50), 25, width=0)        
        if i < board[O_GOAL]:
            pg.draw.circle(screen, BLUE, ((650+(i*50)), 450), 25, width=0)
    for i, s in enumerate(SPACE_POSITIONS):
        y, x = divmod(i, 8)
        y *= 100
        y += 150
        x *= 100
        x += 50
        if s == ' ':
            continue
        if board[s] == ' ':
            continue
        if board[s] == X_PLAYER:
            fill = RED
        elif board[s] == O_PLAYER:
            fill = BLUE
        pg.draw.circle(screen, fill, (x, y), 25, width=0)
    render_text('red home', (0, 0), small_font, RED, False)
    render_text('blue home', (0, 475), small_font, BLUE, False)
    render_text('red goal', (600, 0), small_font, RED, False)
    render_text('blue goal', (600, 475), small_font, BLUE, False)


def show_hints(player, moves):
    if 'home' in moves:
        if player == X_PLAYER:
            pos = 0
        else:
            pos = 400
        pg.draw.rect(screen, YELLOW, pg.Rect(0, pos, 400, 100), 5)
    for i, s in enumerate(SPACE_POSITIONS):
        y, x = divmod(i, 8)
        y *= 100
        y += 100
        x *= 100
        if s == ' ':
            continue
        if s in moves:
            pg.draw.rect(screen, YELLOW, pg.Rect(x, y, 100, 100), 5)


def getValidMoves(board, player, flipTally):
    validMoves = []  # Contains the spaces with tokens that can move.
    if player == X_PLAYER:
        opponent = O_PLAYER
        track = X_TRACK
        home = X_HOME
    elif player == O_PLAYER:
        opponent = X_PLAYER
        track = O_TRACK
        home = O_HOME

    # Check if the player can move a token from home:
    if board[home] > 0 and board[track[flipTally]] == EMPTY:
        validMoves.append('home')

    # Check which spaces have a token the player can move:
    for trackSpaceIndex, space in enumerate(track):
        if space == 'H' or space == 'G' or board[space] != player:
            continue
        nextTrackSpaceIndex = trackSpaceIndex + flipTally
        if nextTrackSpaceIndex >= len(track):
            # You must flip an exact number of moves onto the goal,
            # otherwise you can't move on the goal.
            continue
        else:
            nextBoardSpaceKey = track[nextTrackSpaceIndex]
            if nextBoardSpaceKey == 'G':
                # This token can move off the board:
                validMoves.append(space)
                continue
        if board[nextBoardSpaceKey] in (EMPTY, opponent):
            # If the next space is the protected middle space, you
            # can only move there if it is empty:
            if nextBoardSpaceKey == 'l' and board['l'] == opponent:
                continue  # Skip this move, the space is protected.
            validMoves.append(space)

    return validMoves


if __name__ == '__main__':
    main()