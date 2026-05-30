"""Blackjack, by Al Sweigart al@inventwithpython.com
The classic card game also known as 21. (This version doesn't have
splitting or insurance.)
More info at: https://en.wikipedia.org/wiki/Blackjack
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, card game"""

import random, sys
from tkinter import Tk, Canvas, PhotoImage, Toplevel, StringVar
from tkinter.ttk import Frame, Button, Label, Entry

# Set up the constants:
card_poss = {'A': ((50, 75),), '2': ((50, 37.5), (50, 112.5),), '3': ((50, 25),(50, 75),(50, 125)), '4': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5)), '5': ((50, 75),(25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5)),
'6': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75)), '7': ((25, 37.5), (25, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75), (50, 75)), '8': ((25, 37.5), (50, 37.5), (25, 112.5), (50, 112.5),(75, 37.5), (75, 112.5), (25, 75), (75, 75)),
 '9': ((25, 18.75), (25, 93.75), (25, 131.25), (75, 93.75),(75, 18.75), (75, 131.25), (25, 56.25), (75, 56.25), (50, 75)), '10': ((25, 18.75), (25, 93.75), (25, 131.25), (75, 93.75),(75, 18.75), (75, 131.25), (25, 56.25), (75, 56.25), (50, 37.5), (50, 112.5))}

# (A list of chr codes is at https://inventwithpython.com/charactermap)
BACKSIDE = ('backside', None)

def draw_card(card, suit, canvas):
    if card == 'backside':
        canvas.create_image(0, 0, image=back_image, anchor='nw')
        return
    if card in ('J', 'Q', 'K', 'joker'):
        for i in ((25,75), (75,75)):
            canvas.create_text(i[0], i[1], text=suit)
        canvas.create_text(50, 75, text={'K': '🤴', 'Q': '👸', 'J':'💂', 'joker':'🤹'}[card], font=('Arial', 15))
    else:
        for i in card_poss[card]:
            canvas.create_text(i[0], i[1], text=suit, font=('Arial', 15))
    canvas.create_text(2, 2, text=f'{card}\n{suit}', anchor='nw', font=('Arial', 10))
    canvas.create_text(98, 148, text=f'{suit}\n{card}', anchor='se', font=('Arial', 10))


def displayCards(cards, frame):
    for i in frame.winfo_children():
        i.destroy()
    global card_canvases
    """Display all the cards in the cards list."""
    card_canvases = []
    for i, card in enumerate(cards):
        c = Canvas(frame, width=100, height=150)
        draw_card(card[0], card[1], c)
        c.grid(column=i, row=0)

def show_instructions():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Blackjack!
Rules:
Try to get as close to 21 without going over.
Kings, Queens, and Jacks are worth 10 points.
Aces are worth 1 or 11 points.
Cards 2 through 10 are worth their face value.
(H)it to take another card.
(S)tand to stop taking cards.
On your first play, you can (D)ouble down to increase your bet
but must hit exactly one more time before standing.
In case of a tie, the bet is returned to the player.
The dealer stops hitting at 17.
Based on Al Sweigart's Blackjack.''').grid()

def main():
    global card_canvases, dealer_cards, player_cards, dealer_value, player_value, root, back_image, bet_frame, f, player_controls, info_var, dealer_controls, broke
    card_canvases = []
    root = Tk()
    root.title('Blackjack')
    back_image = PhotoImage(file='backside.png')
    mf = Frame(root)
    mf.grid(sticky='nwes')
    f = Frame(mf)
    f.grid(sticky='nwes') ; f.grid_remove()
    info_var = StringVar()
    Label(f, textvariable=info_var).grid(column=0, row=0)
    dealer_value = StringVar()
    Label(f, textvariable=dealer_value).grid(column=0, row=1)
    dealer_cards = Frame(f)
    dealer_cards.grid(column=0, row=2)
    player_value = StringVar()
    Label(f, textvariable=player_value).grid(column=0, row=3)
    player_cards = Frame(f)
    player_cards.grid(column=0, row=4)
    bet_frame = Frame(mf)
    bet_frame.grid(sticky='nwes')
    player_controls = Frame(f)
    player_controls.grid(column=0, row=5)
    dealer_controls = Frame(f)
    dealer_controls.grid(column=0, row=5) ; dealer_controls.grid_remove()
    broke = Frame(mf)
    broke.grid(sticky='nwes') ; broke.grid_remove()
    g = game()
    Label(broke, text='You\'re broke!\nGood thing you weren\'t playing with real money.\nPress Continue to reload money.').grid(column=0, row=0)
    Button(broke, text='Continue', command=g.__init__).grid(column=0, row=1)
    Button(mf, text='Help', command=show_instructions).grid(column=0, row=1)
    root.mainloop()

class game:
    def __init__(self):
        broke.grid_remove()
        f.grid()
        self.money = 5000
        self.start()

    def start(self):
        if self.money == 0:
            f.grid_remove()
            broke.grid()
            return
        self.bet = self.getBet(self.money)
        self.deck = self.getDeck()
        self.playerHand, self.dealer_hand = None, None
        self.dealerHand = [self.deck.pop(), self.deck.pop()]
        self.playerHand = [self.deck.pop(), self.deck.pop()]
        self.displayHands(self.playerHand, self.dealerHand, False)
        self.play()

    def play(self):
        try:
            self.restart.grid_remove()
        except:
            pass
        player_controls.grid()
        # Check if the player has bust:
        if self.getHandValue(self.playerHand) > 21:
            pass

        # Get the player's move, either H, S, or D:
        for i in player_controls.winfo_children():
            i.destroy()
        info_var.set('')
        Button(player_controls, text='Hit', command=self.take_card).grid(column=0, row=0)
        Button(player_controls, text='Stand', command=self.dealer_turn).grid(column=1, row=0)
        self.dd_button = Button(player_controls, text='Double down', command=self.double_down)
        self.dd_button.grid(column=2, row=0)
        if self.money - self.bet == 0:
            self.dd_button.state(['disabled'])

        # Handle the player actions:
    def double_down(self):
        # Player is doubling down, they can increase their bet:
        additionalBet = self.getBet(min(self.bet, (self.money - self.bet)))
        self.bet += additionalBet
        print('Bet increased to {}.'.format(self.bet))
        print('Bet:', self.bet)
        self.take_card()
        self.dealer_turn()
    
    def take_card(self):
        # Hit/doubling down takes another card.
        self.dd_button.state(['disabled'])
        newCard = self.deck.pop()
        rank, suit = newCard
        self.playerHand.append(newCard)
        info_var.set(f'You drew a {rank} of {suit}.')

        if self.getHandValue(self.playerHand) > 21:
            # The player has busted:
            self.dealer_turn()
        self.displayHands(self.playerHand, self.dealerHand, False)
        return

        # Give the dealer and player two cards from the deck each:
    def dealer_turn(self):
        player_controls.grid_remove()
        dealer_controls.grid()
        for i in dealer_controls.winfo_children():
            i.destroy()
        self.dealer_info = StringVar()
        Label(dealer_controls, textvariable=self.dealer_info).grid(column=0, row=0)
        # Handle the dealer's actions:
        if self.getHandValue(self.playerHand) <= 21:
            if self.getHandValue(self.dealerHand) < 17:
                # The dealer hits:
                self.dealer_info.set('Dealer hits...')
                self.dealerHand.append(self.deck.pop())
                self.displayHands(self.playerHand, self.dealerHand, False)
                info_var.set('Dealer drew a {} of {}.'.format(*self.dealerHand[-1]))

                if self.getHandValue(self.dealerHand) > 21:
                    print('Game ending')
                    Button(dealer_controls, text='Continue', command=self.end_game).grid(column=0, row=1)
                    return
                Button(dealer_controls, text='Continue', command=self.dealer_turn).grid(column=0, row=1)  # The dealer has busted.
            self.dealer_info.set('Dealer stands. Press Continue to finish.')
            Button(dealer_controls, text='Continue', command=self.end_game).grid(column=0, row=1)
        else:
            self.dealer_info.set('Dealer stands. Press Continue to finish.')
            Button(dealer_controls, text='Continue', command=self.end_game).grid(column=0, row=1)

    def end_game(self):
        # Show the final hands:
        self.displayHands(self.playerHand, self.dealerHand, True)
        dealer_controls.grid_remove()

        playerValue = self.getHandValue(self.playerHand)
        dealerValue = self.getHandValue(self.dealerHand)
        # Handle whether the player won, lost, or tied:
        if dealerValue > 21:
            info_var.set('Dealer busts! You win ${}! 🤑'.format(self.bet))
            self.money += self.bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            info_var.set('You lost!')
            self.money -= self.bet
        elif playerValue > dealerValue:
            info_var.set('You won ${}! 🤑'.format(self.bet))
            self.money += self.bet
        elif playerValue == dealerValue:
            info_var.set('It\'s a tie, the bet is returned to you.')
        self.restart = Button(f, text='Restart', command=self.start)
        self.restart.grid(column=0, row=5)


    def getBet(self, maxBet):
        self.maxBet = maxBet
        self.betted = False
        f.grid_remove()
        bet_frame.grid()
        for i in bet_frame.winfo_children():
            i.destroy()
        self.bet_error = StringVar()
        Label(bet_frame, textvariable=self.bet_error).grid(column=0, row=0)
        Label(bet_frame, text=f'How much do you bet? (1-{maxBet})').grid(column=0, row=1)
        self.bet_var = StringVar()
        Entry(bet_frame, textvariable=self.bet_var).grid(column=0, row=2)
        Button(bet_frame, text='Submit', command=self.check_bet).grid(column=0, row=3)
        while not self.betted:
            root.update()
        bet_frame.grid_remove()
        f.grid()
        return int(self.bet_var.get())

    def check_bet(self):
        bet = self.bet_var.get()

        if not bet.isdecimal():
            self.bet_error.set('Please enter a number.')  # If the player didn't enter a number, ask again.
            return

        bet = int(bet)
        if 1 <= bet <= self.maxBet:
            self.betted = True  # Player entered a valid bet.
        else:
            self.bet_error.set(f'Please enter a number between\n1 and {self.maxBet}.')


    def getDeck(self):
        """Return a list of (rank, suit) tuples for all 52 cards."""
        deck = []
        for suit in ('♥️', '♦️', '♠️', '♣️'):
            for rank in range(2, 11):
                deck.append((str(rank), suit))  # Add the numbered cards.
            for rank in ('J', 'Q', 'K', 'A'):
                deck.append((rank, suit))  # Add the face and ace cards.
        random.shuffle(deck)
        return deck


    def displayHands(self, playerHand, dealerHand, showDealerHand):
        """Show the player's and dealer's cards. Hide the dealer's first
        card if showDealerHand is False."""
        if showDealerHand:
            dealer_value.set('DEALER: '+ str(self.getHandValue(dealerHand)))
            displayCards(dealerHand, dealer_cards)
        else:
            dealer_value.set('DEALER: ???')
            # Hide the dealer's first card:
            displayCards([BACKSIDE] + dealerHand[1:], dealer_cards)

        # Show the player's cards:
        player_value.set('PLAYER: '+ str(self.getHandValue(playerHand)))
        displayCards(playerHand, player_cards)


    def getHandValue(self, cards):
        """Returns the value of the cards. Face cards are worth 10, aces are
        worth 11 or 1 (this function picks the most suitable ace value)."""
        value = 0
        numberOfAces = 0

        # Add the value for the non-ace cards:
        for card in cards:
            rank = card[0]  # card is a tuple like (rank, suit)
            if rank == 'A':
                numberOfAces += 1
            elif rank in ('K', 'Q', 'J'):  # Face cards are worth 10 points.
                value += 10
            else:
                value += int(rank)  # Numbered cards are worth their number.

        # Add the value for the aces:
        value += numberOfAces  # Add 1 per ace.
        for i in range(numberOfAces):
            # If another 10 can be added without busting, do so:
            if value + 10 <= 21:
                value += 10

        return value

# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()