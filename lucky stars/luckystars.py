"""Lucky Stars, by Al Sweigart al@inventwithpython.com
A "press your luck" game where you roll dice to gather as many stars
as possible. You can roll as many times as you want, but if you roll
three skulls you lose all your stars.

Inspired by the Zombie Dice game from Steve Jackson Games.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, multiplayer"""

import random
from tkinter import Tk, PhotoImage, Toplevel, messagebox, StringVar
from tkinter import Frame as Tkframe
from tkinter.ttk import Label, Button, Frame, Treeview, Entry

# Set up the constants:
GOLD = "#e5d800"
SILVER = "#777777"
BRONZE = '#d2b48c'

root = Tk()
STAR_FACE = PhotoImage(file='star.png')
SKULL_FACE = PhotoImage(file='skull.png')
QUESTION_FACE = PhotoImage(file='question.png')
root.withdraw()
FACE_WIDTH = 13
FACE_HEIGHT = 7

'''print("""Lucky Stars, by Al Sweigart al@inventwithpython.com

A "press your luck" game where you roll dice with Stars, Skulls, and
Question Marks.

On your turn, you pull three random dice from the dice cup and roll
them. You can roll Stars, Skulls, and Question Marks. You can end your
turn and get one point per Star. If you choose to roll again, you keep
the Question Marks and pull new dice to replace the Stars and Skulls.
If you collect three Skulls, you lose all your Stars and end your turn.

When a player gets 13 points, everyone else gets one more turn before
the game ends. Whoever has the most points wins.

There are 6 Gold dice, 4 Silver dice, and 3 Bronze dice in the cup.
Gold dice have more Stars, Bronze dice have more Skulls, and Silver is
even.
""")'''

def get_names():
    global namewin, numPlayers, playerNames, playerScores, name_var, player_var, nentry, finish_button
    numPlayers = 1
    playerNames = []  # List of strings of player names.
    playerScores = {}  # Keys are player names, values are integer scores.
    namewin = Toplevel(root)
    namewin.title('Lucky Stars')
    name_var = StringVar()
    player_var = StringVar(value='What is player #1\'s name?')
    f = Frame(namewin)
    f.grid(sticky='nwes')
    nentry = Entry(f, textvariable=name_var)
    nentry.grid(column=0, row=1, columnspan=2)
    Label(f, textvariable=player_var).grid(column=0, row=0, columnspan=2)
    Label(f, text='When all the players have entered their names,\npress Finish. Otherwise, press Next.').grid(column=0, row=2, columnspan=2)
    finish_button = Button(f, text='Finish', default='active', command=exit_name, state='disabled')
    finish_button.grid(column=1, row=3)
    Button(f, text='Next', command=lambda: next_name(False)).grid(column=0, row=3)
    namewin.mainloop()

def next_name(reset=False):
    global numPlayers, playerNames, playerScores
    numPlayers += 1
    nentry.focus()
    if (name_var.get() == '' or name_var.get() in playerNames) and (not reset):
        messagebox.showinfo(message='Please enter a name that has not been used.')
        numPlayers -= 2
        next_name(True)
        return
    if numPlayers >= 2:
        finish_button.config(state='normal')
    playerNames.append(name_var.get())
    playerScores[name_var.get()] = 0
    player_var.set('What is player #' + str(numPlayers) + '\'s name?')
    name_var.set('')

def exit_name():
    global playerNames, numPlayers
    if (name_var.get() == '' or name_var.get() in playerNames):
        messagebox.showinfo(message='Please enter a name that has not been used.')
        numPlayers -= 1
        next_name(True)
        return
    playerNames.append(name_var.get())
    playerScores[name_var.get()] = 0
    namewin.destroy()
    root.deiconify()
    playerNames = [i for i in playerNames if not i==""]
    game(playerScores, playerNames, numPlayers)

def restart_game():
    global root, STAR_FACE, SKULL_FACE, QUESTION_FACE
    root.destroy()
    root = Tk()
    root.withdraw()
    STAR_FACE = PhotoImage(file='star.png')
    SKULL_FACE = PhotoImage(file='skull.png')
    QUESTION_FACE = PhotoImage(file='question.png')
    get_names()

class game:
    def __init__(self, playerScores, playerNames, numPlayers):
        self.turn = 0
        self.stars = 0
        self.skulls = 0
        self.playerScores = playerScores
        self.playerNames = playerNames
        self.numPlayers = numPlayers
        self.endGameWith = None
        self.cup = ([GOLD] * 6) + ([SILVER] * 4) + ([BRONZE] * 3)
        self.hand = []
        root.title('Lucky Stars')
        main = Frame(root)
        main.grid(sticky='nsew')
        self.turn_var = StringVar()
        self.result_var = StringVar()
        self.collection_var = StringVar()
        self.rollResults = [None, None, None]
        Label(main, text='Scores:').grid(column=0, row=0, columnspan=4)
        self.scores = Treeview(main, columns=('Score',))
        self.scores.grid(column=0, row=1, columnspan=4)
        self.dief1 = Tkframe(main, width=100, height=100, highlightthickness=10)
        self.dief1.grid(column=0, row=3, padx=5)
        self.dief2 = Tkframe(main, width=100, height=100, highlightthickness=10)
        self.dief2.grid(column=1, row=3, columnspan=2, padx=5)
        self.dief3 = Tkframe(main, width=100, height=100, highlightthickness=10)
        self.dief3.grid(column=3, row=3, padx=5)
        self.die1 = Label(self.dief1)
        self.die1.grid()
        self.die2 = Label(self.dief2)
        self.die2.grid()
        self.die3 = Label(self.dief3)
        self.die3.grid()
        self.next_button = Button(main, text='Next', command=self.play_turn)
        self.next_button.grid(column=0, row=6, columnspan=4)
        self.next_button.grid_remove()
        self.continue_button = Button(main, text='Continue', command=self.end_turn)
        self.continue_button.grid(column=0, row=6, columnspan=4)
        self.continue_button.grid_remove()
        self.restart_button = Button(main, text='Restart', command=restart_game)
        self.restart_button.grid(column=0, row=6, columnspan=4)
        self.restart_button.grid_remove()
        Label(main, textvariable=self.collection_var).grid(column=0, row=4, columnspan=4)
        Label(main, textvariable=self.result_var).grid(column=0, row=5, columnspan=4)
        Label(main, textvariable=self.turn_var).grid(column=0, row=2, columnspan=4)
        self.roll_button = Button(main, text='Roll again', command=self.play_turn)
        self.roll_button.grid(column=0, row=6, columnspan=2)
        self.end_button = Button(main, text='End turn', command=self.end_turn)
        self.end_button.grid(column=2, row=6, columnspan=2)
        self.play_turn()

    def play_turn(self): # Main game loop.
        # Display everyone's score:
        self.continue_button.grid_remove()
        self.next_button.grid_remove()
        self.end_button.grid()
        self.roll_button.grid()
        for i in self.scores.get_children():
            self.scores.delete(i)
        for i, name in enumerate(playerNames):
            self.scores.insert('', 'end', text=name, values=(str(playerScores[name]),))
        self.result_var.set('')
        self.die1.grid()
        self.die2.grid()
        self.die3.grid()
        self.dief1.config(highlightthickness=10)
        self.dief2.config(highlightthickness=10)
        self.dief3.config(highlightthickness=10)
        if self.endGameWith == None:
            self.turn_var.set('It is ' + playerNames[self.turn] + '\'s turn.')
        else:
            self.turn_var.set('It is ' + playerNames[self.turn] + '\'s turn. The game will end at '+ self.endGameWith + '\'s turn.')
        # Check that there's enough dice left in the cup:
        if (3 - len(self.hand)) > len(self.cup):
            # End this turn because there are not enough dice:
            self.result_var.set('There aren\'t enough dice left in the cup to continue ' + self.playerNames[self.turn] + '\'s turn.')
            self.end_button.grid_remove()
            self.roll_button.grid_remove()
            self.continue_button.grid()
            return

        nextHand = []
        for i in range(3):
            if self.rollResults[i] == QUESTION_FACE:
                nextHand.append(self.hand[i])
            else:
                nextHand.append(self.cup.pop())
        self.hand = nextHand
        # Pull dice from the cup until you have 3 in your hand:



        # Roll the dice:
        self.rollResults = []
        for dice in self.hand:
            roll = random.randint(1, 6)
            if dice == GOLD:
                # Roll a gold die (3 stars, 2 questions, 1 skull):
                if 1 <= roll <= 3:
                    self.rollResults.append(STAR_FACE)
                    self.stars += 1
                elif 4 <= roll <= 5:
                    self.rollResults.append(QUESTION_FACE)
                else:
                    self.rollResults.append(SKULL_FACE)
                    self.skulls += 1
            if dice == SILVER:
                # Roll a silver die (2 stars, 2 questions, 2 skulls):
                if 1 <= roll <= 2:
                    self.rollResults.append(STAR_FACE)
                    self.stars += 1
                elif 3 <= roll <= 4:
                    self.rollResults.append(QUESTION_FACE)
                else:
                    self.rollResults.append(SKULL_FACE)
                    self.skulls += 1
            if dice == BRONZE:
                # Roll a bronze die (1 star, 2 questions, 3 skulls):
                if roll == 1:
                    self.rollResults.append(STAR_FACE)
                    self.stars += 1
                elif 2 <= roll <= 4:
                    self.rollResults.append(QUESTION_FACE)
                else:
                    self.rollResults.append(SKULL_FACE)
                    self.skulls += 1

        # Display roll results:
        self.die1.config(image=self.rollResults[0])
        self.die2.config(image=self.rollResults[1])
        self.die3.config(image=self.rollResults[2])

        # Display the type of dice each one is (gold, silver, bronze):
        self.dief1.config(highlightbackground=self.hand[0])
        self.dief2.config(highlightbackground=self.hand[1])
        self.dief3.config(highlightbackground=self.hand[2])

        self.collection_var.set(f'Stars collected: {self.stars}   Skulls collected: {self.skulls}')

        # Check if they've collected 3 or more skulls:
        if self.skulls >= 3:
            self.stars = 0
            self.skulls = 0
            self.result_var.set('3 or more skulls means you\'ve lost your stars!')
            self.end_button.grid_remove()
            self.roll_button.grid_remove()
            self.continue_button.grid()

    def end_turn(self):
        self.collection_var.set(self.playerNames[self.turn]+ ' got '+ str(self.stars)+ ' stars!')
        self.result_var.set('')
        # Add stars to this player's point total:
        self.playerScores[self.playerNames[self.turn]] += self.stars
        self.end_button.grid_remove()
        self.roll_button.grid_remove()
        self.continue_button.grid_remove()
        self.next_button.grid()
        self.die1.grid_remove()
        self.die2.grid_remove()
        self.die3.grid_remove()
        self.dief1.config(highlightthickness=0)
        self.dief2.config(highlightthickness=0)
        self.dief3.config(highlightthickness=0)
        # Check if they've reached 13 or more points:
        # (!) Try changing this to 5 or 50 points.
        if (self.endGameWith == None
            and self.playerScores[self.playerNames[self.turn]] >= 2):
            # Since this player reached 13 points, play one more
            # round for all other players:
            self.result_var.set(self.playerNames[self.turn] + ' has reached 13 points!!!\nEveryone else will get one more turn!')
            self.endGameWith = self.playerNames[self.turn]
        self.cup = ([GOLD] * 6) + ([SILVER] * 4) + ([BRONZE] * 3)
        self.hand = []
        # Discard the stars and skulls, but keep the question marks:
        random.shuffle(self.cup)  # Shuffle the dice in the cup.
        while len(self.hand) < 3:
            self.hand.append(self.cup.pop())

        # Move on to the next player's turn:
        self.turn = (self.turn + 1) % self.numPlayers
        self.stars = 0
        self.skulls = 0
        # If the game has ended, break out of this loop:
        if self.endGameWith == self.playerNames[self.turn]:
            self.end_game()  # End the game.

    def end_game(self):       
        self.turn_var.set('The game has ended...')

        # Display everyone's score:
        for i in self.scores.get_children():
            self.scores.delete(i)
        for i, name in enumerate(playerNames):
            self.scores.insert('', 'end', text=name, values=(str(playerScores[name]),))

        # Find out who the winners are:
        highestScore = 0
        winners = []
        for name, score in playerScores.items():
            if score > highestScore:
                # This player has the highest score:
                highestScore = score
                winners = [name]  # Overwrite any previous winners.
            elif score == highestScore:
                # This player is tied with the highest score.
                winners.append(name)

        if len(winners) == 1:
            # There is only one winner:
            self.collection_var.set('The winner is ' + winners[0] + '!!!')
        else:
            # There are multiple tied winners:
            self.collection_var.set('The winners are: ' + ', '.join(winners))

        self.result_var.set('Thanks for playing!')
        self.next_button.grid_remove()
        self.restart_button.grid()
get_names()
root.mainloop()