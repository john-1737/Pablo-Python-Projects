"""Powerball Lottery, by Al Sweigart al@inventwithpython.com
A simulation of the lottery so you can experience the thrill of
losing the lottery without wasting your money.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, humor, simulation"""

import random
from tkinter import Tk, StringVar, Text, Toplevel
from tkinter.ttk import Frame, Label, Button, Entry, Spinbox, Scrollbar, Notebook

def help():
    win = Toplevel(root)
    win.title('Help')
    n = Notebook(win)
    n.grid(sticky='nwes')

    n.add(Label(n, text='''Welcome to Powerball Lottery!
Each powerball lottery ticket costs $2. The jackpot for this game
is $1.586 billion! It doesn't matter what the jackpot is, though,
because the odds are 1 in 292,201,338, so you won't win.

This simulation gives you the thrill of playing without wasting money.
          
This program is inspired by Al Sweigart's Powerball Lottery.'''), text='About')
    
    n.add(Label(n, text='''To enter the lottery, you first must write
your numbers. To start, enter 5 different numbers between 1 to 69 that are
all different. For example, 5 17 23 42 50 is valid, but 5 42 23 42 50 is
not (because it contains duplicates). 5 79 23 42 50 is also not valid
(because some of the numbers are greater than 69.), Next, enter a powerball
number from 1 to 26. For example, 18 is valid, but 33 is not (because it
is greater than 26). Finally, enter the number of times you want to play.
Each time you play costs $2. (Not in real money, though.) You can play
between 1 and 1,000,000 times.

To win, the 5 numbers must match the 5 lottery numbers in any order, and
the powerball number must match the lottery powerball number.
                
This simulation does not allow users to win or lose money.'''), text='How to play')
    
    n.add(Label(n, text='''In the entry screen, press the Start button to start the simulation. You
cannot press the Start button if there is an error in your selected numbers.

In the simulation screen, press the Stop button to stop the simulation
immediately.
                
In any screen, press the Help button to go to the help menu.'''), text='Controls')

def play():
    entry_frame.grid_remove()
    sim_frame.grid()
    wasted_var.set('You have wasted $0')
    for i in (lost, winning_numbers):
        i['state'] = 'normal'
        i.delete('1.0', 'end')
        i['state'] = 'disabled'
    numPlays = int(plays_var.get())
    numbers = [int(i.get()) for i in number_vars]
    powerball = powerball_var.get()
    possibleNumbers = list(range(1, 70))
    for i in range(numPlays):
        try:
            if not sim_frame.grid_info():
                break
        except:
            break
        # Come up with lottery numbers:
        random.shuffle(possibleNumbers)
        winningNumbers = possibleNumbers[0:5]
        winningPowerball = random.randint(1, 26)

        # Display winning numbers:
        winning_numbers['state'] = 'normal'
        winning_numbers.insert('end', 'The winning numbers are: ')
        allWinningNums = ''
        for j in range(5):
            allWinningNums += str(winningNumbers[j]) + ' '
        allWinningNums += 'and ' + str(winningPowerball)
        winning_numbers.insert('end', allWinningNums + '\n')
        winning_numbers['state'] = 'disabled'

        # NOTE: Sets are not ordered, so it doesn't matter what order the
        # integers in set(numbers) and set(winningNumbers) are.
        if (set(numbers) == set(winningNumbers)
            and powerball == winningPowerball):
                winning_numbers['state'] = 'normal'
                winning_numbers.insert('end', '\nYou have won the Powerball Lottery! Congratulations,\nyou would be a billionaire if this was real!')
                winning_numbers['state'] = 'disabled'
                break
        else:
            lost['state'] = 'normal'
            lost.insert('end', 'You lost.\n')
            lost['state'] = 'disabled'  # The leading space is required here.

        wasted_var.set(f'You have wasted ${i*2+2}')
        lost.see('end-2c')
        winning_numbers.see('end-2c')
        root.update()

def check_variables(*args):
    numbers = []
    for i in range(5):
        numbers.append(number_vars[i].get())
    if '' in numbers:
        error1.set('Please enter 5 numbers.')
        start_button.state(['disabled'])
        return
    # Convert the strings into integers:
    try:
        for i in range(5):
            numbers[i] = int(numbers[i])
    except ValueError:
        error1.set('Please enter numbers, like 27, 35,\nor 62.')
        start_button.state(['disabled'])
        return

    # Check that the numbers are between 1 and 69:
    for i in range(5):
        if not (1 <= numbers[i] <= 69):
            error1.set('The numbers must all be between\n1 and 69.')
            start_button.state(['disabled'])
            return

    # Check that the numbers are unique:
    # (Create a set from number to remove duplicates.)
    if len(set(numbers)) != 5:
        error1.set('You must enter 5 different numbers.')
        start_button.state(['disabled'])
        return
    error1.set('')
    check_button()

def check_powerball(*args):
    response = powerball_var.get()
    try:
        powerball = int(response)
    except ValueError:
        error2.set('Please enter a number, like 3, 15, or\n22.')
        start_button.state(['disabled'])
        return

    # Check that the number is between 1 and 26:
    if not (1 <= powerball <= 26):
        error2.set('The powerball number must be\nbetween 1 and 26.')
        start_button.state(['disabled'])
        return
    error2.set('')
    check_button()

def check_button():
    if error1.get() == '' and error2.get() == '':
        start_button.state(['!disabled'])
    else:
        start_button.state(['disabled'])

def check_num_plays(*args):
    plays = plays_var.get()
    plays = list(plays)
    plays = [i for i in plays if i in '1234567890']
    if plays == []:
        plays = 1
    else:
        plays = str(int(''.join(plays)))
    if int(plays) > 1000000:
        plays = '1000000'
    elif int(plays) == 0:
        plays = 1
    plays_var.set(plays)
    stats_var.set(f'It costs ${2*int(plays)} to play {plays}\ntimes, but don\'t worry. I\'m sure you\'ll\nwin it all back.')

def see_texts(*args, **kwargs):
    winning_numbers.yview(*args, **kwargs)
    lost.yview(*args, **kwargs)

def stop():
    sim_frame.grid_remove()
    entry_frame.grid()

def quit():
    sim_frame.grid_remove()
    root.destroy()

root = Tk()
root.title('Powerball Lottery')
f = Frame(root)
f.grid(sticky='nwes')
entry_frame = Frame(f)
entry_frame.grid(column=0, row=0)
Label(entry_frame, text='Enter 5 different numbers from 1 to 69\nin the entry fields below.\n(For example: 5 17 23 42 50)').grid(column=0, row=0, columnspan=5)
number_vars = []
for i in range(5):
    s = StringVar()
    Entry(entry_frame, textvariable=s, width=2).grid(column=i, row=1)
    s.trace_add('write', check_variables)
    number_vars.append(s)
Label(entry_frame, text='Enter the powerball number from 1 to\n26 in the entry field below.').grid(column=0, row=3, columnspan=5)
powerball_var = StringVar()
powerball_var.trace_add('write', check_powerball)
Entry(entry_frame, textvariable=powerball_var, width=2).grid(column=0, row=4, columnspan=5)
error1 = StringVar(value='Please enter 5 numbers.')
Label(entry_frame, textvariable=error1, foreground='red').grid(column=0, row=2, columnspan=5)
error2 = StringVar(value='Please enter a number, like 3, 15, or\n22.')
Label(entry_frame, textvariable=error2, foreground='red').grid(column=0, row=5, columnspan=5)
Label(entry_frame, text='How many times do you want to play?\n(Max: 1000000)').grid(column=0, row=6, columnspan=5)
plays_var = StringVar(value=1)
plays_var.trace_add('write', check_num_plays)
Spinbox(entry_frame, textvariable=plays_var, width=7, from_=1, to=1000000, wrap=True).grid(column=0, row=7, columnspan=5)
stats_var = StringVar(value='It costs $2 to play 1\ntimes, but don\'t worry. I\'m sure you\'ll\nwin it all back.')
Label(entry_frame, textvariable=stats_var).grid(column=0, row=8, columnspan=5)
start_button = Button(entry_frame, text='Start', default='active', command=play)
start_button.grid(column=0, row=9, columnspan=5)
start_button.state(['disabled'])

sim_frame = Frame(f)
sim_frame.grid(column=0, row=0)
sim_frame.grid_remove()
winning_numbers = Text(sim_frame, width=46, font='TkTextFont', highlightthickness=0, state='disabled')
winning_numbers.grid(column=0, row=0)
lost = Text(sim_frame, width=9, font='TkTextFont', highlightthickness=0, state='disabled')
lost.grid(column=1, row=0)
s = Scrollbar(sim_frame, orient='vertical', command=see_texts)
winning_numbers['yscrollcommand'] = s.set
lost['yscrollcommand'] = s.set
s.grid(column=2, row=0, sticky='ns')
wasted_var = StringVar()
Label(sim_frame, textvariable=wasted_var).grid(column=0, row=1, columnspan=3)
Button(sim_frame, text='Stop', command=stop, default='active').grid(column=0, row=2, columnspan=3)
Button(f, text='Help', command=help).grid(column=0, row=1)
root.protocol('WM_DELETE_WINDOW', quit)
root.mainloop()