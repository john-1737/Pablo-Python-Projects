from turtle import Turtle, numinput, Screen

num = numinput('Enter number', 'Enter number to calculate factors')
def draw_factors(t, num):
    lowest_factor = 0
    num = int(num)
    for i in range(2, num):
        if num%i == 0:
            lowest_factor = i
            break #The number is composite.
    if lowest_factor == 0:
        t.forward(100)
        t.write(num, move=True, font=('Arial', 12, 'normal'))
        return #The number is prime, so no more factors can be calculated.
    t.forward(100)
    t.write(str(num), move=True, font=('Arial', 12, 'normal'))
    t2 = t.clone()
    t.setheading(0)
    t2.setheading(0)
    t.right(45)
    t2.left(45)
    draw_factors(t, num/lowest_factor)
    t2.forward(100)
    t2.write(lowest_factor, move = True, font=('Arial', 12, 'normal'))

t = Turtle()
t.ht()
t.up()
t.goto(-400, 0)
t.down()
draw_factors(t, num)
s = Screen()
s.mainloop()