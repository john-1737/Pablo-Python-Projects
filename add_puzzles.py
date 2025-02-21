from tkinter import messagebox as mb
from tkinter import simpledialog as sd

def check_equation(equation, key):
    if ('+' in equation or '-' in equation) and '=' in equation:
        pass
    else:
        mb.showwarning(message='Equation requires + or - and =')
        return False
    for i in list(equation):
        if i.isalpha() and i not in key:
            mb.showwarning(message='All letters in the equation must be in the key')
            return False
    return True    

equation = sd.askstring('Enter equation', 'Enter an equation').lower()

#Create the key
while True:
    key = {}
    for i in range(10):
        while True:
            key_letter = sd.askstring('Select key', f'Choose a letter for the number {i} or leave empty to skip')
            if key_letter not in ('', None):
                if key_letter in key:
                    mb.showwarning(message='This letter is already in the key.')
                else:
                    key[key_letter.lower()] = str(i)
                    break
            else:
                break

    if check_equation(equation, key):
        break

for i in list(equation):
    if i.isalpha() and i != ' ':
        equation = equation.replace(i, key[i])

problem, answer = equation.split('=')
if eval(problem) == int(answer):
    mb.showinfo(message='The selected key is a solution to the problem.')
else:
    mb.showinfo(message='The selected key is not a solution to the problem.')