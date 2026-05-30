"""Hacking Minigame, by Al Sweigart al@inventwithpython.com
The hacking mini-game from "Fallout 3". Find out which seven-letter
word is the password by using clues each guess gives you.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, artistic, game, puzzle"""

# NOTE: This program requires the sevenletterwords.txt file. You can
# download it from https://inventwithpython.com/sevenletterwords.txt

import random, sys
from tkinter import Tk, StringVar, PhotoImage, Toplevel
from tkinter.ttk import Frame, Entry, Label, Button, Notebook

# Set up the constants:
# The garbage filler characters for the "computer memory" display.
GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

# Load the WORDS list from a text file that has 7-letter words.
with open('sevenletterwords.txt') as wordListFile:
    WORDS = wordListFile.readlines()
for i in range(len(WORDS)):
    # Convert each word to uppercase and remove the trailing newline:
    WORDS[i] = WORDS[i].strip().upper()


def main():
    global memory, tries_var, info, check, cross, e, text, b, previous_var, previous_guesses, root
    """Run a single game of Hacking."""
#     print('''Hacking Minigame, by Al Sweigart al@inventwithpython.com
# Find the password in the computer's memory. You are given clues after
# each guess. For example, if the secret password is MONITOR but the
# player guessed CONTAIN, they are given the hint that 2 out of 7 letters
# were correct, because both MONITOR and CONTAIN have the letter O and N
# as their 2nd and 3rd letter. You get four guesses.\n''')
#     input('Press Enter to begin...')
    root = Tk()
    root.title('Hacking Minigame')
    check = PhotoImage(file='check_button.png')
    cross = PhotoImage(file='cross_button.png')
    f = Frame(root)
    f.grid(sticky='nwes')
    # The "computer memory" is just cosmetic, but it looks cool:
    memory = StringVar()
    Label(f, text='Find the password in the computer\'s memory:').grid(column=0, row=0)
    Label(f, textvariable=memory, font='TkFixedFont').grid(column=0, row=1)
    previous_var = StringVar()
    previous_guesses = []
    Label(f, textvariable=previous_var).grid(column=0, row=2)
    info = Label(f, compound='top')
    info.grid(column=0, row=3)
    tries_var = StringVar()
    Label(f, textvariable=tries_var).grid(column=0, row=4)
    text = StringVar()
    e = Entry(f, textvariable=text)
    e.grid(column=0, row=5)
    b = Button(f, text='Submit', default='active')
    b.grid(column=0, row=6)
    root.bind('<Return>', lambda e: b.invoke())
    Button(f, text='Help', command=help).grid(column=0, row=7)
    start()
    root.mainloop()

def start():
    global tries, secretPassword, gameWords, previous_guesses
    gameWords = getWords()
    memory.set(getComputerMemoryString(gameWords))
    secretPassword = random.choice(gameWords)
    previous_var.set('Previous guesses:\nThere are no previously guessed words.')
    previous_guesses = []
    tries = 4
    tries_var.set(f'Enter password: ({tries} tries remaining)')
    b.config(text='Submit', command=submit)
    info.config(image='', text='')
    e.grid()

def getWords():
    """Return a list of 12 words that could possibly be the password.

    The secret password will be the first word in the list.
    To make the game fair, we try to ensure that there are words with
    a range of matching numbers of letters as the secret word."""
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    # Find two more words; these have zero matching letters.
    # We use "< 3" because the secret password is already in words.
    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    # Find two words that have 3 matching letters (but give up at 500
    # tries if not enough can be found).
    for i in range(500):
        if len(words) == 5:
            break  # Found 5 words, so break out of the loop.

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    # Find at least seven words that have at least one matching letter
    # (but give up at 500 tries if not enough can be found).
    for i in range(500):
        if len(words) == 12:
            break  # Found 7 or more words, so break out of the loop.

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    # Add any random words needed to get 12 words total.
    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)

    assert len(words) == 12
    return words


def getOneWordExcept(blocklist=None):
    """Returns a random word from WORDS that isn't in blocklist."""
    if blocklist == None:
        blocklist = []

    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2):
    """Returns the number of matching letters in these two words."""
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getComputerMemoryString(words):
    """Return a string representing the "computer memory"."""

    # Pick one line per word to contain a word. There are 16 lines, but
    # they are split into two halves.
    linesWithWords = random.sample(range(16 * 2), len(words))
    # The starting memory address (this is also cosmetic).
    memoryAddress = 16 * random.randint(0, 4000)

    # Create the "computer memory" string.
    computerMemory = []  # Will contain 16 strings, one for each line.
    nextWord = 0  # The index in words of the word to put into a line.
    for lineNum in range(16):  # The "computer memory" has 16 lines.
        # Create a half line of garbage characters:
        leftHalf = ''
        rightHalf = ''
        for j in range(16):  # Each half line has 16 characters.
            leftHalf += random.choice(GARBAGE_CHARS)
            rightHalf += random.choice(GARBAGE_CHARS)

        # Fill in the password from words:
        if lineNum in linesWithWords:
            # Find a random place in the half line to insert the word:
            insertionIndex = random.randint(0, 9)
            # Insert the word:
            leftHalf = (leftHalf[:insertionIndex] + words[nextWord]
                + leftHalf[insertionIndex + 7:])
            nextWord += 1  # Update the word to put in the half line.
        if lineNum + 16 in linesWithWords:
            # Find a random place in the half line to insert the word:
            insertionIndex = random.randint(0, 9)
            # Insert the word:
            rightHalf = (rightHalf[:insertionIndex] + words[nextWord]
                + rightHalf[insertionIndex + 7:])
            nextWord += 1  # Update the word to put in the half line.

        computerMemory.append('0x' + hex(memoryAddress)[2:].zfill(4)
                     + '  ' + leftHalf + '    '
                     + '0x' + hex(memoryAddress + (16*16))[2:].zfill(4)
                     + '  ' + rightHalf)

        memoryAddress += 16  # Jump from, say, 0xe680 to 0xe690.

    # Each string in the computerMemory list is joined into one large
    # string to return:
    return '\n'.join(computerMemory)


def submit():
    global tries
    """Let the player enter a password guess."""
    guess = text.get().upper()
    text.set('')
    if not guess in gameWords:
        info.config(image=None, text='That is not one of the possible passwords listed above.\nTry entering "{}" or "{}".'.format(gameWords[0], gameWords[1]))
        return
    if guess == secretPassword:
        info.config(image=check, text='Access Granted')
        tries_var.set('')
        e.grid_remove()
        b.config(text='Restart', command=start)
    else:
        tries -= 1
        numMatches = numMatchingLetters(secretPassword, guess)
        info.config(image=cross, text='Access Denied ({}/7 correct)'.format(numMatches))
        tries_var.set(f'Enter password: ({tries} tries remaining)')
    if tries == 0:
        tries_var.set(f'Out of tries. Secret password was {secretPassword}.')
        e.grid_remove()
        b.config(text='Restart', command=start)
    previous_guesses.append(f'{guess} ({numMatchingLetters(secretPassword, guess)}/7)')
    previous_var.set(f'Previous guesses:\n' + '\n'.join(previous_guesses))

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    n = Notebook(f)
    n.grid()
    n.add(Label(n, text='''Welcome to Hacking Minigame!
In this game, you get to hack into a computer by finding a
password in the computer's memory. You get 4 tries.

This app is inspired by Al Sweigart's Hacking Minigame.'''), text='Overview')
    
    memory_help = Frame(n)
    Label(memory_help, text='''To know what passwords to try, you can find them in the
computer memory. Here's how.
Suppose the computer memory looked like this:''').grid(column=0, row=0)
    Label(memory_help, text='''0x6900  .=#{;(PENALTY}|,    0x6940  ~.+[>$>@@+]={+%@
0x6910  !_(/+%[}%(&,.%^?    0x6950  [{+#_^VARIETY:_<
0x6920  $$~(FANTASY<==[)    0x6960  PORTION{%{[|&&[/
0x6930  (&]{,{$?&<@{[_@[    0x6970  ;PRODUCT]?(;?~@.''', font='TkFixedFont').grid(column=0, row=1)
    Label(memory_help, text='''
First, we ignore all the memory sections that start with 0x,
as those are irrelevant. The punctuation marks are also
irrelevant. After removing the irrelevant characters, we can
that the password could be either PENALTY, VARIETY, FANTASY,
PORTION, or PRODUCT.
(In the game, the memory is bigger.)''').grid(column=0, row=2)
    n.add(memory_help, text='Interpreting the computer memory')
    
    n.add(Label(n, text='''
To enter a password, enter it in the entry box and press Submit
or press the Enter/Return key on your keyboard. The screen will
show how many letters in the password you guessed are correct.
If a letter is correct, it appears in the password in the same
position that appears in the password that you guessed. You can
only guess passwords that are in the computer memory (see
Interpreting the computer memory). After 4 guesses, the
correct password is revealed. Previous guesses also show up in
the Previous Guesses section, along with how many letters are
correct.'''), text='Guessing')

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    main()