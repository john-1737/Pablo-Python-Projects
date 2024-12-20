from tkinter import *
import time
tk = Tk()
canvas = Canvas(tk, width=720, height=720)
canvas.pack()
midnights = PhotoImage(file='/Users/jbellows/Pablo Python Projects/photoimages/midnights.gif')
for a in range(0, 10):
    for b in range(0,10):
        canvas.create_image((a*72)+36, (b*72)+36, image=midnights)
tk.mainloop()