import tkinter as tk

with open('fiveletterwords.txt') as f:
    words = f.read().lower().splitlines()

root = tk.Tk()
root.config(bg='black')
# REMOVED THE GEOMETRY CALL
root.title('Wordle')
mainframe = tk.Frame(root)
mainframe.config(bg='black')
# Added two arguments to ensure that mainframe will expand to fill the entire window when resized
mainframe.pack(expand=True, fill='both')

# Added the following parameters: bg, fg, highlightbackground and highlightthickness
# Corrected the i and the j
labels = [[tk.Label(mainframe, width=2, height=1, relief='solid', text=' ', font=('Arial', 44), bd=2, bg='black', fg='white', highlightbackground='white', highlightthickness=2) for i in range(5)] for i in range(6)]
for i in range(6):
    for j in range(5):
        label = labels[i][j]
        label.grid(column=j, row=i, padx=2, pady=2, sticky='nsew')
        # Removed the blue coloring

root.mainloop()
