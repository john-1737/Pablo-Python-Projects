from random import randrange
from sys import exit
while True:
    print('''Lots Of Dice
Rolls dice lots of times.
Press Control-C at any time to quit.''')
    while True:
        sides = (input('How many sides?\n'))
        if not sides.isdigit():
            print('Must be an integer')
        elif int(sides) < 1:
            print('Must be above 1')
        else:
            sides = int(sides)
            break
    while True:
        times = (input('How many times?\n'))
        if not times.isdigit():
            print('Must be an integer')
        elif int(times) < 1:
            print('Must be above 1')
        else:
            times = int(times)
            break
    dice = []
    try:
        for i in range(times):
            dice.append(str(randrange(sides) + 1))
            print(f'{i + 1} dice done ({times - (i + 1)} left)', end=' ')
            percent= ((i) / times) * 100
            print(f'{percent}% done')
    except KeyboardInterrupt:
        print(f'{len(dice)} dice rolled.')
    print('The dice were:')
    print(', '.join(dice))
    if not input('Press Enter to continue or press another key to exit. ') == '':
        break