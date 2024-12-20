import turtle
t = turtle.Turtle()
def createoctagon(size,red,green,blue,filled):
    t.color(float(red),float(green),float(blue))
    if filled == True:
        t.begin_fill()
    for x in range(0,8):
        t.forward(float(size))
        t.right(45)
    if filled == True:
        t.end_fill()

createoctagon(100,1,0,0,True)
createoctagon(100,0,0,0,False)
input()