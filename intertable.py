from tkinter import Tk, messagebox
from tkmacosx import Button

show_sq = False
show_sq_dif = False

def read_file():
    global hints
    with open('multiplication_hints.txt') as f:
        hints = {}
        for i in f.readlines():
            k, v = i.split(':')
            hints[k] = v.strip('\n')

def get_hint(x, y):
    pos = [x, y]
    pos.sort()
    hint = hints.get(f'{pos[0]}*{pos[1]}', 'There is no hint for this multiplication fact.')
    messagebox.showinfo(message=hint)

def toggle_squares():
    global show_sq
    show_sq = not show_sq
    for i in range(1, 11):
        if show_sq == True:
            buttons[i, i].config(bg='yellow')
        else:
            buttons[i, i].config(bg='white')
    if show_sq == True:
        buttons['show squares'].config(text='Hide Perfect Squares')
    else:
        buttons['show squares'].config(text='Show Perfect Squares')

def toggle_square_diffs():
    global show_sq_dif
    show_sq_dif = not show_sq_dif
    for i in range(1, 10):
        if show_sq_dif == True:
            buttons[i+1, i-1].config(bg='green yellow')
            buttons[i-1, i+1].config(bg='green yellow')    
        else:
            buttons[i+1, i-1].config(bg='white')
            buttons[i-1, i+1].config(bg='white')
    buttons[0, 2].config(bg='green')
    buttons[2, 0].config(bg='green')                      
    if show_sq_dif == True:
        buttons['show square diffs'].config(text='Hide Difference Of Squares')
    else:
        buttons['show square diffs'].config(text='Show Difference Of Squares')

def main():
    global buttons
    buttons = {}
    read_file()
    root = Tk()
    root.title('Interactive table')
    for i in range(0, 11):
        for j in range(0, 11):
            if i == 0 or j == 0:
                if i == 0 and j == 0:
                    b = Button(root, width=50, height=50, bg='green', text='×', command=lambda i=i, j=j: get_hint(i, j))
                else:
                    pos = [i, j]
                    pos.sort()
                    b = Button(root, width=50, height=50, background='green', text=pos[1], command=lambda i=i, j=j : get_hint(i, j))
            else:
                b = Button(root, width=50, height=50, background='white', text=i*j, command=lambda i=i, j=j : get_hint(i, j))
            b.grid(column=i, row=j)
            buttons[i, j] = b
    b = Button(root, text='Show Perfect Squares', command=toggle_squares)
    b.grid(column=0, row=12, columnspan=5)
    buttons['show squares'] = b
    b = Button(root, text='Show Difference Of Squares', command=toggle_square_diffs)
    b.grid(column=6, row=12, columnspan=5)
    buttons['show square diffs'] = b
    root.mainloop()
if  __name__ == '__main__':
    main()