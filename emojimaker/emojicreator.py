from tkinter import Tk, StringVar, PhotoImage
from tkinter.ttk import Label, Button, Radiobutton, Frame
from PIL import Image, ImageTk
from pyperclip import copy

def create_emoji():
    emoji.set(f'{person.get()}{skin_tone.get()}{hair.get()}')

def copy_emoji():
    copy(emoji.get())

root = Tk()
root.title('Emoji Creator')
f = Frame(root)
f.grid(sticky='nwes')
Label(f, text='Select person type:').grid(column=0, row=0)
person_frame = Frame(f)
person_frame.grid(column=0, row=1)
person = StringVar(value='🧑')
for i, j, k, l in zip(('person', 'personfemale', 'personmale'), ('Normal', 'Female', 'Male'), ('🧑', '👩', '👨'), tuple(range(3))):
    img = ImageTk.PhotoImage(Image.open(f'{i}.png').resize((75, 75), Image.Resampling.LANCZOS))
    r = Radiobutton(person_frame, text=j, image=img, compound='top', variable=person, value=k, command=create_emoji)
    r.grid(column=l, row=0)
    r.image = img
Label(f, text='Select skin tone:').grid(column=0, row=2)
skin_tone_frame = Frame(f)
skin_tone_frame.grid(column=0, row=3)
skin_tone = StringVar(value='')    
for i, j, k, l in zip(('none', 'lightskin', 'mediumlightskin', 'mediumskin', 'mediumdarkskin', 'darkskin'), ('None specified', 'Light', 'Medium light', 'Medium', 'Medium dark', 'Dark'),
('', '🏻', '🏼', '🏽', '🏾', '🏿'), tuple(range(6))):
    img = ImageTk.PhotoImage(Image.open(f'{i}.png').resize((75, 75), Image.Resampling.LANCZOS))
    r = Radiobutton(skin_tone_frame, text=j, image=img, compound='top', variable=skin_tone, value=k, command=create_emoji)
    r.grid(column=l, row=0)
    r.image = img
Label(f, text='Select hair style:').grid(column=0, row=4)
hair_frame = Frame(f)
hair_frame.grid(column=0, row=5)
hair = StringVar(value='')
for i, j, k, l in zip(('none', 'baldhair', 'redhair', 'whitehair', 'curlyhair'), ('None specified', 'Bald', 'Red', 'White', 'Curly'),
('', '‍🦲', '‍🦰', '‍🦳', '‍🦱'), tuple(range(5))):
    img = ImageTk.PhotoImage(Image.open(f'{i}.png').resize((75, 75), Image.Resampling.LANCZOS))
    r = Radiobutton(hair_frame, text=j, image=img, compound='top', variable=hair, value=k, command=create_emoji)
    r.grid(column=l, row=0)
    r.image = img
emoji = StringVar()
Label(f, text='Your emoji:').grid(column=0, row=6)
Label(f, textvariable=emoji, font=('Arial', 75)).grid(column=0, row=7)
Button(f, text='Copy emoji', command=copy_emoji).grid(column=0, row=8)
create_emoji()
root.mainloop()