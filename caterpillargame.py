import random
import turtle as t

t.bgcolor('yellow')
caterpillar = t.Turtle()
caterpillar.shape('square')
caterpillar.color('blue')
caterpillar.speed(1)
caterpillar.penup()
caterpillar.hideturtle()

leaf = t.Turtle()
leaf_shape = ((0,0), (14,2), (18,6), (20, 20), (6, 18), (2, 14))
t.register_shape('leaf', leaf_shape)
leaf.shape('leaf')
leaf.color('green')
leaf.penup()
leaf.hideturtle()
leaf.speed(0)

game_started = False
text_turtle = t.Turtle()
text_turtle.write('Press [space] to start!', align='center', font=('Arial', 16, 'bold'))
text_turtle.ht()

score_turtle = t.Turtle()
score_turtle.hideturtle()


def outside_window():
    pass

def game_over():
    pass

def display_score(current_score):
    pass

def place_leaf():
    pass

def start_game():
    global game_started
    if game_started:
        return
    game_started = True

    score = 0
    text_turtle.clear()

    caterpillar_speed = 2
    caterpillar_length = 3
    caterpillar.shapesize(1, caterpillar_length, 1)
    caterpillar.st()
    display_score(score)
    place_leaf()


    while True:
        caterpillar.forward(caterpillar_speed)
        if caterpillar.distance(leaf) < 20:
            place_leaf()
            caterpillar_length += 1
            caterpillar.shapesize(1, caterpillar_length, 1)
            caterpillar_speed += 1
            score += 1
            display_score(score)
        if outside_window:
            game_over()
            break

t.onkey(start_game, 'space')
t.listen()
t.mainloop()
