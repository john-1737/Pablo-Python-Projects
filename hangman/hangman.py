"""Hangman, by Al Sweigart al@inventwithpython.com
Guess the letters to a secret word before the hangman is drawn.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, word, puzzle"""

# A version of this game is featured in the book "Invent Your Own
# Computer Games with Python" https://nostarch.com/inventwithpython

import random, sys
from tkinter import Tk, PhotoImage, Menu, Toplevel
from tkinter.ttk import Frame, Label, Button

# Set up the constants:
# (!) Try adding or changing the strings in HANGMAN_PICS to make a
# guillotine instead of a gallows.


# (!) Try replacing CATEGORY and WORDS with new strings.
CATEGORY = 'Animals'
WORDS = 'ANT BABOON BADGER BAT BEAR BEAVER CAMEL CAT CLAM COBRA COUGAR COYOTE CROW DEER DOG DONKEY DUCK EAGLE FERRET FOX FROG GOAT GOOSE HAWK LION LIZARD LLAMA MOLE MONKEY MOOSE MOUSE MULE NEWT OTTER OWL PANDA PARROT PIGEON PYTHON RABBIT RAM RAT RAVEN RHINO SALMON SEAL SHARK SHEEP SKUNK SLOTH SNAKE SPIDER STORK SWAN TIGER TOAD TROUT TURKEY TURTLE WEASEL WHALE WOLF WOMBAT ZEBRA'.lower().split()


def main():
    global HANGMAN_PICS, f, root, l, bot
    root = Tk()
    root.title('Hangman')
    HANGMAN_PICS = [PhotoImage(file=f'hangman{i}.png') for i in range(1, 8)]
    f = Frame(root)
    f.grid(sticky='nwes')
    l = Label(f, compound='right')
    l.grid(column=0, row=0)
    Button(f, text='New Game', command=new_game).grid(column=0, row=1)
    bot = Label(f, wraplength=200)
    bot.grid(column=0, row=2)
    bot.grid_remove()
    m = Menu(root)
    root['menu'] = m
    help = Menu(m)
    m.add_cascade(menu=help, label='Help ')
    help.add_command(label='Instructions', command=show_help)
    help.add_checkbutton(label='Show Bot', command=toggle_bot)
    new_game()

def new_game():
    global missedLetters, correctLetters, secretWord

    # Setup variables for a new game:
    missedLetters = []  # List of incorrect letter guesses.
    correctLetters = []  # List of correct letter guesses.
    secretWord = random.choice(WORDS)  # The word the player must guess.

    drawHangman(missedLetters, correctLetters, secretWord)
    for i in 'abcdefghijklmnopqrstuvwxyz':
        root.bind(f'<{i}>', play_turn)
    bot.config(text=f'The possible words are:\n{", ".join([i for i in WORDS if len(i) == len(secretWord)])}')
    root.mainloop()

def play_turn(event):
    guess = event.keysym
    
    if guess in secretWord:
        # Add the correct guess to correctLetters:
        correctLetters.append(guess)
        drawHangman(missedLetters, correctLetters, secretWord)

        # Check if the player has won:
        foundAllLetters = True  # Start off assuming they've won.
        for secretWordLetter in secretWord:
            if secretWordLetter not in correctLetters:
                # There's a letter in the secret word that isn't
                # yet in correctLetters, so the player hasn't won:
                foundAllLetters = False
                break
        if foundAllLetters:
            for i in 'abcdefghijklmnopqrstuvwxyz':
                root.unbind(f'<{i}>')
            l.config(text=f'''The category is: {CATEGORY}
{"Missed letters: " + " ".join(missedLetters) if not len(missedLetters) == 0 else "No missed letters yet."}
{' '.join(get_blanks())}

Yes! The secret word is: {secretWord}
You have won!''')
            
    else:
        # The player has guessed incorrectly:
        missedLetters.append(guess)
        drawHangman(missedLetters, correctLetters, secretWord)

        # Check if player has guessed too many times and lost. (The
        # "- 1" is because we don't count the empty gallows in
        # HANGMAN_PICS.)
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            for i in 'abcdefghijklmnopqrstuvwxyz':
                root.unbind(f'<{i}>')
            l.config(text=f'''The category is: {CATEGORY}
{"Missed letters: " + " ".join(missedLetters) if not len(missedLetters) == 0 else "No missed letters yet."}
{' '.join(get_blanks())}

You have run out of guesses!
The word was: {secretWord}''')
            
    for i in 'abcdefghijklmnopqrstuvwxyz':
        if i in missedLetters:
            root.unbind(i)
        elif i in correctLetters:
            root.unbind(i)
    
    letter_positions = {}
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            letter_positions[i] = secretWord[i]

    possible_words1 = [i for i in WORDS if len(i) == len(secretWord)]
    if letter_positions == {}:
        possible_words = possible_words1
    else:
        possible_words = []
        for i in possible_words1:
            is_possible = True
            for j, k in letter_positions.items():
                if not i[j] == k:
                    is_possible = False
            if is_possible:
                possible_words.append(i)
    for i in missedLetters:
        possible_words = [j for j in possible_words if not i in j]

    bot.config(text=f'The possible words are:\n{", ".join(possible_words)}')

def get_blanks():
    # Display the blanks for the secret word (one blank per letter):
    blanks = ['_'] * len(secretWord)

    # Replace blanks with correctly guessed letters:
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks[i] = secretWord[i]
    return blanks

def drawHangman(missedLetters, correctLetters, secretWord):
    """Draw the current state of the hangman, along with the missed and
    correctly-guessed letters of the secret word."""
    # Display the blanks for the secret word (one blank per letter):
    blanks = ['_'] * len(secretWord)

    # Replace blanks with correctly guessed letters:
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks[i] = secretWord[i]
    l.config(image=HANGMAN_PICS[len(missedLetters)], text=f'''The category is: {CATEGORY}
{"Missed letters: " + " ".join(missedLetters) if not len(missedLetters) == 0 else "No missed letters yet."}
{' '.join(blanks)}

Guess a letter.''')
    
def toggle_bot():
    if bot.winfo_ismapped():
        bot.grid_remove()
    else:
        bot.grid()

def show_help():
    win = Toplevel(root)
    win.title('Instructions')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Hangman!
In this game, you guess a word by guessing letters. If you guess a letter wrong,
another part of the hangman will be drawn. There can be 6 parts of the hangman
drawn on top of the empty gallows, every time you guess a letter incorrectly, as
shown here along with the empty gallows:''').grid(column=0, row=0, columnspan=7)
    for i, j in enumerate(HANGMAN_PICS):
        Label(f, image=j).grid(column=i, row=1)
    Label(f, text='''When the entire hangman is drawn, the game ends. You can start a new game at any
time by pressing New Game.
As you guess letters, they will be added to the word. Letters that haven't been
guessed will show as blanks, as this example shows:
          
_ _ _ _ a

For this word, we know the last letter is an A, but we don't know the other
letters. You can simply press a key to guess a letter, but you can't guess a
letter twice. When you guess a letter, all occurrences of the letter appear in
the word.
You can also turn on the bot feature in the Help menu, which shows all possible
words.
This program is inspired by Al Sweigart's Hangman.''').grid(column=0, row=2, columnspan=7)

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()
