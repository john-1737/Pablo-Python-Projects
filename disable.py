import time, sys
print('This program disables your terminal forever.\nYou cannot enable it again, even with Control-C.')
while True:
    prompt = input('Enter \'y\' to start or \'n\' to exit.\n')
    if prompt == 'n':
        sys.exit()
    elif prompt == 'y':
        break
for i in range(5, 0, -1):
    print('\n' * 100)
    print(f'You can press Control-C within {i} seconds.')
    time.sleep(1)
while True:
    try:
        print('\n' * 100)
        print('Terminal disabled.')
    except:
        print('\n' * 100)
        print('Terminal disabled.')