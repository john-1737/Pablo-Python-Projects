import random as r
import time as c
import tkinter as t
import math as m
from tkinter import messagebox as b

hint = {2: 'Anything times 2 is the same as anything plus itself. For example, 11 × 2 is equal to 11 + 11, which is 22.',
        }

answer = None

class equation:
    def __init__(self, root, eqlabel):
        """Initialize the class"""
        self.a = r.randint(1, 9)
        self.b = r.randint(1, 9)
        self.answer = self.a*self.b
        self.eqlabel = eqlabel
        self.root = root

    def show(self):
        self.eqlabel.config(text=f'{self.a} × {self.b} = ')

def submit(*a):
    global continue_
    continue_ = True        

        
root = t.Tk()
eqlabel = t.Label(root)
eqlabel.grid(column=0, row=0)
t.Button(root, text='Submit', command=submit).grid(column=0, row=1)
answer_var = t.IntVar()
answer_e = t.Entry(root, textvariable=answer_var)
answer_e.grid(column=1, row=0)
answer_e.bind('<Key-Return>', submit)
equations = []
for i in range(10):
    equations.append(equation(root, eqlabel))
corrects = 0
times = []
for i in equations:
    continue_ = False
    start_time = m.floor(c.time())
    while not continue_:
        i.show()
        root.update()
    if answer_var.get() == i.answer:
        end_time = m.floor(c.time())
        min, sec = divmod(end_time - start_time, 60)
        b.showinfo(message=f'Answer is correct.\nSolving time : {min}:{sec}')
        times.append(end_time - start_time)
        corrects += 1
    else:
        b.showinfo(message=f'Answer is incorrect.\nCorrect anwer : {i.answer}')
    answer_var.set(0)
b.showinfo(message=f'You got {corrects} out of 10 correct answers.')
av_time = m.floor(sum(times) / corrects)
b.showinfo(message=f'Your average time was {divmod(av_time, 60)}')