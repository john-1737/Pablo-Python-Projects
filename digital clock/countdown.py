import sys, time
import pygame as pg
from pygame.locals import *

screen = pg.display.set_mode((282, 190))
pg.display.set_caption('Countdown')
clockface = pg.image.load('clockface.png').convert_alpha()
digits = []
for i in range(10):
    digits.append(pg.image.load(f'digit{i}.png').convert_alpha())
colon = pg.image.load('colon.png').convert_alpha()
done = pg.image.load('done.png').convert_alpha()

# (!) Change this to any number of seconds:
secondsLeft = 0
clock = pg.time.Clock()
while True:
    running = True
    flash = True
    position = 0
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 134 and y <= 164:
                    if x >= 28 and x <= 75 and position != 0:
                        position -= 1
                    elif x >= 208 and x <= 280:
                        position += 1
                    elif x >= 88 and x <= 135:
                        secondsLeft -= {0:60,1:1}[position]
                    elif x >= 148 and x <= 195:
                        secondsLeft += {0:60,1:1}[position]
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE and position != 0:
                    position -= 1
                elif event.key == K_RETURN:
                    position += 1
                elif event.key == K_RIGHT:
                    secondsLeft += {0:60,1:1}[position]
                elif event.key == K_LEFT and position != 0:
                    secondsLeft -= {0:60,1:1}[position]
        secondsLeft %= 6000 #The highest number that can be displayed.
        if position >= 2:
            running = False
        minutes = str((secondsLeft // 60))
        seconds = str(secondsLeft % 60)

        minutes = minutes[-2:].zfill(2)
        seconds = seconds.zfill(2)
        screen.fill((0, 0, 0))
        screen.blit(clockface, (0, 0))
        if flash:
            for i, j in enumerate(minutes + seconds):
                screen.blit(digits[int(j)], (38+(i*50), 39))
        else:
            for i, j in enumerate([seconds, minutes][position]):
                screen.blit(digits[int(j)], (38+(i*50)+100-(position*100), 39))

        screen.blit(colon, (137, 39))
        pg.display.update()
        clock.tick(2)
        flash = not flash

    running = True
    paused = False
    while running:  # Main program loop.
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 134 and y <= 164:
                    if x >= 28 and x <= 75:
                        running = False
                    elif x >= 208 and x <= 280:
                        paused = not paused
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    running = False
                elif event.key == K_ENTER:
                    paused = not paused

        screen.fill((0, 0, 0))
        screen.blit(clockface, (0, 0))

        # Get the hours/minutes/seconds from secondsLeft:
        # For example: 7265 is 2 hours, 1 minute, 5 seconds.
        # So 7265 // 3600 is 2 hours:
        # And 7265 % 3600 is 65, and 65 // 60 is 1 minute:
        minutes = str(secondsLeft // 60)
        # And 7265 % 60 is 5 seconds:
        seconds = str(secondsLeft % 60)

        minutes = minutes[-2:].zfill(2)
        seconds = seconds.zfill(2)

        # Get the digit strings from the sevseg module:
        if secondsLeft == -1:
            break
        for i, j in enumerate(minutes + seconds):
            screen.blit(digits[int(j)], (38+(i*50), 39))
        screen.blit(colon, (137, 39))
        pg.display.update()
        clock.tick(1)
        if not paused:
            secondsLeft -= 1

    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 134 and y <= 164:
                    if x >= 28 and x <= 75:
                        running = False
                        secondsLeft = 0
            elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                running = False
                secondsLeft = 0
        screen.fill((0, 0, 0))
        screen.blit(clockface, (0, 0))
        screen.blit(done, (38, 39))
        pg.display.update()
        clock.tick(2)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 134 and y <= 164:
                    if x >= 28 and x <= 75:
                        running = False
                        secondsLeft = 0
            elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                running = False
                secondsLeft = 0
        screen.fill((0, 0, 0))
        screen.blit(clockface, (0, 0))
        pg.display.update()
        clock.tick(2)