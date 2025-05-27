from tkinter import *
import random
import time
displaytext = False
score = 0

class Ball:
    def __init__(self, canvas, paddle, player, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(starts)
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
    def hit_paddle(self, pos, player):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                player.increase()
                return True
        return False
    def draw(self, player):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x = self.x * -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos, player) == True:
            self.y = self.y * -1  
        if pos[1] <= 0 or pos[3] >= self.canvas_height:
            self.y = self.y * -1

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)  
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        pass

    def turn_left(self, evt):
        ppos = self.canvas.coords(self.id)
        if evt.keysym == 'Left':
            self.canvas.move(self.id, -50, 0)

    def turn_right(self, evt):
        ppos = self.canvas.coords(self.id)
        if evt.keysym == 'Right':
            self.canvas.move(self.id, 50, 0)
class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0
        self.id = self.canvas.create_text(250, 10, text=(f'Score : {str(self.score)}'), font=('Helvetica', 20))

    def increase(self):
        self.score += 1

    def draw(self):
        self.canvas.itemconfig(self.id, text=(f'Score : {str(self.score)}'))

class Game:
    def __init__(self, canvas):
        self.gamestart = False
        self.gameend = False
        self.canvas = canvas
        self.start = canvas.create_text(250, 200, text='Bounce Game!\n'
                                        +'Use the arrow keys to move the paddle.\n'
                                        +'Hit the ball with the paddle to earn a point.\n'
                                        +'The game ends when the ball hits the bottom of the screen.\n'
                                        +'Click the screen to start!', fill='blue', font=('Helvetica', 15), state='normal')
        self.canvas.bind_all('<Button-1>', self.start_game)
    def start_game(self, evt):
        self.gamestart = True
        self.canvas.itemconfig(self.start, state='hidden')

def main(): 
    tk = Tk()
    tk.title('Bounce Game')
    tk.resizable(0, 0) 
    tk.wm_attributes('-topmost', 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()
    displaytext = False

    player = Player(canvas)
    paddle = Paddle(canvas, 'magenta')
    ball = Ball(canvas, paddle, player, 'green')
    bouncegame = Game(canvas)

    while True:
        if ball.hit_bottom == False:
            if bouncegame.gamestart == True:
                ball.draw(player)
                paddle.draw()
            player.draw()
        else:
            if displaytext == False:
                canvas.create_text(250, 200, text='Game over!', font=('Helvetica', 40), fill='red')
                displaytext = True
                break
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
    tk.update()
    time.sleep(3)
    tk.destroy()
    return player.score

if __name__ == '__main__':
    main()