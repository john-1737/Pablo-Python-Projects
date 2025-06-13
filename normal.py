import turtle as t
from math import sqrt
from random import choice
class ball():
    def __init__(self):
        self.turtle = t.Turtle()
        self.turtle.shape('circle')
        self.turtle.speed(0)
        self.turtle.up()
        self.turtle.ht()
        self.turtle.goto(0, 400)
        self.turtle.down()
        self.turtle.st()
        self.turtle.speed(5)
    def move(self):
        self.turtle.setheading(choice((225, 315)))
        self.turtle.forward(sqrt(3200))
        if round(self.turtle.ycor(), 0) == 0:
            self.stack()
    def stack(self):
        global pile_level
        x = round(self.turtle.xcor(), 0)
        self.turtle.goto(self.turtle.xcor(), pile_level[int(x)])
        pile_level[int(x)] += 10

def draw_paths(y, pen):
    if y == 400:
        pen.setheading(270)
        pen.forward(400)
        return
    pen.color('gray')
    pen.ht()
    pen.speed(0)
    y += 40
    pen.setheading(225)
    pen.forward(sqrt(3200))
    pen2 = pen.clone()
    pen2.setheading(315)
    pen2.forward(sqrt(3200))
    draw_paths(y+40, pen)
    draw_paths(y+40, pen2)

pile_level = {key:-400 for key in range(-400, 400, 40)}
balls = []
for i in range(50):
    b = ball()
    balls.append(b)
for i in range(10):
    for j in balls:
        j.move()
s = t.Screen()
s.mainloop()