"""This example starts learning about pygame"""
import pygame as pg
import sys
import random as ra
from tkinter import messagebox
if not messagebox.askokcancel(message='This game requires a joystick controller connected by USB to the computer. It is designed to work with a Sony PS4 joytick. If you do not have a joystick, press Cancel. You can also play the version\
 that uses a computer keyboard.'):
    sys.exit()
two_player = None
# Initialize Pygame
pg.init()

def handle_joyevent(event, player, winner):
    joy_control = 0 if player == 'x' else 2
    if event.type == pg.JOYBUTTONDOWN and winner == None:
        if event.button == 7+(joy_control / 2):
            pos_x, pos_y = cursor
            player = add_shape(((pos_x * 200) + 100, (pos_y * 200) + 100), player)
    if event.type == pg.JOYAXISMOTION:
        if abs(round(event.value, 2)) == 1:
            joy_control = 0 if player == 'x' else 2
            if event.axis == 0+joy_control:
                if event.value <= 0:
                    if cursor[0] != 0:
                        cursor[0] -= 1
                else:
                    if cursor[0] != 2:
                        cursor[0] += 1           
            elif event.axis == 1+joy_control:
                if event.value <= 0:
                    if cursor[1] != 0:
                        cursor[1] -= 1               
                else:
                    if cursor[1] != 2:
                        cursor[1] += 1
    return player                

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pg.display.set_mode((WIDTH, HEIGHT + 100))
pg.display.set_caption("Tic Tac Toe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
current_player = 'x'

board = {}
for i in (100, 300, 500):
    for j in (100, 300, 500):
        board[i, j] = None

# Initialize font
pg.font.init()
font = pg.font.SysFont(None, 48)
instruction_font = pg.font.SysFont(None, 25)

# Function to render text
def render_text(text, pos, font, bold=True):
    text_surface = font.render(text, bold, WHITE)
    screen.blit(text_surface, pos)

def draw_lines():
    pg.draw.line(screen, WHITE, (0, HEIGHT // 3), (WIDTH, HEIGHT//3), 5)
    pg.draw.line(screen, WHITE, (0, (HEIGHT // 3)*2), (WIDTH, (HEIGHT//3)*2), 5)
    pg.draw.line(screen, WHITE, (HEIGHT // 3, 0), (HEIGHT // 3, WIDTH), 5)
    pg.draw.line(screen, WHITE, ((HEIGHT // 3) * 2, 0), ((HEIGHT // 3) * 2, WIDTH), 5)

def draw_O(pos):
    pg.draw.circle(screen, BLUE, pos, 90, width=10)

def draw_X(pos):
    x, y = pos[0], pos[1]
    pg.draw.line(screen, RED, (x - 80, y - 80), (x + 80, y + 80), 10)
    pg.draw.line(screen, RED, (x - 80, y + 80), (x + 80, y - 80), 10)

def add_shape(pos, player):
    square_pos = ((pos[0] // 200) * 200) + 100, ((pos[1] // 200) * 200) + 100
    if board[square_pos] == None:
        if player == 'x':
            x_list.append(square_pos)
        else:
            o_list.append(square_pos)
        board[square_pos] = player
        if two_player == True:
            player = {'x':'o', 'o':'x'}[player]
        else:
            computer_move(board)
    cursor = [0, 0]        
    return player

def check_win(board):
    for i in (100, 300, 500):
        win_column = []
        for j in (100, 300, 500):
            win_column.append(board[i,j])
        if win_column[0] == win_column[1] == win_column[2] and win_column[0] != None:
            return win_column[0]
    for i in (100, 300, 500):
        win_row = []
        for j in (100, 300, 500):
            win_row.append(board[j,i])
        if win_row[0] == win_row[1] == win_row[2] and win_row[0] != None:
            return win_row[0]
    if board[100, 100] == board[300,300] == board[500,500] and board [100, 100] != None:
        return board[100, 100]
    if board[100, 500] == board[300,300] == board[500,100] and board [100, 500] != None:
        return board[100, 100]

def computer_move(board):
    '''if blank_spaces(board) != []:
        i = ra.choice(blank_spaces(board))
    else:
        i = None'''
    for i in blank_spaces(board):
        temp_board = board.copy()
        temp_board[i] = 'o'
        if check_win(temp_board):
            o_list.append(i)
            board[i] = 'o'
            check_win(board)
            return
    for i in blank_spaces(board):
        temp_board = board.copy()
        temp_board[i] = 'x'
        if check_win(temp_board):
            o_list.append(i)
            board[i] = 'o'
            check_win(board)
            return
    #o_list.append(ra.choice(blank_spaces(board)))
    o_list.append(i)
    board[i] = 'o'
    check_win(board)
    cursor = [0, 0]

blank_spaces = lambda board : [i for i in board if board[i] == None]

x_list = []
o_list = []
winner = None
# Main game loop
message = ""

joystick = pg.joystick.Joystick(0)
joysticks = {}

while two_player == None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.JOYBUTTONDOWN:
            if event.button == 9:
                two_player = False
            elif event.button == 10:
                two_player = True
            elif event.button == 0:
                pg.quit()
                sys.exit()
    render_text('Welcome to Tic Tac Toe!', (0, 25), instruction_font, False)
    render_text('Players take turns placing X and O characters on the board.', (0, 50), instruction_font, False)
    render_text('Player X places Xs on the board and player O places Os on the board.', (0, 75), instruction_font, False)
    render_text('If there are three Xs in a row, column, or diagonal, player X wins.', (0, 100), instruction_font, False)
    render_text('If there are three Os in a row, column, or diagonal, player O wins.', (0, 125), instruction_font, False)
    render_text('Players can move their cursor with the joystick and select by pressing it.', (0, 150), instruction_font, False)
    render_text('Player X uses the left joystick and player O uses the right one.', (0, 175), instruction_font, False) 
    render_text('Keep in mind, you can block the other player by placing an X or O', (0, 200), instruction_font, False)
    render_text('where they could place one and win!', (0, 225), instruction_font, False)
    render_text('If 2 players are playing, press R1 on your joystick to begin.', (0, 250), instruction_font, False)
    render_text('If 1 player is playing, press L1 to play against the computer.', (0, 275), instruction_font, False)
    pg.display.update()
cursor = [0, 0]
while True:
    for event in pg.event.get():
        current_player = handle_joyevent(event, current_player, winner)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.JOYBUTTONDOWN:
            if event.button == 0:
                pg.quit()
                sys.exit()

            if event.type == pg.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joystick = pg.joystick.Joystick(event.device_index)
                joysticks[joystick.get_instance_id()] = joystick
                #print(f"Joystick {joystick.get_instance_id()} connencted")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                #print(f"Joystick {event.instance_id} disconnected")

    # Clear the screen
    screen.fill(BLACK)

     # Draw the red line in the middle of the screen
    draw_lines()
    for i in x_list:
        draw_X(i)
    for i in o_list:
        draw_O(i)
    pg.draw.rect(screen, (255, 0, 0), pg.Rect(cursor[0] * 200, cursor[1] * 200, 200, 200), 5)    
    
    winner = check_win(board)
    if winner:
        render_text(f'{winner} wins!', (50, 625), font)
    else:
        if blank_spaces(board):
            render_text(f'{current_player}\'s turn', (50, 625), font)
        else:
            render_text('It\'s a tie!',(50, 625), font)
        
    
    # Render the message
    # Update the display
    pg.display.update()