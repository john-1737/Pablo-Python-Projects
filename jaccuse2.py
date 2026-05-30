"""J'ACCUSE!, by Al Sweigart al@inventwithpython.com
A mystery game of intrigue and a missing cat.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: extra-large, game, humor, puzzle"""

# Play the original Flash game at:
# https://homestarrunner.com/videlectrix/wheresanegg.html
# More info at: http://www.hrwiki.org/wiki/Where's_an_Egg%3F

import time, random, sys
from tkinter import ttk, Tk, Listbox, Button, Label, messagebox, StringVar
from tkinter.ttk import Treeview

# Set up the constants:
SUSPECTS = ['DUKE HAUTDOG', 'MAXIMUM POWERS', 'BILL MONOPOLIS', 'SENATOR SCHMEAR', 'MRS. FEATHERTOSS', 'DR. JEAN SPLICER', 'RAFFLES THE CLOWN', 'ESPRESSA TOFFEEPOT', 'CECIL EDGAR VANDERTON']
ITEMS = ['FLASHLIGHT', 'CANDLESTICK', 'RAINBOW FLAG', 'HAMSTER WHEEL', 'ANIME VHS TAPE', 'JAR OF PICKLES', 'ONE COWBOY BOOT', 'CLEAN UNDERPANTS', '5 DOLLAR GIFT CARD']
PLACES = ['ZOO', 'OLD BARN', 'DUCK POND', 'CITY HALL', 'HIPSTER CAFE', 'BOWLING ALLEY', 'VIDEO GAME MUSEUM', 'UNIVERSITY LIBRARY', 'ALBINO ALLIGATOR PIT']
time_to_solve = 300  # 300 seconds (5 minutes) to solve the game.

# First letters and longest length of places are needed for menu display:
PLACE_FIRST_LETTERS = {}
LONGEST_PLACE_NAME_LENGTH = 0
for place in PLACES:
    PLACE_FIRST_LETTERS[place[0]] = place
    if len(place) > LONGEST_PLACE_NAME_LENGTH:
        LONGEST_PLACE_NAME_LENGTH = len(place)

# Basic sanity checks of the constants:
assert len(SUSPECTS) == 9
assert len(ITEMS) == 9
assert len(PLACES) == 9
# First letters must be unique:
assert len(PLACE_FIRST_LETTERS.keys()) == len(PLACES)


knownSuspectsAndItems = []
# visitedPlaces: Keys=places, values=strings of the suspect & item there.
visitedPlaces = {}
currentLocation = 'TAXI'  # Start the game at the taxi.
accusedSuspects = []  # Accused suspects won't offer clues.
liars = random.sample(SUSPECTS, random.randint(3, 4))
accusationsLeft = 3  # You can accuse up to 3 people.
culprit = random.choice(SUSPECTS)

# Common indexes link these; e.g. SUSPECTS[0] and ITEMS[0] are at PLACES[0].
random.shuffle(SUSPECTS)
random.shuffle(ITEMS)
random.shuffle(PLACES)

# Create data structures for clues the truth-tellers give about each
# item and suspect.
# clues: Keys=suspects being asked for a clue, value="clue dictionary".
clues = {}
for i, interviewee in enumerate(SUSPECTS):
    if interviewee in liars:
        continue  # Skip the liars for now.

    # This "clue dictionary" has keys=items & suspects,
    # value=the clue given.
    clues[interviewee] = {}
    clues[interviewee]['debug_liar'] = False  # Useful for debugging.
    for item in ITEMS:  # Select clue about each item.
        if random.randint(0, 1) == 0:  # Tells where the item is:
            clues[interviewee][item] = PLACES[ITEMS.index(item)]
        else:  # Tells who has the item:
            clues[interviewee][item] = SUSPECTS[ITEMS.index(item)]
    for suspect in SUSPECTS:  # Select clue about each suspect.
        if random.randint(0, 1) == 0:  # Tells where the suspect is:
            clues[interviewee][suspect] = PLACES[SUSPECTS.index(suspect)]
        else:  # Tells what item the suspect has:
            clues[interviewee][suspect] = ITEMS[SUSPECTS.index(suspect)]

# Create data structures for clues the liars give about each item
# and suspect:
for i, interviewee in enumerate(SUSPECTS):
    if interviewee not in liars:
        continue  # We've already handled the truth-tellers.

    # This "clue dictionary" has keys=items & suspects,
    # value=the clue given:
    clues[interviewee] = {}
    clues[interviewee]['debug_liar'] = True  # Useful for debugging.

    # This interviewee is a liar and gives wrong clues:
    for item in ITEMS:
        if random.randint(0, 1) == 0:
            while True:  # Select a random (wrong) place clue.
                # Lies about where the item is.
                clues[interviewee][item] = random.choice(PLACES)
                if clues[interviewee][item] != PLACES[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
        else:
            while True:  # Select a random (wrong) suspect clue.
                clues[interviewee][item] = random.choice(SUSPECTS)
                if clues[interviewee][item] != SUSPECTS[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
    for suspect in SUSPECTS:
        if random.randint(0, 1) == 0:
            while True:  # Select a random (wrong) place clue.
                clues[interviewee][suspect] = random.choice(PLACES)
                if clues[interviewee][suspect] != PLACES[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
        else:
            while True:  # Select a random (wrong) item clue.
                clues[interviewee][suspect] = random.choice(ITEMS)
                if clues[interviewee][suspect] != ITEMS[SUSPECTS.index(suspect)]:
                    # Break out of the loop when wrong clue is selected.
                    break

# Create the data structures for clues given when asked about Zophie:
zophieClues = {}
for interviewee in random.sample(SUSPECTS, random.randint(3, 4)):
    kindOfClue = random.randint(1, 3)
    if kindOfClue == 1:
        if interviewee not in liars:
            # They tell you who has Zophie.
            zophieClues[interviewee] = culprit
        elif interviewee in liars:
            while True:
                # Select a (wrong) suspect clue.
                zophieClues[interviewee] = random.choice(SUSPECTS)
                if zophieClues[interviewee] != culprit:
                    # Break out of the loop when wrong clue is selected.
                    break

    elif kindOfClue == 2:
        if interviewee not in liars:
            # They tell you where Zophie is.
            zophieClues[interviewee] = PLACES[SUSPECTS.index(culprit)]
        elif interviewee in liars:
            while True:
                # Select a (wrong) place clue.
                zophieClues[interviewee] = random.choice(PLACES)
                if zophieClues[interviewee] != PLACES[SUSPECTS.index(culprit)]:
                    # Break out of the loop when wrong clue is selected.
                    break
    elif kindOfClue == 3:
        if interviewee not in liars:
            # They tell you what item Zophie is near.
            zophieClues[interviewee] = ITEMS[SUSPECTS.index(culprit)]
        elif interviewee in liars:
            while True:
                # Select a (wrong) item clue.
                zophieClues[interviewee] = random.choice(ITEMS)
                if zophieClues[interviewee] != ITEMS[SUSPECTS.index(culprit)]:
                    # Break out of the loop when wrong clue is selected.
                    break

# EXPERIMENT: Uncomment this code to view the clue data structures:
#import pprint
#pprint.pprint(clues)
#pprint.pprint(zophieClues)
#print('culprit =', culprit)
game_over = False


def update_time():
    global time_to_solve
    time_to_solve -= 1
    minutesLeft = int(time_to_solve) // 60
    secondsLeft = int(time_to_solve) % 60
    time_var.set('Time left: {} min, {} sec'.format(minutesLeft, secondsLeft))
    if time_to_solve == 0:
        location_var.set('You\'ve run out of time!')
        accuse_btn.grid_remove()
        ask_zophie_btn.grid_remove()
        back_btn.grid_remove()
        lower_btn.grid_remove()
        locations_tree.grid_remove()
        ask_item_list.grid_remove()
        culpritIndex = SUSPECTS.index(culprit)
        stuff_var.set('It was {} at the {} with the {} who catnapped her!'.format(culprit, PLACES[culpritIndex], ITEMS[culpritIndex]))
        clue_lbl.grid()
        clue_var.set('Better luck next time, Detective.')
    else:
        if not game_over:
            root.after(1000, update_time)

def taxi():
    location_var.set('You are in your TAXI.')
    stuff_var.set('Where do you want to go?')
    for item in locations_tree.get_children():
        locations_tree.delete(item)
    for place in sorted(PLACES):
        placeInfo = ''
        if place in visitedPlaces:
            placeInfo = visitedPlaces[place]
        locations_tree.insert('', 'end', text=place, values=placeInfo, iid=place)
    clue_lbl.grid_remove()
    ask_item_list.grid_remove()
    accuse_btn.grid_remove()
    ask_zophie_btn.grid_remove()
    back_btn.grid_remove()
    locations_tree.grid()
    lower_btn_var.set('Go')
    lower_btn['command'] = go_place

def go_place():
    global thePersonHere, theItemHere
    currentLocation = locations_tree.focus()
    currentLocationIndex = PLACES.index(currentLocation)
    # At a place; player can ask for clues.
    location_var.set(' You are at the {}.'.format(currentLocation))
    currentLocationIndex = PLACES.index(currentLocation)
    thePersonHere = SUSPECTS[currentLocationIndex]
    theItemHere = ITEMS[currentLocationIndex]
    stuff_var.set('{} with the {} is here.'.format(thePersonHere, theItemHere))
    # Add the suspect and item at this place to our list of known
    # suspects and items:
    if thePersonHere not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(thePersonHere)
        ask_item_list.insert('end', thePersonHere)
    if ITEMS[currentLocationIndex] not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(ITEMS[currentLocationIndex])
        ask_item_list.insert('end', theItemHere)
    if currentLocation not in visitedPlaces.keys():
        visitedPlaces[currentLocation] = (thePersonHere.lower(), theItemHere.lower())

    # If the player has accused this person wrongly before, they
    # won't give clues:
    if thePersonHere in accusedSuspects:
        ask_item_list.grid_remove()
        ask_zophie_btn.grid_remove()
        accuse_btn.grid_remove()
        back_btn.grid_remove()
        clue_lbl.grid()
        locations_tree.grid_remove()
        clue_var.set('They are offended that you accused them,\nand will not help with your investigation.')
        lower_btn_var.set('Go back to TAXI')
        lower_btn['command'] = taxi
    else:
        ask_item_list.grid()
        ask_zophie_btn.grid()
        accuse_btn.grid()
        back_btn.grid()
        clue_lbl.grid_remove()
        locations_tree.grid_remove()
        lower_btn_var.set('Ask about suspect/item')
        lower_btn['command'] = ask_item

def accuse():
    global accusationsLeft, game_over
    accusationsLeft -= 1  # Use up an accusation.
    if thePersonHere == culprit:
        accuse_btn.grid_remove()
        ask_zophie_btn.grid_remove()
        back_btn.grid_remove()
        lower_btn.grid_remove()
        locations_tree.grid_remove()
        ask_item_list.grid_remove()
        clue_lbl.grid()
        stuff_var.set(f'You accused {thePersonHere}.')
        # You've accused the correct suspect.
        minutesTaken = int(300 - time_to_solve) // 60
        secondsTaken = int(300 - time_to_solve) % 60
        clue_var.set('You\'ve cracked the case, Detective!\nIt was {} who had catnapped ZOPHIE THE CAT.\nGood job! You solved it in {} min, {} sec.'.format(culprit, minutesTaken, secondsTaken))
    else:
        accusations_var.set(f'Accusations left: {accusationsLeft}')
        if accusationsLeft == 0:
            game_over = True
            location_var.set('You\'ve accused too many innocent people!')
            accuse_btn.grid_remove()
            ask_zophie_btn.grid_remove()
            back_btn.grid_remove()
            lower_btn.grid_remove()
            locations_tree.grid_remove()
            ask_item_list.grid_remove()
            culpritIndex = SUSPECTS.index(culprit)
            stuff_var.set('It was {} at the {} with the {} who catnapped her!'.format(culprit, PLACES[culpritIndex], ITEMS[culpritIndex]))
            clue_lbl.grid()
            clue_var.set('Better luck next time, Detective.')
        else:
            ask_item_list.grid_remove()
            ask_zophie_btn.grid_remove()
            accuse_btn.grid_remove()
            back_btn.grid_remove()
            clue_lbl.grid()
            locations_tree.grid_remove()
            accusedSuspects.append(thePersonHere)
            stuff_var.set(f'You accused {thePersonHere}.')
            clue_var.set('You have accused the wrong person, Detective!\nThey will not help you with anymore clues.')
            lower_btn_var.set('Go back to TAXI')
            lower_btn['command'] = taxi

def ask_zophie():
    ask_item_list.grid_remove()
    ask_zophie_btn.grid_remove()
    accuse_btn.grid_remove()
    back_btn.grid_remove()
    clue_lbl.grid()
    stuff_var.set(f'You asked {thePersonHere} if they knew where ZOPHIE THE CAT is.')
    locations_tree.grid_remove()
    if thePersonHere not in zophieClues:
        clue_var.set('They don\'t know anything about ZOPHIE THE CAT.')
    elif thePersonHere in zophieClues:
        clue_var.set('They give you this clue: "{}"'.format(zophieClues[thePersonHere]))
        # Add non-place clues to the list of known things:
        if zophieClues[thePersonHere] not in knownSuspectsAndItems and zophieClues[thePersonHere] not in PLACES:
            knownSuspectsAndItems.append(zophieClues[thePersonHere])
    lower_btn_var.set('Continue')
    lower_btn['command'] = go_place

def ask_item():
    thingBeingAskedAbout = ask_item_list.curselection()[0]
    thingBeingAskedAbout = knownSuspectsAndItems[thingBeingAskedAbout]
    if not bool(thingBeingAskedAbout):
        go_place()
        return
    ask_item_list.grid_remove()
    ask_zophie_btn.grid_remove()
    accuse_btn.grid_remove()
    back_btn.grid_remove()
    clue_lbl.grid()
    locations_tree.grid_remove()
    if thingBeingAskedAbout in (thePersonHere, theItemHere):
        clue_var.set('They give you this clue: "No comment."')
    else:
        clue_var.set('They give you this clue: "{}"'.format(clues[thePersonHere][thingBeingAskedAbout]))
        if clues[thePersonHere][thingBeingAskedAbout] not in knownSuspectsAndItems and clues[thePersonHere][thingBeingAskedAbout] not in PLACES:
            knownSuspectsAndItems.append(clues[thePersonHere][thingBeingAskedAbout])
    lower_btn_var.set('Continue')
    lower_btn['command'] = go_place

def start():
    root.after(1000, update_time)
    time_var.set('Time left: 5 min, 0 sec')
    accusations_var.set('Accusations left: 3')
    taxi()

# START OF THE GAME
root = Tk()
time_var = StringVar(value='J\'accuse! (a mystery game)')
accusations_var = StringVar()
Label(root, textvariable=time_var).grid(column=0, row=0)
Label(root, textvariable=accusations_var).grid(column=0, row=1)
location_var = StringVar(value="Based on Al Sweigart's J'accuse!, which is inspired by Homestar Runner's \"Where's An Egg?\" game")
stuff_var = StringVar()
Label(root, textvariable=location_var).grid(column=0, row=2)
Label(root, textvariable=stuff_var).grid(column=0, row=3)

clue_var = StringVar(value="""You are the world-famous detective, Mathilde Camus.
ZOPHIE THE CAT has gone missing, and you must sift through the clues.
Suspects either always tell lies, or always tell the truth. Ask them
about other people, places, and items to see if the details they give are
truthful and consistent with your observations. Then you will know if
their clue about ZOPHIE THE CAT is true or not. Will you find ZOPHIE THE
CAT in time and accuse the guilty party?""")
root.title("J'accuse!")
clue_lbl = Label(textvariable=clue_var)
clue_lbl.grid(column=0, row=4, columnspan=3)
accuse_btn = Button(text='J\'accuse!', command=accuse)
ask_zophie_btn = Button(text='Ask if they know where ZOPHIE THE CAT is.', command=ask_zophie)
back_btn = Button(text='Go back to the TAXI.', command=taxi)
accuse_btn.grid(column=0, row=4); accuse_btn.grid_remove()
ask_zophie_btn.grid(column=0, row=5); ask_zophie_btn.grid_remove()
back_btn.grid(column=0, row=6); back_btn.grid_remove()
locations_tree = Treeview(root, columns=('Person here', 'Item here'))
for i in ('Person here', 'Item here'):
    locations_tree.column(i)
    locations_tree.heading(i, text=i)
locations_tree.grid(column=0, row=7); locations_tree.grid_remove()
ask_item_list = Listbox(root, height=18)
ask_item_list.grid(column=0, row=7); ask_item_list.grid_remove()
lower_btn_var = StringVar(value='Start')
lower_btn = Button(root, textvariable=lower_btn_var, command=start)
lower_btn.grid(column=0, row=8)
root.mainloop()