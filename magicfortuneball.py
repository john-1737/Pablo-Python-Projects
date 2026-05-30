"""Magic Fortune Ball, by Al Sweigart al@inventwithpython.com
Ask a yes/no question about your future. Inspired by the Magic 8 Ball.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, humor"""

import random, time
import pygame as pg
from pygame.locals import *
from PIL import Image


def slowSpacePrint(text, interval=0.10):
    clock = pg.time.Clock()
    text = text.upper()
    show_text = ''
    text_iter = 0
    show_clock = interval * 60 - 1
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
        screen.fill((0, 0, 0))
        next_frame()
        if round(show_clock / 60, 2) == interval:
            if text_iter == len(text):
                break
            show_clock = 0
            if text[text_iter] == 'I':
                show_text += 'i '
            else:
                show_text += text[text_iter] + ' '
            text_iter += 1
        show_clock += 1
        render_text(show_text, (0, 150), smallfont)
        pg.display.update()
        clock.tick(60)

def wait(text, time):
    clock = pg.time.Clock()
    text = ' '.join(list(text.upper().replace('I', 'i')))
    show_clock = 0
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pg.quit()
                exit()
        screen.fill((0, 0, 0))
        next_frame()
        if round(show_clock / 60, 1) == time:
            break
        show_clock += 1
        render_text(text, (0, 150), smallfont)
        pg.display.update()
        clock.tick(60)

def next_frame():
    global frame
    frame += 1
    frame %= len(frames)
    screen.blit(frames[frame], (325, 0))

screen = pg.display.set_mode((800, 200))
pg.display.set_caption('Magic Fortune Ball')
pg.font.init()
font = pg.font.SysFont(None, 48)
smallfont = pg.font.SysFont(None, 24)

# Function to render text
def render_text(text, pos, font=font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def split_gif_into_frames(gif_path):
    """
    Splits an animated GIF into individual image frames.

    Args:
        gif_path (str): The path to the input GIF file.
        output_folder (str): The folder where individual frames will be saved.
    """
    frames = []
    with Image.open(gif_path) as im:
        for i in range(im.n_frames):
            im.seek(i)
            image_data = im.tobytes()
            image_size = im.size  # (width, height)
            image_mode = im.mode  # e.g., "RGB", "RGBA", "L"
            surface = pg.transform.scale(pg.image.frombytes(image_data, image_size, image_mode).convert_alpha(), (150, 150))
            frames.append(surface)
    frames.pop(0)
    return frames

frames = split_gif_into_frames('8ball.gif')
frame = 0
    
while True:
    slowSpacePrint('Welcome to Magic Fortune Ball!')
    wait('Welcome to Magic Fortune Ball!', 0.5)
    slowSpacePrint('ASK ME YOUR YES/NO QUESTION.')
    responded = False
    text = ''
    clock = pg.time.Clock()
    while not responded:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key == K_RETURN:
                    responded = True
            elif event.type == TEXTINPUT:
                text += event.text

        screen.fill((0, 0, 0))
        next_frame()
        render_text(' '.join(list('ASK ME YOUR YES/NO QUESTION.'.upper().replace('I', 'i'))), (0, 150), smallfont)
        if text == '':
            render_text('Enter your question', (0, 175), smallfont, (100, 100, 100))
        else:
            render_text(text + '|', (0, 175), smallfont)
        pg.display.update()
        clock.tick(60)


    # Display a brief reply:
    replies = [
        'LET ME THINK ON THIS...',
        'AN INTERESTING QUESTION...',
        'HMMM... ARE YOU SURE YOU WANT TO KNOW..?',
        'DO YOU THINK SOME THINGS ARE BEST LEFT UNKNOWN..?',
        'I MIGHT TELL YOU, BUT YOU MIGHT NOT LIKE THE ANSWER...',
        'YES... NO... MAYBE... I WILL THINK ON IT...',
        'I SHALL CONSULT MY VISIONS...',
        'YOU MAY WANT TO SIT DOWN FOR THIS...',
    ]
    slowSpacePrint(random.choice(replies))

    # Dramatic pause:
    slowSpacePrint('.' * random.randint(4, 12), 0.70)

    # Give the answer:
    slowSpacePrint('I HAVE AN ANSWER...', 0.20)
    wait('I HAVE AN ANSWER...', 1)
    answers = [
        'YES, FOR SURE',
        'MY ANSWER IS NO',
        'ASK ME LATER',
        'I AM PROGRAMMED TO SAY YES',
        'THE STARS SAY YES, BUT I SAY NO',
        'I DUNNO MAYBE',
        'FOCUS AND ASK ONCE MORE',
        'DOUBTFUL, VERY DOUBTFUL',
        'AFFIRMATIVE',
        'YES, THOUGH YOU MAY NOT LIKE IT',
        'NO, BUT YOU MAY WISH IT WAS SO',
    ]
    random_answer = random.choice(answers)
    slowSpacePrint(random_answer, 0.05)

    clock = pg.time.Clock()
    text = ' '.join(list(random_answer.replace('I', 'i')))
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
        next_frame()
        render_text(text, (0, 150), smallfont)
        render_text('Press SPACE to ask another question.', (0, 175), smallfont)
        pg.display.update()
        clock.tick(60)