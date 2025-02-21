from turtle import *
leaf_shape = ((0,0), (14,2), (18,6), (20, 20), (6, 18), (2, 14))

t = Turtle()
register_shape('leaf', leaf_shape)
t.shape('leaf')
t.color('green')
t.speed(0)

#Draw a square
for i in range(4):
    t.forward(200)
    t.left(90)
    
input()