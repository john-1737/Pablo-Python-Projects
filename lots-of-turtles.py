import turtle
import sys
import random


turtles = []

def outside_screen(t):
    x, y = t.pos()
    if x > 500 or x < -500 or y > 500 or y < -500:
        return True
    else:
        return False

def start_game():
    start_text.clear()
    new_turtle()
    while True:
        move_turtles()

def new_turtle():
    t = turtle.Turtle()
    turtles.append(t)
    t.shape('turtle')
    update_turtles(len(turtles))

def one_hundred_turtles():
    for x in range(0, 100):
        new_turtle()

def move_turtles():
    for t in turtles:
        t.speed(0)
        t.forward(random.randrange(150))
        t.right(random.randrange(360))
        t.color(random.randrange(100)/100, random.randrange(100)/100, random.randrange(100)/100)
        if outside_screen(t):
            for x in range(0, 2):
                new_turtle()
            t.home()

def update_turtles(num_turtles):
    number_of_turtles.clear()
    number_of_turtles.up()
    number_of_turtles.goto(0, 400)
    number_of_turtles.down()
    number_of_turtles.write('Number of turtles : ' + str(num_turtles), align='center', font=('Arial', 26, 'normal'))

def close():
    turtle.bye()


s = turtle.Screen()
s.setup(width=1000, height=1000)
start_text = turtle.Turtle()
start_text.write('''Turtle Simulation! Press the SPACE key to start the simulation.
The turtle draws randomly. When it hits the edge, 3 new turtles spawn.
Press S to spawn a turtle. Press H to spawn a hundred turtles.
Press X to exit.''', align=('center'), font=('Arial', 26, 'normal'))
start_text.ht()

number_of_turtles = turtle.Turtle()
number_of_turtles.ht()

s.listen()
s.onkey(start_game, 'space')
s.onkey(new_turtle, 's')
s.onkey(one_hundred_turtles, 'h')
s.onkey(close, 'x')

s.mainloop()