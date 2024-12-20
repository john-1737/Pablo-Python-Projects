import tkinter as tk
import random as ra
import time as t
import math as m

class Raindrop:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_side = ra.choice(('n', 's', 'e', 'w'))
        if self.start_side in 'ns':
            self.x_pos = ra.randint(0, 500)
            if self.start_side == 'n':
                self.y_pos = 0
            else:
                self.y_pos = 500
        else:
            self.y_pos = ra.randint(0, 500)
            if self.start_side == 'w':
                self.x_pos = 0
            else:
                self.x_pos = 500
        self.size = ra.randint(2, 5)
        self.id = self.canvas.create_oval(self.x_pos, self.y_pos, self.x_pos + self.size, self.y_pos + self.size, fill='blue')
        self.canvas.itemconfig(self.id, tags=str(self.id))
        self.fall_speed = 0
        self.gravity = -2
        self.times_moved = 0

    def move(self):
        global black_hole_size, black_hole
        self.fall_speed += self.gravity
        self.canvas.move(self.id, (250-self.x_pos)/125, (250-self.y_pos)/125)
        self.times_moved += 1
        if self.times_moved == 125:
            self.canvas.delete(str(self.id))
            black_hole_size += 1
            canvas.delete('hole')
            black_hole = self.canvas.create_oval(240 - black_hole_size, 240 - black_hole_size, 260 + black_hole_size, 260 + black_hole_size, fill='black', tags='hole')
        
root = tk.Tk()
root.title('Rainfall')
raindrop_frequency_var = tk.StringVar()
canvas = tk.Canvas(root, width=500, height=500)
canvas.grid(column=0, row=0, columnspan=2)
tk.Scale(root, orient='horizontal', length=200, from_=1.0, to=10.0, variable=raindrop_frequency_var).grid(column=0, row=2)
speed_var = tk.StringVar()
tk.Scale(root, orient='horizontal', length=200, from_=1.0, to=10.0, variable=speed_var).grid(column=1, row=2)
tk.Label(root, text='Set raindrop frequency', font=('Arial', 19)).grid(column=0, row=1)
tk.Label(root, text='Set raindrop speed', font=('Arial', 19)).grid(column=1, row=1)
raindrops_label = tk.Label(root, text='Raindrops = 0', font=('Arial', 25))
raindrops_label.grid(column=0, row=3, columnspan=2)
black_hole = canvas.create_oval(240, 240, 260, 260, fill='black', tags='hole')
black_hole_size = 0
raindrops = []
while True:
    raindrop_frequency = int(float(raindrop_frequency_var.get()))
    if ra.randint(1, raindrop_frequency) == 1:
        raindrops.append(Raindrop(canvas))
    for r in raindrops:
        r.move()
    raindrops_label['text'] = f'Raindrops = {len(raindrops)}'
    root.update()
    t.sleep((1/float(speed_var.get())) * 0.1)