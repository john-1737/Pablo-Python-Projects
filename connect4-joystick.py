import pygame as pg
from sys import exit
from copy import deepcopy
from random import randint, choice

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WIDTH, HEIGHT = 700, 600
turn=RED
two_player = None
pg.font.init()
font = pg.font.SysFont(None, 48)

board = [[] for i in range(0, 7)]

def ai_move(board):
    temp_board = deepcopy(board)
    for i, j in enumerate(temp_board):
        j.append(YELLOW)
        if check_win(temp_board) == RED:
            board[i].append(YELLOW)
            return
        else:
            temp_board = deepcopy(board)
    for i, j in enumerate(temp_board):
        j.append(RED)
        if check_win(temp_board) == RED:
            board[i].append(YELLOW)
            return
        else:
            temp_board = deepcopy(board)
    for i, j in enumerate(temp_board):
        j.append(YELLOW)
        temp_board[i + 3].append(YELLOW)
        if check_win(temp_board) == YELLOW:
            if randint(0, 1):
                board[i].append(YELLOW)
            else:
                board[i + 3].append(YELLOW)
            return
        else:
            temp_board = deepcopy(board)
        if i == 3:
            break
    for i, j in enumerate(temp_board):
        j.append(RED)
        temp_board[i + 3].append(RED)
        if check_win(temp_board) == RED:
            if randint(0, 1):
                board[i].append(YELLOW)
            else:
                board[i + 3].append(YELLOW)
            return
        else:
            temp_board = deepcopy(board)
        if i == 3:
            break
    for i, j in enumerate(temp_board):
        j.append(YELLOW)
        temp_board[i + 1].append(YELLOW)
        if check_win(temp_board) == YELLOW:
            if randint(0, 1):
                board[i].append(YELLOW)
            else:
                board[i + 1].append(YELLOW)
            return
        else:
            temp_board = deepcopy(board)
        if i == 6:
            break
    for i, j in enumerate(temp_board):
        j.append(RED)
        temp_board[i + 3].append(RED)
        if check_win(temp_board) == RED:
            if randint(0, 1):
                board[i].append(YELLOW)
            else:
                board[i + 3].append(YELLOW)
            return
        else:
            temp_board = deepcopy(board)
        if i == 3:
            break
    board[choice(board)].append(YELLOW)
            
def handle_joyevent(event, player, winner):
    global cursor
    if player == RED:
        joy_control = 0
    else:
        joy_control = 2
        """if event.type == pg.JOYBUTTONDOWN and winner == None:
        if event.button == 7+(joy_control / 2):
            if place_disk(cursor, turn): 
                if two_player:
                    turn = {RED:YELLOW, YELLOW:RED}[turn]
                else:
                    while True:
                        ai_move(board)
                        for i in board:
                            if len(i) == 7:
                                retry = False """
    if event.type == pg.JOYAXISMOTION:
        if abs(round(event.value, 2)) == 1:
            if player == RED:
                joy_control = 0
            else:
                joy_control = 2
            if event.axis == 0+joy_control:
                if event.value <= 0:
                    if cursor != 0:
                        cursor -= 1
                else:
                    if cursor != 6:
                        cursor += 1               

def draw_circle(pos, color):
    pg.draw.circle(screen, color, pos, 45, width=50)

def display_board(board):
    for i in range(1, 7):
        pg.draw.line(screen, WHITE, ((WIDTH // 7) * i, 0), ((WIDTH // 7) * i, HEIGHT), 5)
    pg.draw.line(screen, WHITE, (0, HEIGHT), (WIDTH, HEIGHT), 5)
    x_positions = (50, 150, 250, 350, 450, 550, 650)
    y_positions = (550, 450, 350, 250, 150, 50) #Note: the y positions are backwards because the disks fall to the bottom.
    for i, j in enumerate(board):
        for k, l in enumerate(j):
            draw_circle((x_positions[i], y_positions[k]), l)      
        if i == cursor:
            pg.draw.polygon(screen, WHITE, ((x_positions[i] - 40, 10), (x_positions[i] + 40, 10), (x_positions[i], 25)))

def place_disk(x, turn):
    global error
    if len(board[x]) == 6:
        error = 'That column is full.'
        return False
    else:
        board[x].append(turn)
        error = ''
        return True
        
def render_text(text, pos, font, bold=True, color=WHITE):
    text_surface = font.render(text, bold, color)
    screen.blit(text_surface, pos)

def check_tie(board):
    for i in board:
        if len(i) != 6:
            return False
    return True

def check_win(board):
    check_board = deepcopy(board)
    for i in check_board:
        while True:
            if len(i) == 6:
                break
            else:
                i.append(None)
    for column in range(4):
        for row in range(6):
            disk1 = check_board[column][row]
            disk2 = check_board[column + 1][row]
            disk3 = check_board[column + 2][row]
            disk4 = check_board[column + 3][row]
            if disk1==disk2==disk3==disk4==RED or disk1==disk2==disk3==disk4==YELLOW:
                return disk1
    
    for column in range(7):
        for row in range(3):
            disk1 = check_board[column][row]
            disk2 = check_board[column][row + 1]
            disk3 = check_board[column][row + 2]
            disk4 = check_board[column][row + 3]
            if disk1==disk2==disk3==disk4==RED or disk1==disk2==disk3==disk4==YELLOW:
                return disk1

    for column in range(4):
        for row in range(3):
            disk1 = check_board[column][row]
            disk2 = check_board[column + 1][row + 1]
            disk3 = check_board[column + 2][row + 2]
            disk4 = check_board[column + 3][row + 3]
            if disk1==disk2==disk3==disk4==RED or disk1==disk2==disk3==disk4==YELLOW:
                return disk1
            
            disk1 = check_board[column + 3][row]
            disk2 = check_board[column + 2][row + 1]
            disk3 = check_board[column + 1][row + 2]
            disk4 = check_board[column][row + 3]
            if disk1==disk2==disk3==disk4==RED or disk1==disk2==disk3==disk4==YELLOW:
                return disk1
            
    return False

pg.joystick.init()
joystick = pg.joystick.Joystick(0)
joysticks = {}

cursor = -1      
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT + 100))
pg.display.set_caption("Connect 4")
error = ''
while two_player == None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.JOYBUTTONDOWN:
            if event.button == 9:
                two_player = False         
            elif event.button == 10:
                two_player = True
    screen.fill((0, 0, 0))
    display_board(board)
    render_text('Press 1 key for 1-player mode.', (50, 600), font, color=WHITE)
    render_text('Press 2 key for 2-player mode.', (50, 650), font, color=WHITE)
    pg.display.update()

winner = None
cursor = 0
while True:
    for event in pg.event.get():
        handle_joyevent(event, turn, winner)
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if player == RED:
                joy_control = 0
            else:
                joy_control = 2
            if event.button == 7+(joy_control / 2) and not (winner or tie):
                if place_disk(*event.pos, turn): 
                    if two_player:
                        turn = {RED:YELLOW, YELLOW:RED}[turn]
                    else:
                        while True:
                            ai_move(board)
                            for i in board:
                                if len(i) == 7:
                                    retry = False

        if event.type == pg.JOYDEVICEADDED:
            joystick = pg.joystick.Joystick(event.device_index)
            joysticks[joystick.get_instance_id()] = joystick

        if event.type == pg.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]

    screen.fill((0, 0, 0))
    display_board(board)
    player = {RED:'red', YELLOW:'yellow'}
    winner = check_win(board)
    tie = check_tie(board)
    if winner:
        render_text(f'{player[winner]} wins!', (50, 610), font)
    elif tie:
        render_text('It\'s a tie!', (50, 610), font)
    else:
        render_text(f'{player[turn]}\'s turn', (50, 610), font)
    render_text(error, (50, 650), font, color=RED)
    pg.display.update()