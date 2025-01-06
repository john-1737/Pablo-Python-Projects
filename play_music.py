import tkinter as tk
from tkinter import ttk
from pygame import mixer

def play_music

song_name = tk.StringVar()
song_artist = tk.StringVar()
root = tk.Tk()

songs = ['a\nb', 'b']
songs_var = tk.StringVar(value=songs)
songs_lbox = tk.Listbox(root, listvariable=songs_var)
songs_lbox.grid(column=0, row=0, padx=20, pady=20)


root.mainloop()