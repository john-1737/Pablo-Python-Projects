#Set
from tkinter import Tk, Canvas, Label, Button, simpledialog, Frame, IntVar, messagebox, Menu, Toplevel
from random import shuffle
from time import sleep
from sys import exit

cards = []
for i in (1, 2, 3): #number
    for j in ('s', 't', 'c'): #squares, triangles, circles (shape)
        for k in ('f', 'd', 'e'): #full, dim, empty (shading)
            for l in ('r', 'g', 'b'): #red, green, blue (color)
                cards.append((i, l, k, j))
shuffle(cards)

def take_cards(cards_num):
    taken_cards = []
    for i in range(cards_num):
        taken_cards.append(cards.pop(0))
    return taken_cards

class card:
    def __init__(self, x, y, root):
        self.root = root
        self.x = x
        self.y = y
        self.canvas = Canvas(self.root, width=100, height=150, bg='white')
        self.canvas.grid(column=self.x, row=self.y, padx=10, pady=10)
        self.canvas.bind('<Button-1>', self.register)
    def showcard(self, card):
        self.canvas.delete('shape')
        poss = {1: (55,), 3:(5, 55, 105), 2:(30, 80)}[card[0]]
        shading = {'r': {'f': {'outline':'white', 'fill': '#ff0000'}, 'd': {'outline':'white', 'fill': '#ff8080'},  'e': {'fill':'white', 'outline': '#ff0000'}}, 'g': {'f': {'outline':'white', 'fill': '#00ff00'}, 'd': {'outline':'white', 'fill': '#80ff80'},  'e': {'fill':'white', 'outline': '#00ff00'}}, 'b': {'f': {'outline':'white', 'fill': '#0000ff'}, 'd': {'outline':'white', 'fill': '#8080ff'},  'e': {'fill':'white', 'outline': '#0000ff'}}}[card[1]][card[2]]
        for i in range(card[0]):
            if card[3] == 's':
                self.canvas.create_rectangle(30, poss[i], 70, poss[i]+40, **shading, tags='shape')
            elif card[3] == 't':
                self.canvas.create_polygon((50, poss[i], 30, poss[i]+40, 70, poss[i]+40), **shading, tags='shape')
            elif card[3] == 'c':
                self.canvas.create_oval(30, poss[i], 70, poss[i]+40, **shading, tags='shape')
        self.card = card
    def clear(self):
        self.canvas.delete('shape')
    def register(self, evt):
        global selcards, showcards
        if len(selcards) == 3:
            return
        self.canvas['bg'] = 'lightgray'
        sleep(0.1)
        self.canvas['bg'] = 'white'
        selcards.append((self.x, self.y))
        if len(selcards) == 3:
            if is_set(showcards[selcards[0]].card, showcards[selcards[1]].card, showcards[selcards[2]].card):
                for i in selcards:
                    showcards[i].showcard(take_cards(1)[0])
                if len(cards) < 3:
                    for i in showcards:
                        showcards[i].clear()
                    self.canvas.unbind_all('<Button-1>')
                    messagebox.showinfo(message='You\'ve run out of cards!')
                score_vars[current_player].set(score_vars[current_player].get() + 1)
            else:
                score_vars[current_player].set(score_vars[current_player].get() - 1)

def is_set(card1, card2, card3):
    return (card1[0]==card2[0]==card3[0] or card1[0]!=card2[0]!=card3[0]!=card1[0])\
    and (card1[1]==card2[1]==card3[1] or card1[1]!=card2[1]!=card3[1]!=card1[1])\
    and (card1[2]==card2[2]==card3[2] or card1[2]!=card2[2]!=card3[2]!=card1[2])\
    and (card1[3]==card2[3]==card3[3] or card1[3]!=card2[3]!=card3[3]!=card1[3])

def change_current_player(player):
    global current_player, selcards
    current_player = player
    selcards = []

def get_new_cards():
    for i in range(4):
        cards.append(showcards[i, 2].card)
    newcards = take_cards(4)
    for i in range(4):
        showcards[i, 2].showcard(newcards[i])

players = simpledialog.askinteger('Players', 'How many are playing?')
if players == None:
    exit()
root = Tk()
showcardvalues = take_cards(12)
showcards = {}
selcards = [1, 1, 1]
root.title('Set')
for i in range(4):
    for j in range(3):
        c = card(i, j, root)
        c.showcard(showcardvalues.pop())
        showcards[i, j] = c
pcs = Frame(root)
pcs.grid(column=0, row=3, columnspan=4)
score_vars = []
for i in range(players):
    Label(pcs, text=f'Player {i+1}').grid(column=i, row=0)
    Label(pcs, text='Score:').grid(column=i, row=1)
    s = IntVar()
    Label(pcs, textvariable=s).grid(column=i, row=2)
    score_vars.append(s)
    Button(pcs, text='Found a set!', command=lambda player=i:change_current_player(player)).grid(column=i, row=3)
Button(root, text='Can\'t find a set? Click to add new cards', command=get_new_cards).grid(column=0, row=4, columnspan=4)
win = Toplevel(root)
Label(win, text='To find a set, each attribute (the number of shapes, the color, the shape, and the shading) must be either all the same or different.\nFor example, this is a set:').grid(column=0, row=0, columnspan=3)
card(0, 1, win).showcard((3, 'r', 'f', 's'))
card(1, 1, win).showcard((3, 'g', 'f', 's'))
card(2, 1, win).showcard((3, 'b', 'f', 's'))
Label(win, text='because the numbers of shapes are all the SAME, the shadings are all the SAME, the shapes are all the SAME, but the colors are all DIFFERENT.\nThis is also a set:').grid(column=0, row=2, columnspan=3)
card(0, 3, win).showcard((1, 'r', 'f', 's'))
card(1, 3, win).showcard((2, 'g', 'd', 't'))
card(2, 3, win).showcard((3, 'b', 'e', 'c'))
Label(win, text='because the numbers of shapes are all DIFFERENT, the shadings are all DIFFERENT, the shapes are all DIFFERENT, and the colors are all DIFFERENT.\nHowever, this is not a set:').grid(column=0, row=4, columnspan=3)
card(0, 5, win).showcard((3, 'r', 'f', 's'))
card(1, 5, win).showcard((3, 'r', 'f', 's'))
card(2, 5, win).showcard((3, 'r', 'f', 't'))
Label(win, text='because the numbers of shapes are all the SAME, the shadings are all the SAME, the colors are all the SAME, but two cards have squares and one has a triangle.').grid(column=0, row=6, columnspan=3)
Button(win, text='Back', command=win.withdraw).grid(column=0, row=7, columnspan=3)
win.withdraw()
menubar = Menu(root)
root['menu'] = menubar
instructions = Menu(menubar)
menubar.add_cascade(menu=instructions, label='Instructions')
instructions.add_command(command=win.deiconify, label='Identifying a set')
instructions.add_command(label='Game Rules', command=lambda: messagebox.showinfo(message='''To play this game, you must find sets (see Identifying Sets) to earn points.
To register a set, press your player's "Found a set!" button and then click on the cards to form your set.
If what you select isn't a set, you lose a point. If it is a set, you earn a point and new cards replace the cards you formed your set with.
If you can't find a set, press the "add new cards" button to move the bottom 4 cards back to the deck and get 4 new cards.
The game ends whem you run out of cards in your deck.
'''))
root.mainloop()