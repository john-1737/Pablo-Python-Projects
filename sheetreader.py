from tkinter import *
from tkinter import ttk, filedialog
from tkinter.ttk import Treeview, Notebook
file = ''

def csv_to_tree(txt):
    global rows
    rows = txt.splitlines()
    rows = [i.split(',') for i in rows]
    del rows[0][0]
    tree['columns'] = rows[0]
    for i in rows[0]:
        tree.column(i)
        tree.heading(i, text=i)
    for i in rows:
        tree.insert('', 'end', text=i[0], values=i[1:])
    text.insert('1.0', txt)
def open_file():
    global file
    with open(filedialog.askopenfilename()) as f:
        file = f.read()
        csv_to_tree(file)
root = Tk()
n = ttk.Notebook(root)
n.pack()
n.bind('<<NotebookTabChanged>>', lambda e: csv_to_tree(text.get('1.0', 'end')))
sheet_frame = Frame(n)
n.add(sheet_frame, text='Spreadsheet')
tree = ttk.Treeview(sheet_frame)
tree.grid(column=1, row=1, columnspan=2)
Button(sheet_frame, text='Open File', command=open_file).grid(column=1, row=0)
#All code below is for CSV frame
csv_frame = Frame(n)
n.add(csv_frame, text='CSV')
text = Text(csv_frame, state='normal')
text.grid(column=1, row=1, columnspan=2)
root.mainloop()