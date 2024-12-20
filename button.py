from tkinter import *
tk = Tk()
def helloworld():
    canvas.create_text(100, 100, text='helo world')
canvas = Canvas(tk, width=1500, height=1500)
canvas.place(x=50, y=50)
btn = Button(tk, text='click me', command=helloworld)
btn.pack()
tk.mainloop()