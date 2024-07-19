from random import *
while True:
    sides = int(input('To roll a die, enter the number of sides.\n'))
    print(f'You rolled a {(randrange(sides)) + 1}!')
    if input('Type "exit" to exit. Type anything else to roll another die.\n') == 'exit':
        break
