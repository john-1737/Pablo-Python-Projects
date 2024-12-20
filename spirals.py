import turtle
import time
a = turtle.Turtle()
b = turtle.Turtle()
a.color(0,1,0)
b.color(1,0,0)
b.left(180)
for x in range(1,4):
    a.forward(100)
    b.forward(100)
    b.right(90)
    a.left(90)
for x in [80,60,40]:
    for i in range(1,3):
        b.forward(x)
        a.forward(x)
        b.right(90)
        a.left(90)

time.sleep(5.0)