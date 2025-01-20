from shutil import get_terminal_size
while True:
    lines = int(input('How many lines?'))
    for i in range(lines):
        print(r'\\\\ ', end='')
    if not input('Press Enter to continue or press another key to exit. ') == '':
        break