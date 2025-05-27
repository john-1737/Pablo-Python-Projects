from tkinter import Tk, Button, Label, PhotoImage, FALSE, Toplevel, Menu, messagebox

root = Tk()
switch_off = PhotoImage(file='switch_off.gif')
switch_on = PhotoImage(file='switch_on.gif')
light_off = PhotoImage(file='light_off.gif')
light_on = PhotoImage(file='light_on.gif')
light_image = light_off
switch1_image = switch_off
switch2_image = switch_off
q, a = 'question', 'answer'

puzzles = {
1:{q:'Flip both switches to turn the light off.', a:'You must start with both switches at either off or on.'},
2:{q:'Flip both switches to turn the light on.', a:'You must start with one switch on and the other off.'},
3:{q:'Every time you flip both switches, the light will remain what it was before. Can you figure out why?', a:'When you flip one switch, the light toggles, and when you flip the other, it toggles back.'},
4:{q:'Can you find a way to make the light flash using both switches?', a:'ANY two-key combination will work for this one, since each key toggles the light, but the easiest one is left, right, left, right, etc.'}
}

def toggle_light():
    global light_image
    light_image = {light_off:light_on, light_on:light_off}[light_image]
    light.config(image=light_image)

def toggle_switch(switch):
    global switch1_image, switch2_image
    if switch == 1:
        switch1_image = {switch_off:switch_on, switch_on:switch_off}[switch1_image]
        switch1.configure(image=switch1_image)
        switch1.image = switch1_image
    else:
        switch2_image = {switch_off:switch_on, switch_on:switch_off}[switch2_image]
        switch2.configure(image=switch2_image)
        switch2.image = switch2_image
    toggle_light()

root.title('Switch game')
root.option_add('*tearOff', FALSE)
win = Toplevel(root)
menubar= Menu(win)
win['menu'] = menubar
about_menu = Menu(menubar)
puzzles_menu = Menu(menubar)
menubar.add_cascade(menu=about_menu, label='About')
menubar.add_cascade(menu=puzzles_menu, label='Puzzles')
about_menu.add_command(label='Instructions', command=lambda:messagebox.showinfo(message='''This switch design is found in some houses.
Whenever the switch is flipped, the switch toggles and the light toggles. The other switch does not toggle.
It is not an OR gate, as both switches can be turned on and the light can be turned off.
Each switch can turn the light off if it is on, or turn the light on if it is off.
When a switch is turned on, the word "on" appears on the switch. When it is turned off, the word "off" appears.
When the light is turned on, it is yellow. When it is turned off, it is gray.'''))
about_menu.add_command(label='Controls', command=lambda:messagebox.showinfo(message='''You can toggle the left switch by clicking on it or with the F key.
You can toggle the right switch by clicking on it or with the J key.
The light toggles based on the switches (see Instructions)'''))
puzzle_menu = Menu(puzzles_menu)
puzzle_answer_menu = Menu(puzzles_menu)
puzzles_menu.add_cascade(menu=puzzle_menu, label='Puzzles')
puzzles_menu.add_cascade(menu=puzzle_answer_menu, label='Puzzle Answers')
for i in range(1, 5):
    puzzle_menu.add_command(label=f'Puzzle {i}', command=lambda:messagebox.showinfo(message=puzzles[i][q]))
    puzzle_answer_menu.add_command(label=f'Puzzle {i} Answer', command=lambda:messagebox.showinfo(message=puzzles[i][a]))    

light = Label(root, image=light_image)
light.grid(column=1, row=0)
switch1 = Button(root, image=switch1_image, command=lambda: toggle_switch(1))
switch1.grid(column=0, row=1)
switch2 = Button(root, image=switch2_image, command=lambda: toggle_switch(2))
switch2.grid(column=2, row=1)
root.bind('<f>', lambda e: toggle_switch(1))
root.bind('<j>', lambda e: toggle_switch(2))
win.withdraw()
root.mainloop()