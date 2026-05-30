"""Bitmap Message, by Al Sweigart al@inventwithpython.com
Displays a text message according to the provided bitmap image.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, artistic"""

import sys
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Button, Label, Entry

# (!) Try changing this multiline string to any image you like:

# There are 68 periods along the top and bottom of this string:
# (You can also copy and paste this string from
# https://inventwithpython.com/bitmapworld.txt)
bitmap = """
....................................................................
   **************   *  *** **  *      ******************************
  ********************* ** ** *  * ****************************** *
 **      *****************       ******************************
          *************          **  * **** ** ************** *
           *********            *******   **************** * *
            ********           ***************************  *
   *        * **** ***         *************** ******  ** *
               ****  *         ***************   *** ***  *
                 ******         *************    **   **  *
                 ********        *************    *  ** ***
                   ********         ********          * *** ****
                   *********         ******  *        **** ** * **
                   *********         ****** * *           *** *   *
                     ******          ***** **             *****   *
                     *****            **** *            ********
                    *****             ****              *********
                    ****              **                 *******   *
                    ***                                       *    *
                    **     *                    *
...................................................................."""

def draw_bitmap(*args):
    text = ''
    message = message_var.get()
    if message == '':
        message = ' '
    # Loop over each line in the bitmap:
    for line in bitmap.splitlines():
        # Loop over each character in the line:
        for i, bit in enumerate(line):
            if bit == ' ':
                # Print an empty space since there's a space in the bitmap:
                text += ' '
            else:
                # Print a character from the message:
                text += message[i % len(message)]
        text += '\n'  # Print a newline.
    bitmap_var.set(text)

root = Tk()
root.title('Bitmap Message')
f = Frame(root)
f.grid(sticky='nwes')
Label(root, text='Enter the message to display with the bitmap.').grid(column=0, row=0)
message_var = StringVar()
Entry(root, textvariable=message_var).grid(column=0, row=1)
bitmap_var = StringVar()
Label(root, textvariable=bitmap_var, font='TkFixedFont').grid(column=0, row=2)
draw_bitmap()
message_var.trace_add('write', draw_bitmap)
root.mainloop()