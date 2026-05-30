# Sonar Treasure Hunt

import random
import sys
import math
import pygame as pg
from pygame.locals import *

pg.init()
pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 25)

def render_text(text, pos, center=False, color=(255, 255, 255), font=font):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

def getNewBoard():
    # Create a new 60x15 board data structure.
    board = []
    for x in range(30): # The main list is a list of 60 lists.
        board.append([])
        for y in range(15): # Each list in the main list has 15 single-character strings.
            # Use different characters for the ocean to make it more readable.
            board[x].append('')
    return board

def drawBoard(board):
    # Draw the board data structure.
    pg.draw.rect(screen, (0, 0, 255), pg.Rect(25, 25, 750, 375))
    for i in range(30):
        render_text(str(i+1), (i*25+37.5, 12.5), True, font=smallfont)
        render_text(str(i+1), (i*25+37.5, 412.5), True, font=smallfont)
        pg.draw.line(screen, (255, 255, 255), (i*25+25, 0), (i*25+25, 425), 1)
    pg.draw.line(screen, (255, 255, 255), (30*25+25, 0), (30*25+25, 425), 1)
    
    for i in range(15):
        render_text(str(i+1), (12.5, i*25+37.5), True, font=smallfont)
        render_text(str(i+1), (787.5, i*25+37.5), True, font=smallfont)
        pg.draw.line(screen, (255, 255, 255), (0, i*25+25), (800, i*25+25), 1)
    pg.draw.line(screen, (255, 255, 255), (0, 15*25+25), (800, 15*25+25), 1)

    # Print each of the 15 rows.
    for row in range(15):
        # Create the string for this row on the board.
        for column in range(30):
            item = board[column][row]
            if item.isdigit():
                screen.blit(sonar_device_small, (column*25+25, row*25+25))
                render_text(item, (column*25+37.5, row*25+37.5), True, font=smallfont)
            elif item == 'X':
                screen.blit(sonar_device_small, (column*25+25, row*25+25))

    # Print the numbers across the bottom of the board.



def getRandomChests(numChests):
    # Create a list of chest data structures (two-item lists of x, y int coordinates).
    chests = []
    while len(chests) < numChests:
        newChest = [random.randint(0, 29), random.randint(0, 14)]
        if newChest not in chests: # Make sure a chest is not already here.
            chests.append(newChest)
    return chests

def isOnBoard(x, y):
    # Return True if the coordinates are on the board; otherwise, return False.
    return x >= 0 and x <= 59 and y >= 0 and y <= 14

def makeMove(board, chests, x, y):
    # Change the board data structure with a sonar device character. Remove treasure chests from the chests list as they are found.
    # Return False if this is an invalid move.
    # Otherwise, return the string of the result of this move.
    smallestDistance = 100 # Any chest will be closer than 100.
    for cx, cy in chests:
        distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))

        if distance < smallestDistance: # We want the closest treasure chest.
            smallestDistance = distance

    smallestDistance = round(smallestDistance)

    if smallestDistance == 0:
        # xy is directly on a treasure chest!
        chests.remove([x, y])
        return 'You have found a sunken treasure chest!'
    else:
        if smallestDistance < 10:
            board[x][y] = str(smallestDistance)
            return 'Distance to treasure from sonar device: %s' % (smallestDistance)
        else:
            board[x][y] = 'X'
            return 'All treasure chests out of range.'

def enterPlayerMove(previousMoves, xm, ym):
    global result
    # Let the player enter their move. Return a two-item list of int xy coordinates.
    move = (xm/25-1, ym/25-1)

    if isOnBoard(int(move[0]), int(move[1])):
        if [int(move[0]), int(move[1])] in previousMoves:
            result = 'You already moved there.'
            return None, None
        return [int(move[0]), int(move[1])]

def showInstructions():
    run = True
    while run:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    run = False
        screen.fill((0, 0, 0))
        render_text('Instructions:', (0, 0), font=smallfont)
        render_text('You are the captain of the Simon, a treasure-hunting ship. Your current mission', (0, 25), font=smallfont)
        render_text('is to use sonar devices to find three sunken treasure chests at the bottom of', (0, 50), font=smallfont)
        render_text('the ocean. But you only have cheap sonar that finds distance, not direction.', (0, 75), font=smallfont)

        render_text('Enter the coordinates to drop a sonar device. The ocean map will be marked with', (0, 125), font=smallfont)
        render_text('how far away the nearest chest is, or an blank device if it is beyond the sonar device\'s', (0, 150), font=smallfont)
        render_text('range. For example, the chest symbols are where chests are. The sonar device shows a', (0, 175), font=smallfont)
        render_text('3 because the closest chest is 3 spaces away.', (0, 200), font=smallfont)
        pg.draw.rect(screen, (0, 0, 255), pg.Rect(25, 225+25, 750, 125))
        for i in range(30):
            render_text(str(i+1), (i*25+37.5, 212.5+25), True, font=smallfont)
            render_text(str(i+1), (i*25+37.5, 362.5+25), True, font=smallfont)
            pg.draw.line(screen, (255, 255, 255), (i*25+25, 200+25), (i*25+25, 375+25), 1)
        pg.draw.line(screen, (255, 255, 255), (30*25+25, 200+25), (30*25+25, 375+25), 1)
        
        for i in range(5):
            render_text(str(i+1), (12.5, i*25+237.5+25), True, font=smallfont)
            render_text(str(i+1), (787.5, i*25+237.5+25), True, font=smallfont)
            pg.draw.line(screen, (255, 255, 255), (0, i*25+225+25), (800, i*25+225+25), 1)
        pg.draw.line(screen, (255, 255, 255), (0, 5*25+225+25), (800, 5*25+225+25), 1)
        screen.blit(chest_small, (125, 300))
        screen.blit(chest_small, (375, 300))
        screen.blit(chest_small, (375, 350))
        screen.blit(sonar_device_small, (200, 300))
        render_text('3', (212.5, 312.5), True, font=smallfont)
        render_text('(In the real game, the chests are not visible in the ocean.)', (0, 400), font=smallfont)
        render_text('Press SPACE to continue.', (0, 425), font=smallfont)
        pg.display.update()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    run = False
        screen.fill((0, 0, 0))
        render_text('When you drop a sonar device directly on a chest, you retrieve it and the other', (0, 0), font=smallfont)
        render_text('sonar devices update to show how far away the next nearest chest is. The chests', (0, 25), font=smallfont)
        render_text('are beyond the range of the sonar device on the left, so it shows an X.', (0, 50), font=smallfont)
        pg.draw.rect(screen, (0, 0, 255), pg.Rect(25, 225-125, 750, 125))
        for i in range(30):
            render_text(str(i+1), (i*25+37.5, 212.5-125), True, font=smallfont)
            render_text(str(i+1), (i*25+37.5, 362.5-125), True, font=smallfont)
            pg.draw.line(screen, (255, 255, 255), (i*25+25, 200-125), (i*25+25, 375-125), 1)
        pg.draw.line(screen, (255, 255, 255), (30*25+25, 200-125), (30*25+25, 375-125), 1)
        
        for i in range(5):
            render_text(str(i+1), (12.5, i*25+237.5-125), True, font=smallfont)
            render_text(str(i+1), (787.5, i*25+237.5-125), True, font=smallfont)
            pg.draw.line(screen, (255, 255, 255), (0, i*25+225-125), (800, i*25+225-125), 1)
        pg.draw.line(screen, (255, 255, 255), (0, 5*25+225-125), (800, 5*25+225-125), 1)
        screen.blit(sonar_device_small, (125, 300-150))
        screen.blit(chest_small, (375, 300-150))
        screen.blit(chest_small, (375, 350-150))
        screen.blit(sonar_device_small, (200, 300-150))
        render_text('7', (212.5, 312.5-150), True, font=smallfont)
        render_text('The treasure chests don\'t move around. Sonar devices can detect treasure chests', (0, 250), font=smallfont)
        render_text('up to a distance of 9 spaces. Try to collect all 3 chests before running out of', (0, 275), font=smallfont)
        render_text('sonar devices. Good luck!', (0, 300), font=smallfont)
        render_text('Press SPACE to start playing.', (0, 325), font=smallfont)
        render_text('This program is based on Al Sweigart\'s Sonar Treasure Hunt.', (0, 350), font=smallfont)
        pg.display.update()

screen = pg.display.set_mode((800, 725))
pg.display.set_caption('Sonar Treasure Hunt')
sonar_device = pg.transform.scale(pg.image.load('sonar_device.png').convert_alpha(), (40, 40))
sonar_device_gray = pg.transform.scale(pg.image.load('sonar_device_gray.png').convert_alpha(), (40, 40))
sonar_device_small = pg.image.load('sonar_device_small.png').convert_alpha()
chest = pg.image.load('chest.png').convert_alpha()
chest_gray = pg.image.load('chest_gray.png').convert_alpha()
chest_small = pg.image.load('chest_small.png').convert_alpha()
start = True
while start:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == K_SPACE:
                start = False
            elif event.key == K_RETURN:
                showInstructions()
                start = False
    screen.fill((0, 0, 0))
    render_text('Welcome to Sonar Treasure Hunt!', (0, 0))
    render_text('Press SPACE to start playing.', (0, 50))
    render_text('Press ENTER to view the instructions.', (0, 100))
    pg.display.update()

while True:
    # Game setup
    sonarDevices = 20
    theBoard = getNewBoard()
    theChests = getRandomChests(3)
    drawBoard(theBoard)
    previousMoves = []
    result = ''
    while sonarDevices > 0:
        xm, ym = None, None
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                xp, yp = event.pos
                if yp > 25 and xp > 25 and yp < 400 and xp < 775:
                    xm, ym = xp, yp
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        drawBoard(theBoard)
        render_text('Sonar devices left:', (0, 475))
        for i in range(20):
            if i < sonarDevices:
                screen.blit(sonar_device, (i*40, 525))
            else:
                screen.blit(sonar_device_gray, (i*40, 525))
        found_chests = 3 - len(theChests)
        render_text('Chests found:', (0, 575))
        for i in range(3):
            if i < found_chests:
                screen.blit(chest, (i*40, 625))
            else:
                screen.blit(chest_gray, (i*40, 625))        
        if xm != None and ym != None:
            x, y = enterPlayerMove(previousMoves, xm, ym)
            if x == y == None:
                render_text(result, (0, 425))
                pg.display.update()
                continue
            previousMoves.append([x, y]) # We must track all moves so that sonar devices can be updated.

            moveResult = makeMove(theBoard, theChests, x, y)
            if moveResult == False:
                pg.display.update()
                render_text(result, (0, 425))
                continue
            else:
                if moveResult == 'You have found a sunken treasure chest!':
                    # Update all the sonar devices currently on the map.
                    for x, y in previousMoves:
                        makeMove(theBoard, theChests, x, y)
                drawBoard(theBoard)
                result = moveResult
            sonarDevices -= 1

        if len(theChests) == 0:

            break
        render_text(result, (0, 425))
        pg.display.update()

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
        screen.fill((0, 0, 0))
        if sonarDevices == 0:
            render_text('We\'ve run out of sonar devices! Now we have to', (0, 425))
            render_text('turn the ship around and head for home with', (0, 475))
            render_text('treasure chests still out there! Game over.', (0, 525))
            render_text('The remaining chests are on the above map.', (0, 575))
            render_text('Press SPACE to play again.', (0, 625))
            drawBoard(getNewBoard())
            for x, y in theChests:
                screen.blit(chest_small, (x*25+25, y*25+25))
        else:
            render_text('You have found all the sunken treasure chests!', (0, 425))
            render_text('Congratulations and good game!', (0, 475))
            render_text('Press SPACE to play again.', (0, 525))
            drawBoard(getNewBoard())          
        pg.display.update()