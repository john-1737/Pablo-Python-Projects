import tkinter as tk
from tkinter import ttk, filedialog
import os

def print(*args, sep=' ', **kargs):
    return sep.join(args)

def run_terminal(terminal_var, terminal_entry):
    os.system(terminal_var.get())
    terminal_entry.delete(0, 'end')

def ask_open_file(inp):
    filename = filedialog.askopenfilename()
    open_file(inp, filename)

def open_file(inp, filename):
    if filename == '':
        return
    with open(filename, encoding='utf-8') as f:
        inp.delete(1.0, 'end')
        inp.insert(1.0, f.read())

def save_file(inp):
    filename = filedialog.asksaveasfilename()
    if filename == '':
        return
    with open(filename, 'w') as f:
        f.write(inp.get(1.0, 'end'))

def on_return(text):
    cmd = text.get('prompt.last', 'end').strip()
    if cmd:
        try:
            output = str(eval(cmd))
        except Exception as e:
            output = str(e)
        text.insert('end', '\n' + output, ('output',))
    text.insert('end', '\n>>> ', ('prompt',))
    return'break'

def calc_return(prompt, text):
    global output
    text['state'] = 'disabled'
    text.unbind('<Return>')
    text_ls = list(text.get(1.0, 'end').splitlines().pop())
    text = str(text_ls)
    out = text

