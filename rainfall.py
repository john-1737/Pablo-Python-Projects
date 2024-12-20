import tkinter as tk
import random as ra
import time as t

class Raindrop:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x_pos = ra.randint(0, 400)
        self.y_pos = 0
        self.size = ra.randint(2, 5)
        self.id = self.canvas.create_rectangle(self.x_pos, self.y_pos, self.x_pos + self.size, self.y_pos + 20 + self.size, fill='blue')
        self.canvas.itemconfig(self.id, tags=str(self.id))
        self.fall_speed = 0
        self.gravity = -2

    def move(self):
        self.fall_speed += self.gravity
        self.y_pos -= self.fall_speed
        self.canvas.move(self.id, 0, -self.fall_speed)
        if self.y_pos == 500:
            canvas.delete(str(self.id))

root = tk.Tk()
root.title('Rainfall')
raindrop_frequency_var = tk.StringVar()
canvas = tk.Canvas(root, width=400, height=500)
canvas.grid(column=0, row=0, columnspan=2)
tk.Scale(root, orient='horizontal', length=200, from_=1.0, to=10.0, variable=raindrop_frequency_var).grid(column=0, row=2)
speed_var = tk.StringVar()
tk.Scale(root, orient='horizontal', length=200, from_=1.0, to=10.0, variable=speed_var).grid(column=1, row=2)
tk.Label(root, text='Set raindrop frequency', font=('Arial', 19)).grid(column=0, row=1)
tk.Label(root, text='Set raindrop speed', font=('Arial', 19)).grid(column=1, row=1)
raindrops_label = tk.Label(root, text='Raindrops = 0', font=('Arial', 25))
raindrops_label.grid(column=0, row=3, columnspan=2)
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