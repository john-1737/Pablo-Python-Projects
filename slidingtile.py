from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import random as ra
import copy as cp
import math
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import webbrowser as wb

class Sliding_tile_game:
    def __init__(self, root, squares, directory):
        self.root = root
        self.squares = int(math.sqrt(squares))
        self.directory = directory
        self.squarepositions = {}
        num_tile = 1
        for i in range(self.squares):
            for j in range(self.squares):
                self.squarepositions[i, j] = num_tile
                num_tile += 1
        self.finishedgrid = cp.copy(self.squarepositions)
        self.images = []
        self.buttons = []
        self.blank_number = self.squares ** 2

    def create_buttons(self):
        num_tile = 1
        for i in range(self.squares):
            for j in range(self.squares):
                imagepl = Image.open(f'{self.directory}/tile{num_tile}.gif')
                imagetk = ImageTk.PhotoImage(imagepl)
                self.images.append(imagetk)
                button = tk.Button(self.root, image=imagetk)
                self.buttons.append(button)
                num_tile += 1
        #self.blank = tk.Button(self.root)
        self.buttons[-1] = tk.Button(self.root)

    def display_buttons(self):
        blank_pos = self.find_blank()
        num_tile = 1
        squares_adjacent_to_blank = []
        squares_adjacent_to_blank.append((blank_pos[0] , (blank_pos[1] + 1)))
        squares_adjacent_to_blank.append((blank_pos[0] , (blank_pos[1] - 1)))
        squares_adjacent_to_blank.append(((blank_pos[0] + 1), blank_pos[1]))
        squares_adjacent_to_blank.append(((blank_pos[0] - 1), blank_pos[1]))
        for i in self.squarepositions:
            button_num = self.squarepositions[i] - 1
            button = self.buttons[button_num]
            button.grid(column=i[0], row=i[1])
            button.config(command=lambda i=i: self.move_button(i, self.find_blank(), True))
            if i not in squares_adjacent_to_blank:
                button.config(state=tk.DISABLED)
            else:
                button.config(state=tk.NORMAL)
            num_tile += 1
        
    def random_move(self, solving):
        blank_pos = self.find_blank()
        squares_adjacent_to_blank = []
        squares_adjacent_to_blank.append((blank_pos[0] , (blank_pos[1] + 1)))
        squares_adjacent_to_blank.append((blank_pos[0] , (blank_pos[1] - 1)))
        squares_adjacent_to_blank.append(((blank_pos[0] + 1), blank_pos[1]))
        squares_adjacent_to_blank.append(((blank_pos[0] - 1), blank_pos[1]))
        valid_moves = [pos for pos in squares_adjacent_to_blank if pos in self.squarepositions]
        if valid_moves:
            move = ra.choice(valid_moves)
            self.move_button(move, blank_pos, solving)

    def move_button(self, start, end, solving):
        self.squarepositions[start], self.squarepositions[end] = self.squarepositions[end], self.squarepositions[start]
        self.display_buttons()
        if self.check_win() and solving:
            mb.showinfo(message='Congratulations, you solved the puzzle!')

    def find_blank(self):
        keys = []
        for key, val in self.squarepositions.items():
            if val == self.blank_number:
                return key

    def check_win(self):
        return self.squarepositions == self.finishedgrid
    
class Instructions:
    def __init__(self, root):
        self.root = root
        self.root.title('Sliding Tile Game')
        tk.Label(self.root, text='''This game is inspired by Al Sweigart's Sliding Tile Puzzle game,
available at https://nostarch.com/big-book-small-python-programming.
To play the original game, click Play Original.
To play my game, click Play.
To open the original game online, click Open Original.
This game requires an image to use in the game.
You can select an image using the selection menu below.
Instructions:
Click on a tile to slide it to an empty space.
To win, all tiles must be in the right order.''').grid(column=0, columnspan=2, row=0)
        self.image_var = tk.StringVar()
        self.images_albums = ('1989b', 'midnightsb', 'loverb')
        radio_buttons = []
        for x in range(1, 4):
            radio_buttons.append(tk.Radiobutton(root, text=f'Image {x}', variable=self.image_var, value=self.images_albums[x-1]))
        for i, rb in enumerate(radio_buttons, start=1):
            rb.grid(column=0, row=i)
        self.image_var.set(None)
        imagefiles = []
        for i in self.images_albums:
            gif_path = f'photoimages/taylor{i}.gif'
            gif_image = tk.PhotoImage(file=gif_path)
            imagefiles.append(gif_image)
        for i, image in enumerate(imagefiles, start=1):
            tk.Label(self.root, image=image).grid(column=1, row=i)
        tk.Button(self.root, text='    Play    ',bg='blue', command=self.start_game).grid(column=0, row=4)
        tk.Button(self.root, text='Play Original', command=self.play_original).grid(column=1, row=4)
        tk.Button(self.root, text='Open Original', command=lambda:wb.open('https://nostarch.com/big-book-small-python-programming')).grid(column=0, row=5, columnspan=2)
        self.root.mainloop()

    def get_image(self):
        return self.image_var.get()

    def start_game(self):
        image = self.get_image()
        main(image)

    def play_original(self):
        self.root.destroy()
        try:
            import slidingtile_original as sl
            sl.main()
        except:
            mb.showinfo(message='The original sliding tile game is not downloaded. You can download it from https://nostarch.com/big-book-small-python-programming.')


def create_squares(filepath, squares):
    squares = math.sqrt(squares)
    image = Image.open(filepath)
    image_width, image_height = image.size
    tile_width = image_width / squares
    tile_height = image_height / squares
    num_tile = 1
    for i in range(0, int(squares)):
        for j in range(0, int(squares)):
            tile = image.crop((i * tile_width, j * tile_height, (i * tile_width) + tile_width, (j * tile_height) + tile_height))
            tile.save(f'photoimages/tiles/tile{num_tile}.gif')
            num_tile += 1

def main(image):
    startroot.destroy()
    try:
        difficulty = {1:9, 2:16, 3:25}[sd.askinteger('Enter difficulty', 'Enter difficulty level from 1 to 3')]
    except:
        difficulty = 9
    create_squares(f'photoimages/taylor{image}.gif', difficulty)
    root = tk.Tk()
    root.title('Sliding Tile Game')
    g = Sliding_tile_game(root, difficulty, 'photoimages/tiles')
    g.create_buttons()
    g.display_buttons()
    solving = False
    for i in range(5):
        g.random_move(solving)
    solving = True
    blank_key = g.find_blank()
    root.mainloop()

startroot = tk.Tk()
instruction = Instructions(startroot)
#print