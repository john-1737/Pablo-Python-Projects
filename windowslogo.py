import turtle
import time, this
t = turtle.Turtle()
def createsquare(red,green,blue):
    t.color(float(red),float(green),float(blue))
    t.begin_fill()
    for x in range (1,4):
        t.forward(50)
        t.left(90)
    t.forward(50)
    t.end_fill()

def space():
    t.up()
    t.forward(10)
    t.down()
    
t.up()
t.forward(5) 
t.down()   
createsquare(0,0.75,0)
space()
createsquare(1,1,0)
space()
createsquare(0,0,1)
space()
createsquare(1,0,0)
t.up()
time.sleep(3)