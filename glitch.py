from random import choice
from sys import exit
from time import sleep
print('''Glitch
Produces an infinitely long glitch.''')
if input('''Glitch screen now?
Enter 'y' for yes and anything else for no.
''') != 'y':
    exit()
while True:
    try:
        print(choice(list('1234567890')), end='')
    except KeyboardInterrupt:
        print(choice(list('1234567890')), end='')    
