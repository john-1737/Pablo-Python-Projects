"""Progress Bar Simulation, by Al Sweigart al@inventwithpython.com
A sample progress bar animation that can be used in other programs.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, module"""

import random, time
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Progressbar, Label

BAR = chr(9608) # Character 9608 is '█'

def main():
    global bytesDownloaded, downloadSize, b, info, root
    root = Tk()
    root.title('Progress Bar Simulation')
    f = Frame(root)
    f.grid(sticky='nwes')
    b = Progressbar(f, orient='horizontal', mode='determinate')
    b.grid(column=0, row=0)
    info = StringVar()
    Label(f, textvariable=info).grid(column=1, row=0)
    bytesDownloaded = 0
    downloadSize = 4096
    root.after(200, update)
    root.mainloop()

def update():
    global bytesDownloaded
    if bytesDownloaded >= downloadSize:
        root.destroy()
        exit()

    # "Download" a random amount of "bytes":
    bytesDownloaded += random.randint(0, 100)

    # Get the progress bar string for this amount of progress:
    getProgressBar(bytesDownloaded, downloadSize)

    root.after(200, update)

def getProgressBar(progress, total):
    """Returns a string that represents a progress bar that has barWidth
    bars and has progressed progress amount out of a total amount."""

    progressBar = ''  # The progress bar will be a string value.
    progressBar += '['  # Create the left end of the progress bar.

    # Make sure that the amount of progress is between 0 and total:
    if progress > total:
        progress = total
    if progress < 0:
        progress = 0

    # Calculate the number of "bars" to display:
    numberOfBars = int((progress / total) * 100)

    b.config(value=numberOfBars)

    # Calculate the percentage complete:
    percentComplete = round(progress / total * 100, 1)
    info.set(str(percentComplete) + '% ' + str(progress) + '/' + str(total))

# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
