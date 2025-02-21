from math import sin, cos, pi
#from numpy import 
import pygame as pg
from tkinter import simpledialog

def create_polygon(sides):
    poss = [(200, 200)]
    angle = 0
    for i in range(1, sides + 1):
        x, y = poss[-1]
        rad = deg_to_rad(angle)
        x += (400 /sides) * cos(rad)
        y += (400/sides) * sin(rad)
        angle += (360/sides)
        poss.append((x, y))
        print(angle)
    return poss

def deg_to_rad(deg):
    distance = 2*pi
    return (deg / 360) * distance

sides = simpledialog.askinteger(title='Sides', prompt='How many sides?')
pg.init()
screen = pg.display.set_mode((1000, 1000))
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            raise SystemExit
    pg.draw.polygon(screen,(255, 0, 0),create_polygon(sides))
    pg.display.update()