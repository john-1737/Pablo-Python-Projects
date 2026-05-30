"""Multiplication Table, by Al Sweigart al@inventwithpython.com
Print a multiplication table.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, math"""

from tkinter import Tk
from tkinter.ttk import Frame, Label, Separator
from tkinter.font import Font, nametofont

root = Tk()
root.title('Multiplication Table')

f = Frame(root)
f.grid(sticky='nwes')

font_dict = nametofont('TkDefaultFont').actual()
font_dict['weight'] = 'bold'
bold_font = Font(**font_dict)

for i in range(13):
    Label(f, text=i, font=bold_font).grid(column=i+2, row=0)

# Display each row of products:
for number1 in range(0, 13):

    # Print the vertical numbers labels:
    Label(f, text=str(number1), font=bold_font).grid(column=0, row=number1+2)

    for number2 in range(0, 13):
        # Print the product followed by a space:
        Label(f, text=str(number1 * number2)).grid(column=number1+2, row=number2+2)

Separator(f, orient='horizontal').grid(column=0, row=1, columnspan=15, sticky='ew')
Separator(f, orient='vertical').grid(column=1, row=0, rowspan=15, sticky='ns')

root.mainloop()
