images = []
while True:
    i = input('Any info from this input-line will be restored. ')
    if i == '':
        break
    images.append(i)

from tkinter import Tk, Canvas, PhotoImage
root = Tk()
c = Canvas(root, width=340, height=440)
c.pack()
img = PhotoImage(file='allopen.gif')
c.create_image(0, 0, anchor='nw', image=img)
img2 = PhotoImage(file='exitb.gif')
c.create_image(0, 0, anchor='nw', image=img2)
root.mainloop()