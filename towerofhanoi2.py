import tkinter as tk
from tkinter import messagebox

class Tower_of_hanoi_game:
    def __init__(self, root, num_disks):
        self.num_disks = num_disks
        self.root = root
        self.root.config(bg='black')
        self.root.geometry('400x300')
        self.mainframe = tk.Frame(root).grid(column=0, row=0)
        self.canvas = tk.Canvas(self.mainframe, width=400, height=100, background='black')
        self.canvas.grid(column=0, row=3, columnspan=2, pady=20)
        tk.Label(self.mainframe, text='Select a tower to move a disk from.', fg='white', bg='black').grid(column=0, row=0, sticky='w', pady=20)
        tk.Label(self.mainframe, text='Select a tower to move a disk to.', fg='white', bg='black').grid(column=0, row=1, sticky='w', pady=20)
        self.from_tower = tk.IntVar()
        self.to_tower = tk.IntVar()
        self.from_tower_entry = tk.Entry(self.mainframe, width=7, textvariable=self.from_tower, bg='black').grid(column=1, row=0)
        self.to_tower_entry = tk.Entry(self.mainframe, width=7, textvariable=self.to_tower, bg='black').grid(column=1, row=1)
        self.submit_button = tk.Button(self.mainframe, text='Submit', command=self.submit_move, bg='black').grid(column=0, row=2)
        self.towers = [[4,3,2,1], [], []]
        return None
    
    def draw_towers(self):
        tower_positions = [100, 200, 300]
        for i in tower_positions:
            self.canvas.create_rectangle(i - 5, 25, i + 5, 100, fill='red')
    
    def draw_disks(self):
        self.canvas.delete('disk')
        tower_positions = [100, 200, 300]
        for i, j in enumerate(self.towers):
            for x, y in enumerate(j, start=1):
                self.canvas.create_rectangle(tower_positions[i] - (10 * y), 100 - 10 * x, \
                tower_positions[i] + (10 * y), 100 - (10 *(x - 1)), fill='blue', tags='disk')
    
    def check_win(self):
        return self.towers == [[], [], [4,3,2,1]]
        
    def submit_move(self):
        ready = False
        from_tower = self.from_tower.get() - 1
        to_tower = self.to_tower.get() - 1
        # Uncomment code below to view move:
        #print(from_tower, to_tower)
        if from_tower > 3:
            messagebox.showinfo(message='Please enter 1, 2, or 3.', icon='warning')
        elif len(self.towers[from_tower]) == 0:
            messagebox.showinfo(message='That tower doesn\'t have any disks.', icon='warning')
        else:
            ready = True

        if to_tower > 3:
            messagebox.showinfo(message='Please enter 1, 2, or 3.', icon='warning')
            ready = False
        elif self.towers[to_tower] and self.towers[to_tower][-1] < self.towers[from_tower][-1]:
            messagebox.showinfo(message='You can\'t place a larger disk on top of a smaller disk.', icon='warning')
            ready = False
        else:
            ready = True
        
        
        if ready:
            self.move_disks(from_tower, to_tower)
            self.draw_disks()

        if self.check_win():
            self.canvas.create_text(200, 50, text='You win!', font=('Helvetica', 30), fill='black')
    
    def move_disks(self, from_tower, to_tower):
        moved_disk = self.towers[from_tower].pop()
        self.towers[to_tower].append(moved_disk)
                
    def gameloop(self):
        while True:
            if self.check_win():
                break
            #from_tower, to_tower = self.ask_move()
            print('Your move is', self.from_tower, self.to_tower)
            #self.move_disks(self.from_tower, self.to_tower)
            #self.draw_disks()
        self.canvas.create_text(200, 50, text='You win!', font=('Helvetica', 30), fill='black')

class Intro():
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x300')
        self.root.title('Tower Of Hanoi')
        tk.Label(self.root, text='''This game is inspired by Al Sweigart\'s Tower Of Hanoi game,
        available at https://nostarch.com/big-book-small-python-programming.
        To play the original game, click Play Original.
        To play my game, click Play.
        Instructions:
        Move the tower of disks, one disk at a time, to another tower. Larger
        disks cannot rest on top of a smaller disk. To win, all of the disks must be
        placed on the 3rd tower in order.''').grid(column=0, row=0, columnspan=2)
        tk.Button(self.root, text='Play', command=main).grid(column=0, row=1, pady=20)
        tk.Button(self.root, text='Play Original', command=self.original).grid(column=1, row=1, pady=20)

    def original(self):
        self.root.destroy()
        try:
            import towerofhanoioriginal as origin
            origin.main()
        except ModuleNotFoundError:
            messagebox.showinfo(message='To play the original game, download towerofhanoi.py from https://nostarch.com/big-book-small-python-programming\
                                and save it as towerofhanoioriginal.py.', icon='warning')

def start():
    global instructions
    instructions = tk.Tk()
    intro = Intro(instructions)
    instructions.mainloop()

def main():
    instructions.destroy()
    root = tk.Tk()
    root.title('Tower Of Hanoi')
    g = Tower_of_hanoi_game(root, 4)
    g.draw_towers()
    g.draw_disks()
    root.mainloop()
    

if __name__ == '__main__':
    start()