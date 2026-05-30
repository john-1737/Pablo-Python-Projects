import pygame as pg
from pygame.locals import *
from time import time

keys = list('abcdefghijklmnopqrstuvwxyz1234567890;')
keys.append('Return')
typed_keys = []
enter_symbol = '↳'

def teach(finger_pos, key):
    typing = True
    while typing:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == TEXTINPUT and event.text.lower() == key:
                typing = False
            if control_keys(event):
                return
            screen.fill((255, 255, 255))
            render_text(finger_pos, (0, 0))
            render_text(key, (0, 50), typing_font)
            pg.display.update()

    end = True
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if control_keys(event, True):
                return
        screen.fill((255, 255, 255))
        render_text('Good job! Press the space key to continue.', (0, 0))
        render_text(key, (0, 50), typing_font, color=(0, 255, 0))
        pg.display.update()

def scrolling(text):
    orig_length = len(text)
    correct_length = 0
    color = (0, 0, 0)
    start_time = time()
    while text:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == TEXTINPUT:
                if event.text.lower() == text[0]:
                    if color == (255, 0, 0):
                        correct_length -= 1
                    text = text[1:]
                    color = (0, 255, 0)
                    correct_length += 1
                else:
                    color = (255, 0, 0)
            if control_keys(event, True):
                return
            screen.fill((255, 255, 255))
            render_text(f'{correct_length} out of {orig_length} correct.', (0, 0))
            render_text(text, (0, 50), typing_font, color)
            pg.display.update()

    end = True
    total_time = time() - start_time
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if control_keys(event, True):
                return
            screen.fill((255, 255, 255))
            render_text('Good job! Press the space key to continue.', (0, 0))
            render_text(f'You got {int(round(correct_length/orig_length*100, 0))}% correct letters in {round(total_time, 2)} seconds!', (0, 50))
            pg.display.update()

def game(text):
    orig_length = len(text)
    correct_length = 0
    color = (0, 255, 0)
    start_time = time()
    while text:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if check_key_press(event) == text[0]:
                text = text[1:]
                color = (0, 255, 0)
                correct_length += 1
            elif check_key_press(event) != None:
                color = (255, 0, 0)
            if control_keys(event):
                return

        screen.fill((0, 0, 0))
        pg.draw.polygon(screen, color, ((5, 55), (45, 55), (25, 75), (45, 95), (5, 95)))
        render_text(f'You\'ve gotten {correct_length} out of {orig_length} correct.', (0, 0), game_font, (255, 255, 255))
        render_text(text, (50, 50), typing_font, (255, 255, 255))
        pg.display.update()

    end = True
    total_time = time() - start_time
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if control_keys(event, True):
                return
            screen.fill((255, 255, 255))
            render_text('Good job! Press the space key to continue.', (0, 0))
            render_text(f'You got {int(round(correct_length/orig_length*100, 0))}% correct letters in {round(total_time, 2)} seconds!', (0, 50))
            pg.display.update()

def standard(text_list):
    correct_length = 0
    orig_length = len(''.join(text_list))
    typing_char = 0
    char_colors = []
    start_time = time()
    while text_list:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if check_key_press(event) == text_list[0][typing_char]:
                if len(char_colors) > 1 and char_colors[-1] == (255, 0, 0):
                    del char_colors[-1]
                    correct_length -= 1
                char_colors.append((0, 255, 0))
                correct_length += 1
                typing_char += 1
            elif check_key_press(event) != None:
                if len(char_colors) > 1 and char_colors[-1] == (255, 0, 0):
                    del char_colors[-1]
                char_colors.append((255, 0, 0))
            if control_keys(event):
                return

        screen.fill((255, 255, 255))
        if typing_char == len(text_list[0]):
            del text_list[0]
            typing_char = 0
            char_colors = []
        if text_list == []:
            break
        for i in range(1 if len(text_list) == 1 else 2):
            pos_counter = 0
            for k, j in enumerate(text_list[i]):
                try:
                    color = char_colors[k]
                    assert i == 0
                except:
                    color = (0, 0, 0)
                if j.lower() in 'abcdefghijklmnopqrstuvwxyz!?\', 1234567890.':
                    text_surface = typing_font.render(j, True, color)
                elif j == '↳':
                    text_surface = replace_color(enter_key, color)
                else:
                    continue
                screen.blit(text_surface, (pos_counter, i*50))
                pos_counter += text_surface.get_rect().width

        pg.display.update()

    end = True
    total_time = time() - start_time
    while end:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if control_keys(event, True):
                return
            screen.fill((255, 255, 255))
            render_text('Good job! Press the space key to continue.', (0, 0))
            render_text(f'You got {int(round(correct_length/orig_length*100, 0))}% correct letters in {round(total_time, 2)} seconds!', (0, 50))
            pg.display.update()

def replace_color(surface, replace_color):
    # Create a PixelArray from the surface
    pixel_array = pg.PixelArray(surface)
    # Replace all pixels of find_color with replace_color
    pixel_array.replace((0,0,0), replace_color)
    # Delete the PixelArray to unlock the surface for blitting
    del pixel_array
    return surface

def check_key_press(event):
    if event.type == TEXTINPUT:
        return event.text.lower()
    elif event.type == KEYDOWN and event.key == K_RETURN:
        return enter_symbol
    return None

def control_keys(event, end=False):
    if event.type == KEYDOWN:
        if event.key == K_LEFT and not current_item == 0:
            section(current_lesson, current_item - 1)
            return True
        elif event.key == K_RIGHT or (event.key == K_SPACE and end):
            if not current_item == len(lessons_list[current_lesson]) - 2:
                section(current_lesson, current_item + 1)
            else:
                main_menu()
            return True
        elif event.key == K_ESCAPE:
            main_menu()
            return True

def section(lesson, item):
    global current_lesson, current_item
    current_lesson, current_item = lesson, item
    exec(lessons_list[lesson][item+1])

def main_menu():
    scroll_position = 0
    length = 0
    level = None
    for i in lessons_list:
        ilevel = i[0].split('|')[0]
        if ilevel != level:
            level = ilevel
            length += 50
        length += 50
    while True:
        mouse_y = -1
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_position >= 0:
                    scroll_position -= 1
                elif event.button == 5 and scroll_position <= length-100:
                    scroll_position += 1
                elif event.button == 1:
                    mouse_y = event.pos[1] + scroll_position
        level = None
        length = 0
        screen.fill((255, 255, 255))
        for j, i in enumerate(lessons_list):
            ilevel, lesson, name = i[0].split('|')
            if ilevel != level:
                level = ilevel
                pg.draw.rect(screen, (0, 0, 255), pg.Rect(0, length-scroll_position, 800, 50))
                pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, length-scroll_position, 800, 50), 5)
                render_text(f'{level} Lessons', (10, length-scroll_position))
                length += 50
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, length-scroll_position, 800, 50), 5)
            if (mouse_y // 50) * 50 == length:
                section(j, 0)
                return
            render_text(f'{level}, {lesson}: {name}', (10, length-scroll_position))
            length += 50
        pg.display.update()

with open('typinglessons.txt') as f:
    lessons = f.read()

lessons = lessons.split('    ')
lessons_list = []
for i in lessons:
    lessons_list.append(i.strip().split('\n'))
del lessons_list[0]

screen = pg.display.set_mode((800, 100))
pg.display.set_caption('Typing Game')
pg.font.init()
font = pg.font.SysFont('Arial', 35)
smallfont = pg.font.SysFont('Arial', 17)
game_font = pg.font.SysFont(None, 48)
typing_font = pg.font.SysFont('monaco', 35)
enter_key = pg.image.load('enterkey.png').convert_alpha()

# Function to render text
def render_text(text, pos, font=font, color=(0, 0, 0)):
    pos_counter = 0
    for i in text:
        if i.lower() in 'abcdefghijklmnopqrstuvwxyz!?\', 1234567890.%:;':
            text_surface = font.render(i, True, color)
        elif i == '↳':
            text_surface = replace_color(enter_key, color)
        else:
            continue
        screen.blit(text_surface, (pos[0] + pos_counter, pos[1]))
        pos_counter += text_surface.get_rect().width

main_menu()