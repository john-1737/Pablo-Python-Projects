import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import idepkg as id

def launch():
    try:
        exec(inp.get(1.0, 'end'))
    except Exception as e:
        messagebox.showinfo(message=f'{type(e).__name__}: {str(e)}', icon='warning')

def launch_file():
    name=filedialog.askopenfilename()
    if name == '':
        return
    with open(name) as f:
        text = f.read()
    try:
        exec(text)
    except Exception as e:
        messagebox.showinfo(message=f'{type(e).__name__}: {str(e)}', icon='warning')
        
def print(*values, sep=' ', end='\n', file='', flush=False):
    output['state'] = 'normal'
    output.insert('end', sep.join(values) + end)
    output['state'] = 'disabled'

def input(prompt=''):
    inp_var = ''
    print(prompt, end='')
    print('<Cannot support input in editor>')
    '''output['state'] = 'normal'
    output.bind('<Return>', lambda evt: id.calc_return(prompt, output, inp_var))'''
    return inp_var

root = tk.Tk()
root.title('Editor')
root.option_add('*tearoff', tk.FALSE)
win = tk.Toplevel(root)
win.withdraw()
menubar = tk.Menu(win)
win['menu'] = menubar
menu_file = tk.Menu(menubar)
menu_file.add_command(label='Create', command=lambda: inp.delete(1.0, 'end'), accelerator='Command-N')
menu_file.add_command(label='Open', command=lambda:id.open_file(inp), accelerator='Command-O')
menu_file.add_command(label='Save', command=lambda:id.save_file(inp), accelerator='Command-S')
menubar.add_cascade(menu=menu_file, label='File')
menu_edit = tk.Menu(menubar)
menu_edit.add_command(label='Cut', command=lambda:root.focus_get().event_generate('<<Cut>>'), accelerator='Command-X')
menu_edit.add_command(label='Copy', command=lambda:root.focus_get().event_generate('<<Copy>>'), accelerator='Command-C')
menu_edit.add_command(label='Paste', command=lambda:root.focus_get().event_generate('<<Paste>>'), accelerator='Command-V')
menu_edit.add_command(label='Undo', command=lambda:root.focus_get().event_generate('<<Undo>>'), accelerator='Command-Z')
menu_edit.add_command(label='Redo', command=lambda:root.focus_get().event_generate('<<Redo>>'), accelerator='Shift-Command-Z')
menubar.add_cascade(menu=menu_edit, label='Edit')
menu_run = tk.Menu(menubar)
menu_run.add_command(label='Run', command=launch)
menu_run.add_command(label='Run File', command=launch_file)
menubar.add_cascade(menu=menu_run, label='Run')
n = ttk.Notebook(root)
editor = ttk.Frame(root)
shell = ttk.Frame(root)
n.add(editor, text='Editor')
n.add(shell, text='Python Shell')
n.pack()
tk.Button(editor, text='+ Create', command=lambda: inp.delete(1.0, 'end')).grid(column=0, row=0)
tk.Button(editor, text='⇧ Open', command=lambda:id.open_file(inp)).grid(column=1, row=0)
tk.Button(editor, text='⇩ Save', command=lambda:id.save_file(inp)).grid(column=2, row=0)
tk.Button(editor, text='⏵ Run', command=launch).grid(column=3, row=0)
tk.Button(editor, text='⏵ Run File', command=launch_file).grid(column=4, row=0)
inp = tk.Text(editor, width=40, height=50, wrap='none')
inp.grid(column=0, row=1, columnspan=3)
inp_yscroller = tk.Scrollbar(editor, command=inp.xview, orient='horizontal', bg='black')
inp_yscroller.grid(column=0, row=2, sticky='ew', columnspan=3)
inp.config(yscrollcommand = inp_yscroller.set)
output = tk.Text(editor, width=40, height=50, state='disabled')
output.grid(column=3, row=1, columnspan=3)

tk.Label(root, text='Enter commands for terminal').pack()
terminal_var = tk.StringVar()
terminal_entry = tk.Entry(root, textvariable=terminal_var, width=60)
terminal_entry.pack()
terminal_entry.bind('<Return>', lambda evt:id.run_terminal(terminal_var, terminal_entry))

shell_entry = tk.Text(shell, width=80, height=50, bg='black', fg='lightgreen')
shell_entry.pack()
shell_entry.tag_configure('prompt', foreground='magenta')
shell_entry.tag_configure('output', foreground='yellow')
shell_entry.insert('end', '>>> ', ('prompt',))
shell_entry.bind('<Return>', lambda e:id.on_return(shell_entry))

root.mainloop()