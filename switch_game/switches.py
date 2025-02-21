from tkinter import Tk, Button, Label, PhotoImage

root = Tk()
switch_off = PhotoImage(file='switch_off.gif')
switch_on = PhotoImage(file='switch_on.gif')
light_off = PhotoImage(file='light_off.gif')
light_on = PhotoImage(file='light_on.gif')
light_image = light_off
switch1_image = switch_off
switch2_image = switch_off

def toggle_light():
    light_image = {light_off:light_on, light_on:light_off}[light_image]
    light.config(image=light_image)

def toggle_switch(switch):
    switch_image = {1:switch1_image, 2:switch2_image}[switch]
    switch_button = {1:switch1_image, 2:switch2_image}[switch]    
    light_image = {light_off:light_on, light_on:light_off}[light_image]
    light.config(image=light_image)

light = Label(root, image=light_image)
light.grid(column=1, row=0)
switch1 = Button(root, image=switch1_image).grid(column=0, row=1)
switch2 = Button(root, image=switch2_image).grid(column=2, row=1)
root.mainloop()