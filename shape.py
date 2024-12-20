import turtle
t = turtle.Turtle()
def shape(size,sides,red,green,blue,filled):
    if filled == True:
        t.begin_fill()
    t.color(float(red),float(green),float(blue))
    for x in range(0,int(sides)):
        t.forward(int(size))
        t.right(360 / int(sides))
    if filled == True:
        t.end_fill()

while True:
    t.reset()
    size = input("Enter the size of your shape.\n")
    sides = input("Enter the number of sides in your shape.\n")
    filled = input("Would you like your shape to have a fill color?\nEnter 'yes' if you want a outline color or anything else if you do not.\n")
    if filled == 'yes':
        print("Enter the amounts of red, green, and blue for the  fill color of your shape.\n1 represents 100% and 0 represents 0%.")
        fill_red = input("Amount of red: ")
        fill_green = input("Amount of green: ")
        fill_blue = input("Amount of blue: ")
    outlined = input("Would you like your shape to have an outline color?\nEnter 'yes' if you want a outline color or anything else if you do not.\n")
    if outlined == 'yes':    
        print("Enter the amounts of red, green, and blue for the outline color of your shape.\n1 represents 100% and 0 represents 0%.")
        outline_red = input("Amount of red: ")
        outline_green = input("Amount of green: ")
        outline_blue = input("Amount of blue: ")
    print("Creating shape...")
    if filled == 'yes':
        shape(size,sides,fill_red,fill_green,fill_blue,True)
    if outlined == 'yes':
        print('Creating outline...')
        shape(size,sides,outline_red,outline_green,outline_blue,False)  
    exit = input("Enter 'exit' to exit. Enter anything else to create another shape.\n")
    if exit == 'exit':
        break