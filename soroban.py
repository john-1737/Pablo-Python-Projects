"""Soroban Japanese Abacus, by Al Sweigart al@inventwithpython.com
A simulation of a Japanese abacus calculator tool.
More info at: https://en.wikipedia.org/wiki/Soroban
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, artistic, math, simulation"""

NUMBER_OF_DIGITS = 10
import pygame as pg
from pygame.locals import *
pg.font.init()
font = pg.font.SysFont(None, 24)
smallfont = pg.font.SysFont(None, 20)

def main():
    global screen, show_letters
    screen = pg.display.set_mode((220, 355))
    pg.display.set_caption('Soroban')

    abacusNumber = 0  # This is the number represented on the abacus.
    show_letters = False
    typed_number = ''

    while True:  # Main program loop.
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                direction = 0
                if y >= 180 and y <= 200:
                    direction = 1
                elif y >= 220 and y <= 240:
                    direction = -1
                if direction and x >= 10 and x <= 210:
                    row = 9 - (x - 10) // 20
                    abacusNumber += 10 ** row * direction
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    abacusNumber += 1000000000
                elif event.key == K_a:
                    abacusNumber -= 1000000000
                elif event.key == K_w:
                    abacusNumber += 100000000
                elif event.key == K_s:
                    abacusNumber -= 100000000
                elif event.key == K_e:
                    abacusNumber += 10000000
                elif event.key == K_d:
                    abacusNumber -= 10000000
                elif event.key == K_r:
                    abacusNumber += 1000000
                elif event.key == K_f:
                    abacusNumber -= 1000000
                elif event.key == K_t:
                    abacusNumber += 100000
                elif event.key == K_g:
                    abacusNumber -= 100000
                elif event.key == K_y:
                    abacusNumber += 10000
                elif event.key == K_h:
                    abacusNumber -= 10000
                elif event.key == K_u:
                    abacusNumber += 1000
                elif event.key == K_j:
                    abacusNumber -= 1000
                elif event.key == K_i:
                    abacusNumber += 100
                elif event.key == K_k:
                    abacusNumber -= 100
                elif event.key == K_o:
                    abacusNumber += 10
                elif event.key == K_l:
                    abacusNumber -= 10
                elif event.key == K_p:
                    abacusNumber += 1
                elif event.key == K_SEMICOLON:
                    abacusNumber -= 1
                elif event.key == K_b:
                    show_letters = not show_letters
                elif event.key == K_BACKSPACE and typed_number:
                    typed_number = typed_number[:-1]
                elif event.key == K_RETURN and typed_number:
                    abacusNumber = int(typed_number)
                    typed_number = ''
            elif event.type == TEXTINPUT and event.text in '1234567890':
                typed_number += event.text
        # The abacus can't show negative numbers:
        if abacusNumber < 0:
            abacusNumber = 0  # Change any negative numbers to 0.
        # The abacus can't show numbers larger than 9999999999:
        if abacusNumber > 9999999999:
            abacusNumber = 9999999999
        screen.fill((0, 0, 0))
        displayAbacus(abacusNumber)
        render_text('Enter a number or up/down', (0, 240))
        render_text('letters, or press the up/down', (0, 265))
        render_text(f'buttons. Press B to {"hide" if show_letters else "show"}', (0, 290))
        render_text('the up/down letters.', (0, 315))
        render_text(typed_number, (0, 340))
        pg.display.update()
        continue

def displayAbacus(number):
    letters = ('qa', 'ws', 'ed', 'rf', 'tg', 'yh', 'uj', 'ik', 'op', 'p;')
    numberList = list(str(number).zfill(NUMBER_OF_DIGITS))

    hasBead = []  # Contains a True or False for each bead position.

    # Top heaven row has a bead for digits 0, 1, 2, 3, and 4.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '01234')

    # Bottom heaven row has a bead for digits 5, 6, 7, 8, and 9.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '56789')

    # 1st (topmost) earth row has a bead for all digits except 0.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '12346789')

    # 2nd earth row has a bead for digits 2, 3, 4, 7, 8, and 9.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '234789')

    # 3rd earth row has a bead for digits 0, 3, 4, 5, 8, and 9.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '034589')

    # 4th earth row has a bead for digits 0, 1, 2, 4, 5, 6, and 9.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '014569')

    # 5th earth row has a bead for digits 0, 1, 2, 5, 6, and 7.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '012567')

    # 6th earth row has a bead for digits 0, 1, 2, 3, 5, 6, 7, and 8.
    for i in range(NUMBER_OF_DIGITS):
        hasBead.append(numberList[i] in '01235678')

    # Convert these True or False values into O or | characters.
    abacusChar = []
    for i, beadPresent in enumerate(hasBead):
        if beadPresent:
            abacusChar.append('O')
        else:
            abacusChar.append('|')

    # Draw the abacus with the O/| characters.
    chars = abacusChar + numberList
    for i in range(1, 11):
        pg.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, 180), 2)
        if abacusChar[i-1] == 'O':
            pg.draw.circle(screen, (0, 0, 255), (i*20, 10), 8)
        if abacusChar[i+9] == 'O':
            pg.draw.circle(screen, (0, 0, 255), (i*20, 50), 8)
        for j in range(6):
            if abacusChar[j*10+19+i] == 'O':
                pg.draw.circle(screen, (255, 0, 0), (i*20, j*20+70), 8)
        render_text(f'+{letters[i-1][0]}' if show_letters else '+', (i*20, 190), True, font=smallfont)
        render_text(str(numberList[i-1]), (i*20, 210), True, font=smallfont)
        render_text(f'-{letters[i-1][1]}' if show_letters else '-', (i*20, 230), True, font=smallfont)
    pg.draw.line(screen, (255, 255, 255), (0, 0), (220, 0), 5)
    pg.draw.line(screen, (255, 255, 255), (0, 0), (0, 180), 5)
    pg.draw.line(screen, (255, 255, 255), (220, 0), (220, 180), 5)
    pg.draw.line(screen, (255, 255, 255), (0, 180), (220, 180), 5)
    pg.draw.line(screen, (255, 255, 255), (0, 60), (220, 60), 5)

def render_text(text, pos, center=False, color=(255, 255, 255), font=font):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

if __name__ == '__main__':
    main()