from tkinter import simpledialog as sd
from tkinter import Tk, Label, StringVar

def format_number(num):
    #Converts int to list, and reverses it
    num = str(num)[::-1]
    nums = [str(num[i:i+3]) for i in range(0, len(num), 3)]
    nums = nums[::-1]
    nums = [i[::-1] for i in nums]
    return ','.join(nums)

#display_num = StringVar()

def add_format(num1, num2):
    num1, num2 = format_number(num1), format_number(num2)
    w = max(len(num1), len(num2))
    print(f' {num1:>{w}}')
    print(f'+{num2:>{w}}')
    print('-' * (w+1))

num1,num2= '1234217' , '875624'
numstr = ''
w = max(len(num1), len(num2))
print(str(format_number('10000000000000000000000000000000000000000000000000000000000000000003')))
add_format(num1, num2)
input()
print('',format_number(int(num1) + int(num2)))