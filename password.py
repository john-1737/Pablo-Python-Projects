from keybrgui import int_keyboard
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import time
from sys import exit
tries = 3
while True:
    for i in range(tries, -1, -1):
        password = int_keyboard(f'Enter password ({i} tries left)', 'Enter the password')
        if password == 2025:
            mb.showinfo(message='Correct')
            exit()
        elif not password:
            exit()
        #if i:
        #    mb.showinfo(message=f'Incorrect password ({i} tries left)')
    go = mb.askokcancel(message='Press OK to try again in 10 seconds.')
    if not go:
        break
    time.sleep(10)
