from turtle import *
from random import randint

class branch:
    def __init__(self, angle, length, pos, direction, repeats):
        self.angle = angle
        self.length = length
        self.repeats = repeats
        self.turtle = Turtle()
        self.turtle.goto(pos)
        self.turtle.setheading(direction)
        self.move()
        
    def move(self):
        self.turtle.forward(self.length)
        self.split()

    def split(self):
        self.turtle.setheading(0)
        self.length *= 1
        self.repeats -= 1
        if self.repeats != -1:
            self.turtle.right(self.angle)
            branch(self.angle, self.length, self.turtle.pos(), self.turtle.heading(), self.repeats)
            self.turtle.left(self.angle * 2)
            self.move()
        else:
            return

branch(45, 50, (100, 100), 0, 8)