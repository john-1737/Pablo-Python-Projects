from tkinter import Tk, Canvas, Button, Label, Frame, StringVar, IntVar
from random import shuffle, choice
from PIL import Image, ImageTk

SC = 7


card_poss = {'A': ((50, 75),), '2': ((50, 37.5), (50, 112.5),), '3': ((50, 25),(50, 75),(50, 125)), '4': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5)), '5': ((50, 75),(25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5)),
'6': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75)), '7': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75), (50, 75)), '8': ((25, 37.5), (50, 37.5), (25, 112.5), (50, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75)),
 '9': ((25, 18.75), (25, 93.75), (25, 131.25), (75, 93.75),(75, 18.75), (75, 131.25), (25, 56.25), (75, 56.25), (50, 75)), '10': ((25, 18.75), (25, 93.75), (25, 131.25), (75, 93.75),(75, 18.75), (75, 131.25), (25, 56.25), (75, 56.25), (50, 37.5), (50, 112.5))}
class card():
    def __init__(self, root, card, suit, xpos, ypos):
        self.root = root
        self.canvas = Canvas(root, width=100, height=150, bg='white')
        self.canvas.grid(column=xpos, row=ypos)
        self.canvas.bind('<Button-1>', self.clicked)
        self.card = card
        self.suit = suit
        self.draw()
    def grid(self, xpos, ypos):
        self.canvas.grid(column=xpos, row=ypos)
    def ungrid(self):
        self.canvas.grid_forget()
    def draw(self):
        if self.card in ('J', 'Q', 'K', 'joker'):
            for i in ((25,75), (75,75)):
                self.canvas.create_image(i[0], i[1], image=self.suit)
            self.canvas.create_image(50, 75, image={'K': king, 'Q': queen, 'J':jack, 'joker':joker}[self.card])
        else:
            for i in card_poss[self.card]:
                self.canvas.create_image(i[0], i[1], image=self.suit)
        self.canvas.create_text(2, 2, text=self.card, anchor='nw', font=('Arial', 15))
        self.canvas.create_text(98, 148, text=self.card, anchor='se', font=('Arial', 15))
    def clicked(self, evt):
        global selcard
        if turn_var.get() == 'Turn: player' and selcard == None:
            selcard = (self.card, self.suit)
            if not selcard[0] in ('AJQK'):
                question_var.set(f'Player\'s question: Do you have a {selcard[0]}?')
            else:
                question_var.set('Player\'s question: Do you have a ' +{'J':'jack', 'A':'ace', 'Q':'queen', 'K':'king'}[selcard[0]]+'?')            
            answer = 'Computer\'s answer: No, go fish!'
            for i in aicardvalues:
                if i[0] == selcard[0]:
                    answer = 'Computer\'s answer: Yes!'
            answer_var.set(answer)
            response_var.set({'Computer\'s answer: No, go fish!': 'Fish', 'Computer\'s answer: Yes!': 'Get card'}[answer])

def ai_move():
    global selcard
    if turn_var.get() == 'Turn: computer':
        selcard = choice(aicardvalues)
        if not selcard[0] in ('AJQK'):
            question_var.set(f'Computer\'s question: Do you have a {selcard[0]}?')
        else:
            question_var.set('Computer\'s question: Do you have a ' +{'J':'jack', 'A':'ace', 'Q':'queen', 'K':'king'}[selcard[0]]+'?')            
        answer = 'Player\'s answer: No, go fish!'
        for i in playercardvalues:
            if i[0] == selcard[0]:
                answer = 'Player\'s answer: Yes!'
        answer_var.set(answer)
        response_var.set('Respond')

def game_over():
    answer_var.set('')
    response_var.set('')
    card_frame.unbind_all('<Button-1>') #Disable all card presses.
    turn_var.set('Game over!')
    if player_score > computer_score:
        question_var.set('Player wins!')
    elif computer_score < player_score:
        question_var.set('Computer wins!')
    else:
        question_var.set('It\'s a tie!')

def respond_control_button():
    global player_score, computer_score
    global selcard
    av = answer_var.get()
    if av == '':
        return
    elif av == 'Player\'s answer: No, go fish!':
        turn_var.set('Turn: player')
        aicardvalues.append(cards.pop(0))
        if aicardvalues[-1][0] == selcard[0]:
            aicardvalues.pop()
            aicardvalues.remove(selcard)
            computer_score += 1
        selcard = None
        question_var.set('(Click a card to ask computer)')
        answer_var.set('')
        response_var.set('')
    elif av == 'Player\'s answer: Yes!':
        turn_var.set('Turn: player')
        for i in playercardvalues:
            if i[0] == selcard[0]:
                playercards[playercardvalues.index(i)].ungrid()
                playercards.pop(playercardvalues.index(i))
                playercardvalues.remove(i)
        aicardvalues.remove(selcard)
        selcard = None
        computer_score += 1
        question_var.set('(Click a card to ask computer)')
        answer_var.set('')
        response_var.set('')
    elif av == 'Computer\'s answer: Yes!':
        turn_var.set('Turn: computer')
        for i in aicardvalues:
            if i[0] == selcard[0]:
                aicardvalues.remove(i)
        playercards[playercardvalues.index(selcard)].ungrid()
        playercards.pop(playercardvalues.index(selcard))
        playercardvalues.remove(selcard)
        player_score += 1
        ai_move()
    elif av == 'Computer\'s answer: No, go fish!':
        turn_var.set('Turn: computer')
        c = cards.pop(0)
        playercardvalues.append(c)
        playercards.append(card(card_frame, c[0], c[1], (len(playercardvalues)-1)//3, (len(playercardvalues)-1)%3))
        if playercardvalues[-1][0] == selcard[0]:
            playercardvalues.pop()
            playercards[-1].ungrid()
            playercards.pop()
            playercards[playercardvalues.index(selcard)].ungrid()
            playercards.pop(playercardvalues.index(selcard))
            playercardvalues.remove(selcard)
            player_score += 1
        ai_move()
    player_score_var.set(player_score)
    computer_score_var.set(computer_score)
    for i, j in enumerate(playercards):
        j.ungrid()
        j.grid(i//3, i%3)
    if cards == []:
        game_over()

root = Tk()
root.title('Go Fish')
club = ImageTk.PhotoImage(Image.open('club.png').resize((26, 26)))
diamond = ImageTk.PhotoImage(Image.open('diamond.png').resize((26, 26)))
heart = ImageTk.PhotoImage(Image.open('heart.png').resize((26, 26)))
jack = ImageTk.PhotoImage(Image.open('jack.png').resize((26, 26)))
king = ImageTk.PhotoImage(Image.open('king.png').resize((26, 26)))
queen = ImageTk.PhotoImage(Image.open('queen.png').resize((26, 26)))
spade = ImageTk.PhotoImage(Image.open('spade.png').resize((26, 26)))
red = ImageTk.PhotoImage(Image.open('red.png').resize((26, 26)))
black = ImageTk.PhotoImage(Image.open('black.png').resize((26, 26)))
joker = ImageTk.PhotoImage(Image.open('joker.png').resize((26, 26)))
cards = []
for i in ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'):
    for j in (club, diamond, heart, spade):
        cards.append((i, j))
cards.append(('joker', red))
cards.append(('joker', black))
shuffle(cards)
while True:
    if len(set(cards[0:SC])) != len(cards[0:SC]) or len(set(cards[SC-1:SC*2])) != len(cards[SC-1:SC*2]):
        shuffle(cards)
    else:
        break
player_score = 0
player_score_var = IntVar()
computer_score = 0
computer_score_var = IntVar()
playercards = []
playercardvalues = []
aicardvalues = []
selcard = None
card_frame = Frame(root)
card_frame.pack()
for i in range(SC):
    ct = cards.pop(0)
    c = card(card_frame, ct[0], ct[1], i//3, i%3)
    playercards.append(c)
    playercardvalues.append(ct)
for i in range(SC):
    aicardvalues.append(cards.pop(0))


turn_var = StringVar(value='Turn: player')
Label(root, textvariable=turn_var).pack()
#question_turn_var = StringVar(value='Player\'s question:')
#Label(root, textvariable=question_turn_var).pack()
question_var = StringVar(value='(Click a card to ask computer)')
Label(root, textvariable=question_var).pack()
answer_var = StringVar()
Label(root, textvariable=answer_var).pack()
response_var = StringVar()
Button(root, textvariable=response_var, command=respond_control_button).pack()
scores = Frame(root)
scores.pack()
Label(scores, text='Player Score:').grid(column=0, row=0)
Label(scores, text='Computer Score:').grid(column=1, row=0)
Label(scores, textvariable=player_score_var).grid(column=0, row=1)
Label(scores, textvariable=computer_score_var).grid(column=1, row=1)

root.mainloop()
