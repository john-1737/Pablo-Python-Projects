from tkinter import *
t = 0
tk = Tk()
canvas = Canvas(tk, width=400, height=400)
canvas.pack()
pages = ['These are the instructions for how to operate bouncegame.py.'
         +'Click the right arrow key to start.',
        'To use the instructions, click the right arrow key to move to the next page.'
        +'Click the left arrow key to move back.'
        +'There are 5 pages. The page returns to the first page after the last page.'
        'How to use the paddle:'
        +'Press the left arrow key to move the paddle to the left.'
        +'The paddle only stops at the edges and the start of the game.', 
        'How to operate the ball:'
        +'The ball bounces off the walls and the paddle.'
        +'Hit the ball with the paddle to win a point.', 
        'The end of the game:'
        +'The game ends when the ball touches the bottom of the screen.']

textbox = canvas.create_text(200, 200, text = pages[t], width = 250, fill = 'red')

def switchscreen(event):
    global t
    if event.keysym == 'Right':
        t += 1
        canvas.itemconfig(textbox, text = pages[t%len(pages)])
    else:
        t -= 1
        canvas.itemconfig(textbox, text = pages[t%len(pages)])


canvas.bind_all('<KeyPress-Left>', switchscreen)
canvas.bind_all('<KeyPress-Right>', switchscreen)


tk.mainloop()
