from tkinter import messagebox, simpledialog
import bouncegame
questions = {'What is Taylor Swift\'s favorite number?' : '13',
             "Which jewelry is commonly worn by Swifties?\nA = rings B = necklaces C = bracelets" : "C",
             "True or false : Taylor Swift's first album was Red." : 'F',
             "What is Taylor Swift's favorite color?\nA = red B = purple C = blue" : 'B',
             "When did Taylor Swift receive her first award?\nA = 2006 B = 2007 C = 2008" : 'B',
             'How old was Taylor Swift when she released her first album?' : '16',
             'How many cats does Taylor Swift have as of 2023?' : '3'}
def quiz():
    messagebox.showinfo(message='''It's time for a Taylor Swift quiz!\nHere are some instructions for the quiz:
On open-ended questions, type your answer.\nOn multiple-choice questions, type the letter of your choice.\nOn true or false questions, enter T for true and F for false.\nYou get one point per question. There are 7 questions.''')
    score = 0
    for x in questions:
        answerinput = simpledialog.askstring('Enter question', x)
        if answerinput.upper() == questions[x]:
            messagebox.showinfo(message='Correct!')
            score = score + 1
        else:
            messagebox.showinfo(message='Incorrect!')
            messagebox.showinfo(message=f'The correct answer was {questions[x]}')
            score = score - 1
        messagebox.showinfo(message=f'Current score : {score}')
    win = score * 10
    if score > 0:
        messagebox.showinfo(message=f'You won ${win}!')
    else:
        messagebox.showinfo(message=f'You lost ${-win}.')
    return win

def bounce():
    score = bouncegame.main() * 20
    messagebox.showinfo(message=f'You won ${score}!')
    return score