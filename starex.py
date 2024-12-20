import turtle
t = turtle.Turtle()

def mystar(size, filled, points):
    if filled == True:
        t.begin_fill()
    for x in range(1,(points*2) + 1):
        t.forward(size)
        if x % 2 ==0:
            t.left(175)
        else:
            t.left(225)
    if filled == True:
        t.end_fill()

t.color(0.9,0.75,0)
mystar(100, True, 9)
input()