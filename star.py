import turtle
t = turtle.Turtle()
def drawstar(size,points):
    t.reset()
    for x in range(0,points):
         t.forward(size)
         t.left((360/points) + 180)

drawstar(100,5)
input()