# Reversegam: a clone of Othello/Reversi
import random, sys
import pygame as pg
from pygame.locals import *
WIDTH = 8  # Board is 8 spaces wide
HEIGHT = 8 # Board is 8 spaces tall
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def drawBoard(board):
    # This function prints the board that it was passed. Returns None.
    for y in range(1, HEIGHT+1):
        pg.draw.line(screen, WHITE, (0, y*50), (50*WIDTH, y*50), 1)
    for x in range(1, WIDTH):
        pg.draw.line(screen, WHITE, (x*50, 0), (x*50, 50*HEIGHT), 1)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if board[x][y] == 'X':
                pg.draw.circle(screen, RED, ((50*x)+25, (50*y)+25), 25, width=0)
            elif board[x][y] == 'O':
                pg.draw.circle(screen, BLUE, ((50*x)+25, (50*y)+25), 25, width=0)
            elif board[x][y] == 'x':
                pg.draw.circle(screen, RED, ((50*x)+25, (50*y)+25), 25, width=1)
            elif board[x][y] == 'o':
                pg.draw.circle(screen, BLUE, ((50*x)+25, (50*y)+25), 25, width=1)

def getNewBoard():
    # Creates a brand-new, blank board data structure.
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # First step in the x direction
        y += ydirection # First step in the y direction
        while isOnBoard(x, y) and board[x][y] == otherTile:
            # Keep moving in this x & y direction.
            x += xdirection
            y += ydirection
            if isOnBoard(x, y) and board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def getBoardWithValidMoves(board, tile):
    # Returns a new board with periods marking the valid moves the player can make.
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        if tile == 'X':
            boardCopy[x][y] = 'x'
        else:
            boardCopy[x][y] = 'o'
    return boardCopy

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def whoGoesFirst():
    # Randomly choose who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move; True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return it.
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

def getPlayerMove(board, playerTile, xc, yc):
    # Let the player enter their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()

    if yc <= 400:
        x = xc//50
        y = yc//50
        if isValidMove(board, playerTile, x, y) == False:
            return None
        else:
            return [x, y]
    else:
        return None

def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # randomize the order of the moves

    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Find the highest-scoring move possible.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    render_text(f'Red score: {scores[playerTile]} points.', (0, 400))
    render_text(f'Blue score: {scores[computerTile]} points.', (0, 450))

def playGame(playerTile, computerTile, players):
    showHints = False
    turn = playerTile
    # Clear the board and place starting pieces.
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        move = None
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                move = getPlayerMove(board, turn, x, y)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_h:
                    showHints = not showHints
        xValidMoves = getValidMoves(board, playerTile)
        oValidMoves = getValidMoves(board, computerTile)
        screen.fill(BLACK)
        if showHints:
            validMovesBoard = getBoardWithValidMoves(board, turn)
            drawBoard(validMovesBoard)
        else:
            drawBoard(board)
        printScore(board, playerTile, computerTile)
        if turn == 'X':
            render_text('It is red\'s turn.', (0, 500))
        else:
            render_text('It is blue\'s turn.', (0, 500))
        if showHints:
            render_text('Press H to turn off hints.', (0, 550))
        else:
            render_text('Press H to turn on hints.', (0, 550))
        if xValidMoves == [] and oValidMoves == []:
            return board # No one can move, so end the game.
        elif turn == 'X' and move: # Player's turn
            if xValidMoves != []:
                makeMove(board, playerTile, move[0], move[1])
            turn = 'O'

        elif turn == 'O': # Computer's turn
            if players == 2 and move:
                if oValidMoves != []:
                    makeMove(board, computerTile, move[0], move[1])
                    turn = 'X'
            elif players == 1 and oValidMoves != []:
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
                turn = 'X'
        pg.display.update()

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)

def render_text(text, pos, font=font, color=WHITE, bold=True):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)
    
playerTile, computerTile = 'X', 'O'
players = 0
screen = pg.display.set_mode((400, 600))
pg.display.set_caption('Reversegam')
while not players:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == K_1:
                players = 1
            elif event.key == K_2:
                players = 2
    screen.fill(BLACK)
    render_text('Welcome to Reversegam!', (0, 0))
    render_text('Two players take turns placing tiles of their chosen', (0, 50), font=smallfont)
    render_text('color—red or blue—on the board.', (0, 75), font=smallfont)
    render_text('When a player places a tile on the board, any of the', (0, 100), font=smallfont)
    render_text('opponent\'s tiles that are between the new tile and', (0, 125), font=smallfont)
    render_text('the other tiles of the player\'s color are flipped.', (0, 150), font=smallfont)
    render_text('The goal of the game is to end with more tiles of', (0, 175), font=smallfont)
    render_text('your color than your opponent\'s color.', (0, 200), font=smallfont)
    render_text('Tiles in all directions are flipped as long as they', (0, 225), font=smallfont)
    render_text('are between the player\'s new tile and an existing', (0, 250), font=smallfont)
    render_text('tile of that color.', (0, 275), font=smallfont)
    render_text('Players must always make a move that flips at least', (0, 300), font=smallfont)
    render_text('one tile. The game ends when either a player can\'t', (0, 325), font=smallfont)
    render_text('make a move or the board is completely full. The', (0, 350), font=smallfont)
    render_text('player with the most tiles of their color wins.', (0, 375), font=smallfont)
    render_text('Based on Al Sweigart\'s Reversegam.', (0, 400), font=smallfont)
    render_text('Press 1 key for 1-player mode.', (0, 425), font=smallfont)
    render_text('Press 2 key for 2-player mode.', (0, 450), font=smallfont)
    pg.display.update()


while True:
    finalBoard = playGame(playerTile, computerTile, players)
    end = True
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    end = False

        # Display the final score.
        screen.fill(BLACK)
        drawBoard(finalBoard)
        printScore(finalBoard, playerTile, computerTile)
        scores = getScoreOfBoard(finalBoard)
        if scores[playerTile] > scores[computerTile]:
            render_text('red wins!', (0, 500))
        elif scores[playerTile] < scores[computerTile]:
            render_text('blue wins!', (0, 500))
        else:
            render_text('The game is a tie!', (0, 500))
        render_text('Press SPACE to restart.', (0, 550))
        pg.display.update()