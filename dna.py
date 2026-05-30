"""DNA, by Al Sweigart al@inventwithpython.com
A simple animation of a DNA double-helix. Press Ctrl-C to stop.
Inspired by matoken https://asciinema.org/a/155441
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, artistic, scrolling, science"""

import random, sys, time
import pygame as pg
from pygame.locals import *


class nucleotides:
    def __init__(self, left_nucleotide):
        self.y = 400
        self.leftn = {'a': (64, 196, 255), 't': (158, 216, 57), 'g': (46, 95, 230), 'c': (238, 140, 255)}[left_nucleotide]
        self.rightn = {'t': (64, 196, 255), 'a': (158, 216, 57), 'c': (46, 95, 230), 'g': (238, 140, 255)}[left_nucleotide]

    def draw(self):
        pg.draw.rect(screen, self.leftn, pg.Rect(0, self.y, 100, 20))
        pg.draw.rect(screen, self.rightn, pg.Rect(100, self.y, 100, 20))

    def move(self):
        self.y -= 1

screen = pg.display.set_mode((200, 400))
pg.display.set_caption('DNA Animation')
dna = pg.image.load('dna-strand.png').convert_alpha()

dna_y = 400
nucleotide_clock = 0
clock = pg.time.Clock()
nucleotides_list = []

while True:  # Main program loop.
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()

    dna_y -= 1
    if dna_y == -200:
        dna_y = 0

    nucleotide_clock += 1
    nucleotide_clock %= 20
    screen.fill((255, 255, 255))

    if nucleotide_clock == 0:
        nucleotides_list.append(nucleotides(random.choice(('a', 't', 'g', 'c'))))

    for i in nucleotides_list:
        i.move()
        i.draw()

    for i in nucleotides_list[:]:
        if i.y == -20:
            nucleotides_list.remove(i)

    screen.blit(dna, (0, dna_y))
    screen.blit(dna, (0, dna_y+200))
    screen.blit(dna, (0, dna_y+400))
    pg.display.update()
    clock.tick(60)