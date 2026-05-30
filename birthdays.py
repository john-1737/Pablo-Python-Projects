"""Birthday Paradox Simulation, by Al Sweigart al@inventwithpython.com
Explore the surprising probabilities of the "Birthday Paradox".
More info at https://en.wikipedia.org/wiki/Birthday_problem
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, math, simulation"""

import datetime, random
from tkinter import Tk, StringVar, messagebox, Text, Toplevel
from tkinter.ttk import Label, Progressbar, Entry, Frame, Button
from tkinter.font import nametofont

def getBirthdays(numberOfBirthdays):
    """Returns a list of number random date objects for birthdays."""
    birthdays = []
    for i in range(numberOfBirthdays):
        # The year is unimportant for our simulation, as long as all
        # birthdays have the same year.
        startOfYear = datetime.date(2001, 1, 1)

        # Get a random day into the year:
        randomNumberOfDays = datetime.timedelta(random.randint(0, 364))
        birthday = startOfYear + randomNumberOfDays
        birthdays.append(birthday)
    return birthdays


def getMatch(birthdays):
    """Returns the date object of a birthday that occurs more than once
    in the birthdays list."""
    if len(birthdays) == len(set(birthdays)):
        return None  # All birthdays are unique, so return None.

    # Compare each birthday to every other birthday:
    for a, birthdayA in enumerate(birthdays):
        for b, birthdayB in enumerate(birthdays[a + 1 :]):
            if birthdayA == birthdayB:
                return birthdayA  # Return the matching birthday.
            
def show_frame(frame):
    for i in (continue_frame, loading_frame, probability_label):
        if i == frame:
            i.grid()
        else:
            i.grid_remove()

def obtain_birthdays():
    global num
    num = num_var.get()
    if not num.isdecimal():
        messagebox.showwarning(message='Please enter a number.')
        num_var.set('')
    if not (0 < int(num) <= 100):
        messagebox.showwarning(message='Please enter a number between 0 and 100.')
        num_var.set('')
    num = int(num)
    num_frame.grid_remove()
    sim_frame.grid()
    show_frame(continue_frame)
    continue_var.set(f'Press Continue to generate {num} random birthdays 100,000\ntimes.')
    birthday_info.set(f'Here are {num} birthdays:')
    birthdays = getBirthdays(num)
    birthdays_text.config(state='normal')
    for i, birthday in enumerate(birthdays):
        if i != 0:
            # Display a comma for each birthday after the first birthday.
            birthdays_text.insert('end', ', ')
        monthName = MONTHS[birthday.month - 1]
        dateText = '{} {}'.format(monthName, birthday.day)
        birthdays_text.insert('end', dateText)
    birthdays_text.config(state='disabled')
    # Determine if there are two birthdays that match.
    match = getMatch(birthdays)

    # Display the results:
    if match != None:
        monthName = MONTHS[match.month - 1]
        dateText = '{} {}'.format(monthName, match.day)
        match_var.set(f'In this simulation, multiple people have a birthday on {dateText}.')
    else:
        match_var.set('In this simulation, there are no matching birthdays.')
    

def run_100000_simulations():
    # Run through 100,000 simulations:
    show_frame(loading_frame)
    loading_var.set(f'Generating {num} random birthdays 100,000 times...\n0.0% done...')
    simMatch = 0  # How many simulations had matching birthdays in them.
    for i in range(100000):
        if not sim_frame.winfo_ismapped():
            break
        # Report on the progress every 10,000 simulations:
        if i % 100 == 0:
            loading_var.set(f'Generating {num} random birthdays 100,000 times...\n{round(i/1000, 1)}% done...')
            b.config(value=i/1000)
            root.update()
        birthdays = getBirthdays(num)
        if getMatch(birthdays) != None:
            simMatch = simMatch + 1

    # Display simulation results:
    show_frame(probability_label)
    probability = round(simMatch / 100000 * 100, 2)
    probability_label.config(text=f'''Out of 100,000 simulations of {num} people, there was a
matching birthday in that group {simMatch} times. This
means that {num} people have a {probability} % chance of
having a matching birthday in their group.
That\'s probably more than you would think!''')
    
def restart():
    sim_frame.grid_remove()
    num_frame.grid()
    
def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Birthday Paradox!

The birthday paradox shows us that in a group of N people, the odds
that two of them have matching birthdays is surprisingly large.
This program does a Monte Carlo simulation (that is, repeated random
simulations) to explore this concept.

(It's not actually a paradox, it's just a surprising result.)
        
This program is inspired by Al Sweigart's Birthday Paradox.''').grid()

# Set up a tuple of month names in order:
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

root = Tk()
root.title('Birthday Paradox')
f = Frame(root)
f.grid(sticky='nwes')
num_frame = Frame(f)
num_frame.grid(column=0, row=0)
num_var = StringVar()
Label(num_frame, text='How many birthdays shall I generate? (Max 100)').grid(column=0, row=0)
Entry(num_frame, textvariable=num_var).grid(column=0, row=1)
Button(num_frame, text='Submit', default='active', command=obtain_birthdays).grid(column=0, row=2)
sim_frame = Frame(f)
sim_frame.grid(column=0, row=0)
sim_frame.grid_remove()
birthday_info = StringVar()
Label(sim_frame, textvariable=birthday_info).grid(column=0, row=0)
birthdays_text = Text(sim_frame, font=nametofont('TkDefaultFont'), width=40, height=14, wrap='word', background='gray90', state='disabled')
birthdays_text.grid(column=0, row=1)
match_var = StringVar()
Label(sim_frame, textvariable=match_var).grid(column=0, row=2)
Button(sim_frame, text='Restart', command=restart).grid(column=0, row=4)
continue_frame = Frame(sim_frame)
continue_frame.grid(column=0, row=3)
continue_var = StringVar()
Label(continue_frame, textvariable=continue_var).grid(column=0, row=0)
Button(continue_frame, text='Continue', command=run_100000_simulations, default='active').grid(column=0, row=1)
loading_frame = Frame(sim_frame)
loading_var = StringVar()
Label(loading_frame, textvariable=loading_var).grid(column=0, row=0)
b = Progressbar(loading_frame, orient='horizontal')
b.grid(column=0, row=1)
loading_frame.grid(column=0, row=3)
probability_label = Label(sim_frame)
probability_label.grid(column=0, row=3)
Button(f, text='Help', command=help).grid(column=0, row=1)
root.mainloop()