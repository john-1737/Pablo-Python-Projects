"""Clickbait Headline Generator, by Al Sweigart al@inventwithpython.com
A clickbait headline generator for your soulless content farm website.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, beginner, humor, word"""

import random
from tkinter import Tk, StringVar, Menu
from tkinter.ttk import Treeview, Entry, Label, Button, Frame, Scrollbar
from pyperclip import copy as clip

# Set up the constants:
OBJECT_PRONOUNS = ['Her', 'Him', 'Them']
POSSESIVE_PRONOUNS = ['Her', 'His', 'Their']
PERSONAL_PRONOUNS = ['She', 'He', 'They']
STATES = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania',
          'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
NOUNS = ['Athlete', 'Clown', 'Shovel', 'Paleo Diet', 'Doctor', 'Parent',
         'Cat', 'Dog', 'Chicken', 'Robot', 'Video Game', 'Avocado',
         'Plastic Straw', 'Serial Killer', 'Telephone Psychic']
PEOPLE = ['Athlete', 'Clown', 'Doctor', 'Parent', 'Serial Killer', 'Telephone Psychic']
PLACES = ['House', 'Attic', 'Bank Deposit Box', 'School', 'Basement',
          'Workplace', 'Donut Shop', 'Apocalypse Bunker']
WHEN = ['Soon', 'This Year', 'Later Today', 'RIGHT NOW', 'Next Week']


def main():
    global headlines, error, t, endmessage
    root = Tk()
    root.title('Clickbait Headline Generator')
    f = Frame(root)
    f.grid(sticky='nwes')
    Label(f, text='Our website needs to trick people into looking at ads!').grid(column=0, row=0, columnspan=2)
    error = StringVar()
    Label(f, textvariable=error).grid(column=0, row=1, columnspan=2)
    Label(f, text='Enter the number of clickbait headlines to generate:').grid(column=0, row=2, columnspan=2)
    headlines = StringVar()
    Entry(f, textvariable=headlines).grid(column=0, row=3, columnspan=2)
    Button(f, text='Generate headlines', command=generate_headlines, default='active').grid(column=0, row=4, columnspan=2)
    t = Treeview(f)
    t.grid(column=0, row=5, sticky='ew')
    s1 = Scrollbar(f, orient='vertical', command=t.yview)
    t['yscrollcommand'] = s1.set
    s1.grid(column=1, row=5, sticky='ns')
    s2 = Scrollbar(f, orient='horizontal', command=t.xview)
    t['xscrollcommand'] = s2.set
    s2.grid(column=0, row=6, sticky='ew')
    endmessage = StringVar()
    Button(f, text='Copy Selection', command=copy).grid(column=0, row=7, columnspan=2)
    Label(f, textvariable=endmessage).grid(column=0, row=8, columnspan=2)
    root.mainloop()
    
def generate_headlines():
    if not headlines.get().isdecimal():
        error.set('Please enter a number.')
        headlines.set('')
        return
    numberOfHeadlines = int(headlines.get())
    error.set('')
    for i in t.get_children():
        t.delete(i)

    for i in range(numberOfHeadlines):
        clickbaitType = random.randint(1, 8)

        if clickbaitType == 1:
            headline = generateAreMillenialsKillingHeadline()
        elif clickbaitType == 2:
            headline = generateWhatYouDontKnowHeadline()
        elif clickbaitType == 3:
            headline = generateBigCompaniesHateHerHeadline()
        elif clickbaitType == 4:
            headline = generateYouWontBelieveHeadline()
        elif clickbaitType == 5:
            headline = generateDontWantYouToKnowHeadline()
        elif clickbaitType == 6:
            headline = generateGiftIdeaHeadline()
        elif clickbaitType == 7:
            headline = generateReasonsWhyHeadline()
        elif clickbaitType == 8:
            headline = generateJobAutomatedHeadline()

        t.insert('', 'end', text=headline)

    website = random.choice(['wobsite', 'blag', 'Facebuuk', 'Googles',
                             'Facesbook', 'Tweedie', 'Pastagram'])
    when = random.choice(WHEN).lower()
    endmessage.set(f'Post these to our {website} {when} or you\'re fired!')

# Each of these functions returns a different type of headline:
def generateAreMillenialsKillingHeadline():
    noun = random.choice(NOUNS)
    return 'Are Millenials Killing the {} Industry?'.format(noun)


def generateWhatYouDontKnowHeadline():
    noun = random.choice(NOUNS)
    pluralNoun = random.choice(NOUNS) + 's'
    when = random.choice(WHEN)
    return 'Without This {}, {} Could Kill You {}'.format(noun, pluralNoun, when)


def generateBigCompaniesHateHerHeadline():
    pronoun = random.choice(OBJECT_PRONOUNS)
    state = random.choice(STATES)
    noun1 = random.choice(PEOPLE)
    noun2 = random.choice(NOUNS)
    return 'Big Companies Hate {}! See How This {} {} Invented a Cheaper {}'.format(pronoun, state, noun1, noun2)


def generateYouWontBelieveHeadline():
    state = random.choice(STATES)
    noun = random.choice(NOUNS)
    pronoun = random.choice(POSSESIVE_PRONOUNS)
    place = random.choice(PLACES)
    return 'You Won\'t Believe What This {} {} Found in {} {}'.format(state, noun, pronoun, place)


def generateDontWantYouToKnowHeadline():
    pluralNoun1 = random.choice(PEOPLE) + 's'
    pluralNoun2 = random.choice(NOUNS) + 's'
    return 'What {} Don\'t Want You To Know About {}'.format(pluralNoun1, pluralNoun2)


def generateGiftIdeaHeadline():
    number = random.randint(7, 15)
    noun = random.choice(NOUNS)
    state = random.choice(STATES)
    return '{} Gift Ideas to Give Your {} From {}'.format(number, noun, state)


def generateReasonsWhyHeadline():
    number1 = random.randint(3, 19)
    pluralNoun = random.choice(NOUNS) + 's'
    # number2 should be no larger than number1:
    number2 = random.randint(1, number1)
    return '{} Reasons Why {} Are More Interesting Than You Think (Number {} Will Surprise You!)'.format(number1, pluralNoun, number2)


def generateJobAutomatedHeadline():
    state = random.choice(STATES)
    noun = random.choice(PEOPLE)

    i = random.randint(0, 2)
    pronoun1 = POSSESIVE_PRONOUNS[i]
    pronoun2 = PERSONAL_PRONOUNS[i]
    if pronoun1 == 'Their':
        return 'These {} {}s Didn\'t Think Robots Would Take {} Jobs. {} Were Wrong.'.format(state, noun, pronoun1, pronoun2)
    else:
        return 'This {} {} Didn\'t Think Robots Would Take {} Job. {} Was Wrong.'.format(state, noun, pronoun1, pronoun2)

def copy():
    clip(t.item(t.focus(), option="text"))

# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
