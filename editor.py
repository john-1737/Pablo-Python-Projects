import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import idepkg as id
from PIL import Image, ImageTk

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
    global out
    print(prompt, end='')
    out = ''
    output['state'] = 'normal'
    output.bind('<Return>', lambda evt: id.calc_return(prompt, output))
    return out

def setfolder():
    folder_name = filedialog.askdirectory()
    if folder_name == None:
        return
    folder.set(folder_name)
    files.set(os.listdir(folder.get()))

def configure_mode(darkmode):
    if darkmode:
        master.config(bg='black')
        editor.config(bg='black')
        shell.config(bg='black')
        inp.config(bg='black', fg='white')
        output.config(bg='black', fg='white')
        terminal_entry.config(bg='black', fg='white')
        entlbl.config(bg='black', fg='white')
        shell_entry.config(bg='black', fg='lightgreen')
        shell_entry.tag_configure('prompt', foreground='magenta')
        shell_entry.tag_configure('output', foreground='yellow')
    else:
        master.config(bg='systemWindowHeaderBackground')
        editor.config(background='systemWindowHeaderBackground')
        shell.config(background='systemWindowHeaderBackground')
        inp.config(bg='white', fg='black')
        output.config(bg='white', fg='black')
        terminal_entry.config(bg='white', fg='black')
        entlbl.config(bg='systemWindowHeaderBackground', fg='black')
        shell_entry.config(bg='white', fg='black')
        shell_entry.tag_configure('prompt', foreground='green')
        shell_entry.tag_configure('output', foreground='red')

def open_editdialog(filename, win):
    win.deiconify()
    if filename.endswith('.jpeg')\
    or filename.endswith('.png')\
    or filename.endswith('.gif'):
        img = ImageTk.PhotoImage(Image.open(filename))
        wininp.image_create('sel.first', image=img)
    else:
        id.open_file(wininp, filename)

def open_editor(filename):
    n.select('Editor')
    id.open_file(inp, filename)

def ask_open_editdialog(win):
    open_editdialog(filedialog.askopenfilename(), win)

def text_editdialog(text):
    win.deiconify()
    wininp.insert('1.0', text)

def show_buttons(e):
    b2.grid_remove()
    b1.grid_remove()
    f = os.listdir(folder.get())[listb.curselection()[0]]
    selfile.set(f)
    filen, filee = f.split('.')
    if filee in ['py', 'txt', 'csv', 'md', 'jpeg', 'png', 'bmp', 'blp', 'dds', 'eps', 'gif', 'icns', 'ico', 'msp', 'pcx', 'png', 'ppm', 'sgi', 'tga', 'tiff', 'webp', 'xbm']:
        b2.grid()
    if filee in ['py', 'txt', 'csv', 'md']:
        b1.grid()

def main():
    global win, wininp, shell_entry, entlbl, terminal_entry, output, inp, shell, editor, master, folder, files, listb, selfile, n, b1, b2
    master = tk.Tk()
    master.title('Editor')
    win = tk.Toplevel(master)
    master.option_add('*tearoff', tk.FALSE)
    menubar = tk.Menu(master)
    master['menu'] = menubar
    menu_file = tk.Menu(menubar)
    menu_file.add_command(label='Create', command=lambda: inp.delete(1.0, 'end'), accelerator='Command-N')
    menu_file.add_command(label='Open', command=lambda:id.ask_open_file(inp), accelerator='Command-O')
    menu_file.add_command(label='Save', command=lambda:id.save_file(inp), accelerator='Command-S')
    menu_file.add_separator()
    menu_file.add_command(label='Create in EasyEdit', command=win.deiconify)
    menu_file.add_command(label='Open Current File in EasyEdit', command=lambda: text_editdialog(inp.get(1.0, 'end')))
    menu_file.add_command(label='Open in EasyEdit', command=lambda: ask_open_editdialog(win))
    menubar.add_cascade(menu=menu_file, label='File')
    menu_edit = tk.Menu(menubar)
    menu_edit.add_command(label='Cut', command=lambda:master.focus_get().event_generate('<<Cut>>'), accelerator='Command-X')
    menu_edit.add_command(label='Copy', command=lambda:master.focus_get().event_generate('<<Copy>>'), accelerator='Command-C')
    menu_edit.add_command(label='Paste', command=lambda:master.focus_get().event_generate('<<Paste>>'), accelerator='Command-V')
    menu_edit.add_command(label='Undo', command=lambda:master.focus_get().event_generate('<<Undo>>'), accelerator='Command-Z')
    menu_edit.add_command(label='Redo', command=lambda:master.focus_get().event_generate('<<Redo>>'), accelerator='Shift-Command-Z')
    menubar.add_cascade(menu=menu_edit, label='Edit')
    win.withdraw()
    wininp = tk.Text(win, width=80, height=50, wrap='none')
    wininp.grid(column=0, row=0)
    wininp_yscroller = tk.Scrollbar(win, command=wininp.xview, orient='horizontal', bg='black')
    wininp_yscroller.grid(column=0, row=1, sticky='ew')
    wininp.config(yscrollcommand = wininp_yscroller.set)
    menubar2 = tk.Menu(win)
    win['menu'] = menubar2
    menu_file2 = tk.Menu(menubar2)
    menu_file2.add_command(label='Create', command=lambda: inp.delete(1.0, 'end'), accelerator='Command-N')
    menu_file2.add_command(label='Open', command=lambda:id.ask_open_file(wininp), accelerator='Command-O')
    menu_file2.add_command(label='Save', command=lambda:id.save_file(wininp), accelerator='Command-S')
    menu_file2.add_command(label='Close Window', command=win.withdraw)
    menubar2.add_cascade(menu=menu_file2, label='File')
    menu_edit2 = tk.Menu(menubar2)
    menu_edit2.add_command(label='Cut', command=lambda:win.focus_get().event_generate('<<Cut>>'), accelerator='Command-X')
    menu_edit2.add_command(label='Copy', command=lambda:win.focus_get().event_generate('<<Copy>>'), accelerator='Command-C')
    menu_edit2.add_command(label='Paste', command=lambda:win.focus_get().event_generate('<<Paste>>'), accelerator='Command-V')
    menu_edit2.add_command(label='Undo', command=lambda:win.focus_get().event_generate('<<Undo>>'), accelerator='Command-Z')
    menu_edit2.add_command(label='Redo', command=lambda:win.focus_get().event_generate('<<Redo>>'), accelerator='Shift-Command-Z')
    menubar2.add_cascade(menu=menu_edit2, label='Edit')
    menu_run = tk.Menu(menubar)
    menu_run.add_command(label='Run', command=launch)
    menu_run.add_command(label='Run File', command=launch_file)
    menubar.add_cascade(menu=menu_run, label='Run')
    menu_settings = tk.Menu(menubar)
    theme_menu = tk.Menu(menu_settings)
    theme_menu.add_command(label='Light', command=lambda: configure_mode(False))
    theme_menu.add_command(label='Dark', command=lambda: configure_mode(True))
    menu_settings.add_cascade(menu=theme_menu, label='Themes')
    menubar.add_cascade(menu=menu_settings, label='Settings')
    n = ttk.Notebook(master)
    editor = tk.Frame(master)
    shell = tk.Frame(master)
    n.add(editor, text='Editor')
    n.add(shell, text='Python Shell')
    n.pack()
    tk.Button(editor, text='+ Create', command=lambda: inp.delete(1.0, 'end')).grid(column=0, row=0)
    tk.Button(editor, text='⇧ Open', command=lambda:id.ask_open_file(inp)).grid(column=1, row=0)
    tk.Button(editor, text='⇩ Save', command=lambda:id.save_file(inp)).grid(column=2, row=0)
    tk.Button(editor, text='⏵ Run', command=launch).grid(column=3, row=0)
    tk.Button(editor, text='⏵ Run File', command=launch_file).grid(column=4, row=0)
    inp = tk.Text(editor, width=40, height=50, wrap='none')
    inp.grid(column=0, row=1, columnspan=3)
    inp_yscroller = tk.Scrollbar(editor, command=inp.xview, orient='horizontal', bg='black')
    inp_yscroller.grid(column=0, row=2, sticky='ew', columnspan=3)
    inp.config(yscrollcommand = inp_yscroller.set)
    output = tk.Text(editor, width=40, height=50, state='disabled')
    output_yscroller = tk.Scrollbar(editor, command=output.xview, orient='horizontal', bg='black')
    output_yscroller.grid(column=3, row=2, sticky='ew', columnspan=3)
    output.config(yscrollcommand = output_yscroller.set)
    output.tag_configure('right', justify=tk.RIGHT)
    output.grid(column=3, row=1, columnspan=3)

    entlbl = tk.Label(master, text='Enter commands for terminal')
    entlbl.pack()
    terminal_var = tk.StringVar()
    terminal_entry = tk.Entry(master, textvariable=terminal_var, width=60)
    terminal_entry.pack()
    terminal_entry.bind('<Return>', lambda evt:id.run_terminal(terminal_var, terminal_entry))

    shell_entry = tk.Text(shell, width=80, height=50, bg='white', fg='black')
    shell_entry.pack()
    shell_entry.tag_configure('prompt', foreground='green')
    shell_entry.tag_configure('output', foreground='red')
    shell_entry.insert('end', '>>> ', ('prompt',))
    shell_entry.bind('<Return>', lambda e:id.on_return(shell_entry))

    file_manager = tk.Frame(master)
    file_manager_labels = []
    n.add(file_manager, text='File Manager')
    folder = tk.StringVar(value=os.getcwd())
    l = tk.Label(file_manager, textvariable=folder)
    l.grid(column=0, row=0, columnspan=2, sticky='w')
    file_manager_labels.append(l)
    tk.Button(file_manager, text='Change Directory', command=setfolder).grid(column=0, row=1)
    files = tk.StringVar(value=os.listdir(folder.get()))
    listb = tk.Listbox(file_manager, listvariable=files, height=40, width=30)
    listb.grid(column=0, row=2, rowspan=4)
    selfile = tk.StringVar()
    l = tk.Label(file_manager, textvariable=selfile)
    l.grid(column=1, row=2)
    file_manager_labels.append(l)
    listb.bind('<<ListboxSelect>>', show_buttons)
    b1 = tk.Button(file_manager, text='Open in editor', command=lambda: open_editor(os.listdir(folder.get())[listb.curselection()[0]]))
    b2 = tk.Button(file_manager, text='Open in EasyEdit', command=lambda: open_editdialog(os.listdir(folder.get())[listb.curselection()[0]], win))
    b1.grid(column=1, row=3, sticky='n')
    b2.grid(column=1, row=4, sticky='n')
    b1.grid_remove()
    b2.grid_remove()
    tk.Button(file_manager, text='Open in default application', command=lambda : os.system('open ' + os.listdir(folder.get())[listb.curselection()[0]])).grid(column=1, row=5)
    master.mainloop()

if __name__ == '__main__':
    main()