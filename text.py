from tkinter import *
tk = Tk()
canvas = Canvas(tk, width=1500, height=1500)
canvas.pack()
canvas.create_text(100, 100, text='helo world')
tk.mainloop()