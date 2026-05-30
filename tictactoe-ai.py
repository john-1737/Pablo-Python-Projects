from tkinter import Tk, Toplevel, Radiobutton, Label, ttk, Scale, Spinbox, StringVar, Button, Listbox, IntVar, Scrollbar
from tkinter.ttk import Combobox, Progressbar
from tictactoe2 import main

def simulate():
    simulations = sims.get()
    xm = xmove.get()
    if xm == 'custom':
        xm = resultx
    om = omove.get()
    if om == 'custom':
        om = resulto
    lbox.delete('0', 'end')
    left.grid()
    pbar.grid()
    left.config(text='0%% complete')
    pbar.config(maximum=100, value=0)
    xwins = 0
    owins = 0
    ties = 0
    for i in range(simulations):
        win = main(xm, om)
        if win.startswith('X wins'):
            xwins += 1
        elif win.startswith('O wins'):
            owins += 1
        elif win.startswith('Tie'):
            ties += 1
        lbox.insert('end', str(i+1) + ': ' + win)
        pbar.config(value=round(((i + 1)/simulations) * 100))
        left.config(text=f'{i+1} simulations done, {simulations-(i+1)} left, {round(((i + 1)/simulations) * 100)}% complete')
        root.update()
    left.config(text=f'X wins: {xwins}, O wins: {owins}, Ties: {ties}\nX wins: {round(((xwins)/simulations) * 100)}%, O wins: {round(((owins)/simulations) * 100)}%, Ties: {round(((ties)/simulations) * 100)}%')
    pbar.grid_remove()

def custom_move(player):
    global moves_var, win
    win = Toplevel(root)
    win.title('Custom Move')
    vars = [StringVar() for i in range(5)]
    for i, k in enumerate(vars):
        Label(win, text=f'Move {i+1}').grid(column=i, row=0)
        for j, l in enumerate(('Winning', 'Blocking', 'Corner', 'Center', 'Side'), start=1):
            move_letters = {'Winning': 'w', 'Blocking': 'b', 'Corner': 'c', 'Center': 'm', 'Side': 's'}
            Radiobutton(win, text=l, value=move_letters[l], variable=k).grid(column=i, row=j)
    Label(win, text='Moves:').grid(column=0, row=6)
    moves_var = IntVar()
    Scale(win, from_=1, to=5, variable=moves_var, orient='horizontal').grid(column=1, row=6, columnspan=2)
    Button(win, text='OK').grid(column=3, row=6, columnspan=2)

root = Tk()
xmove = StringVar(value='wbcms')
omove = StringVar(value='wbcms')
for i, j in enumerate(('Best move', 'Corner move', 'Side move', 'Center move', 'Random move')):
    move_structures = {'Best move': 'wbmcs', 'Corner move': 'c', 'Center move': 'm', 'Side move': 's', 'Random move': ' '}
    Radiobutton(root, text=j, value=move_structures[j], variable=xmove).grid(column=0, row=i)
    Radiobutton(root, text=j, value=move_structures[j], variable=omove).grid(column=1, row=i)

Radiobutton(root, text='Custom Algorithm', value='custom', variable=xmove, command=lambda:custom_move('x')).grid(column=0, row=6)
Radiobutton(root, text='Custom Algorithm', value='custom', variable=omove, command=lambda:custom_move('o')).grid(column=1, row=6)

sims = IntVar()
Label(root, text='Simulations: ').grid(column=0, row=8)
Spinbox(root, textvariable=sims, from_=1, to=10000000).grid(column=1, row=8)
Button(root, text='Run Simulations', command=simulate).grid(column=0, row=9, columnspan=2)
left = Label(root, text='0%% complete')
left.grid(column=0, row=10, columnspan=2); left.grid_remove()
pbar = Progressbar(root, orient='horizontal', mode='determinate', length=309)
pbar.grid(column=0, row=11, columnspan=2); pbar.grid_remove()

lbox = Listbox(root)
lbox.grid(column=0, row=12, columnspan=2)
sbar = Scrollbar(root, orient='vertical', command=lbox.yview)
sbar.grid(column=2, row=12, sticky = 'nsw')
lbox['yscrollcommand'] = sbar.set

root.mainloop()