from tkinter import Tk, messagebox, StringVar, Toplevel, PhotoImage
from tkinter.ttk import Frame, Label, Entry, Button

def help():
    win = Toplevel(root)
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Collatz Tester!
This program tests large numbers to see if they all terminate at 1 
when using the Collatz Sequence.

The Collatz sequence is a sequence of numbers produced from a starting
number n, following three rules:

1) If n is even, the next number n is n / 2.
2) If n is odd, the next number n is n * 3 + 1.
3) If n is 1, stop. Otherwise, repeat.

It is generally thought, but so far not mathematically proven, that
every starting number eventually terminates at 1.''').grid()
    
def test():
    global response
    response = num.get()
    if not response.isdecimal() or response == '0':
        messagebox.showwarning(message='You must enter an integer greater than 0.')
        return
    b1.state(['disabled'])
    b2.state(['disabled'])
    result.set('Testing...')
    root.update()
    n = int(response)
    while n != 1:
        if n % 2 == 0:  # If n is even...
            n = n // 2
        else:  # Otherwise, n is odd...
            n = 3 * n + 1
    result.set('✅ Test Passed')
    b1.state(['!disabled'])
    b2.state(['!disabled'])
    root.update()

def test_all():
    global response
    response = num.get()
    if not response.isdecimal() or response == '0':
        messagebox.showwarning(message='You must enter an integer greater than 0.')
        return
    b1.state(['disabled'])
    b2.state(['disabled'])
    result.set('Testing...')
    root.update()
    number = int(response)
    for i in range(1, number+1):
        n = i
        while n != 1:
            if n % 2 == 0:  # If n is even...
                n = n // 2
            else:  # Otherwise, n is odd...
                n = 3 * n + 1
    result.set('✅ Test Passed')
    b1.state(['!disabled'])
    b2.state(['!disabled'])
    root.update()
    
root = Tk()
f = Frame(root)
f.grid(sticky='nsew')
root.title('Collatz Tester')
Label(f, text='Enter a number to test all numbers to\nor a single number to test:').grid(column=0, row=0)
num = StringVar()
Entry(f, textvariable=num).grid(column=0, row=1)
b1 = Button(f, text='Test Number', command=test)
b1.grid(column=0, row=2)
b2 = Button(f, text='Test All Numbers to Entered Number', command=test_all)
b2.grid(column=0, row=3)
result = StringVar()
Label(f, textvariable=result).grid(column=0, row=4)
Button(f, text='Help', command=help).grid(column=0, row=5)
root.mainloop()