from tkinter import *
import random
import time
tk = Tk()
canvas = Canvas(tk, width=224, height=275)
canvas.pack()
albums = (PhotoImage(file='/Users/jbellows/Pablo Python Projects/photoimages/taylor_debut.gif'),
          PhotoImage(file='/Users/jbellows/Pablo Python Projects/photoimages/taylor_fearless.gif'),
          PhotoImage(file='/Users/jbellows/Pablo Python Projects/photoimages/taylorspeaknow.gif'),
          PhotoImage(file='/Users/jbellows/Pablo Python Projects/photoimages/taylor_red.gif'))
albumnames = ('Taylor Swift', 'Fearless', 'Speak Now', 'Red')
class image:
    def __init__(self, canvas, albums):
        self.canvas = canvas
        self.id = canvas.create_image(112, 162.5)
        self.albumlist = list(albums)
    def draw(self, imagenumber):
        self.canvas.itemconfig(self.id, image=self.albumlist[imagenumber])
        self.albumlist = list(albums)
        del self.albumlist[imagenumber]
class text:
    def __init__(self, canvas, player):
        self.canvas = canvas
        self.player = player
        self.id = self.canvas.create_text(112, 0, anchor='n', font=('Helvetica', 12), text='Taylor Swift Albums Game!\nClick the albums with the correct key\nwhen they match the album on screen.\nClick A to start!')
        self.setup()
    def setup(self):
        while self.player.running != 1:
            continue
        self.canvas.itemconfig(self.id, text='Select difficulty:\nQ = Easy A = Medium Z = Hard\nClick X to exit.')
        print('True')
    def draw(self):
        if self.player.running == 2:
            if self.player.difficulty == 1:
                pass
    def checkreset(self):
        if self.player.running == 0:
            self.canvas.itemconfig(self.id, text='Taylor Swift Albums Game!\nClick the albums with the correct key\nwhen they match the album on screen.\nClick A to start!')
        self.setup()    
class player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.running = 0
        #self.image.imagenumber = image.imagenumber
        self.canvas.bind_all('<KeyPress-q>', self.imageset)
        self.canvas.bind_all('<KeyPress-a>', self.imageset)
        self.canvas.bind_all('<KeyPress-z>', self.imageset)
        self.canvas.bind_all('<KeyPress-x>', self.close)
        self.difficulty = 0

    def imageset(self, evt):
        if self.running == 2:
            if evt.keysym == 'q':
                clicknumber = 1
            elif evt.keysym == 'a':
                clicknumber = 2
            elif evt.keysym == 'z':
                clicknumber = 3
            self.checkimage(clicknumber)
        elif self.running == 0:
            if evt.keysym == 'a':
                self.running = 1
        elif self.running == 1:
            if evt.keysym == 'q':
                self.difficulty = 1
            elif evt.keysym == 'a':
                self.difficulty = 2
            elif evt.keysym == 'z':
                self.difficulty = 3

    def close(self, evt):
        self.running = 0
    #def checkimage(self, clicked):
        #if self.text.clicklist[clicked] == 

tk.update()
play = player(canvas)
t = text(canvas, play)
i = image(canvas, albums)
tk.update()
imagenumber = None
while True:
    #imagenumber = random.randrange(len(i.albumlist) + 1)
    #i.draw(imagenumber)
    t.draw()
    tk.update()
    time.sleep(0.01)