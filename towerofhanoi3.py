from tkinter import messagebox, Canvas, StringVar, Tk
from tkinter.ttk import Label, Button, Frame
from tkinter.font import Font, nametofont

class Tower_of_hanoi_game:
    def __init__(self, root, num_disks):
        self.num_disks = num_disks
        self.root = root
        self.mainframe = Frame(root)
        self.mainframe.grid(sticky='nwes')
        self.canvas = Canvas(self.mainframe, width=400, height=120)
        self.canvas.grid(column=0, row=3, columnspan=3)
        self.turn_var = StringVar(value='Select a tower to move a disk from:')
        self.error_var = StringVar()
        self.to_turn = False
        self.from_tower = None
        self.to_tower = None
        font_dict = nametofont('TkDefaultFont').actual()
        font_dict['weight'] = 'bold'
        bold_font = Font(**font_dict)
        Label(self.mainframe, textvariable=self.error_var, foreground='red', font=bold_font).grid(column=0, row=0, columnspan=3)
        Label(self.mainframe, textvariable=self.turn_var).grid(column=0, row=1, columnspan=3)
        self.button1 = Button(self.mainframe, text='1', command=lambda:self.make_move(0))
        self.button1.grid(column=0, row=2)
        self.button2 = Button(self.mainframe, text='2', command=lambda:self.make_move(1))
        self.button2.grid(column=1, row=2)
        self.button3 = Button(self.mainframe, text='3', command=lambda:self.make_move(2))
        self.button3.grid(column=2, row=2)
        self.button_reset = Button(self.mainframe, text='Play Again', command=main, default='active')
        self.button_reset.grid(column=0, row=4, columnspan=3)
        self.button_reset.grid_remove()
        self.towers = [[4,3,2,1], [], []]
        return None
    
    def draw_towers(self):
        tower_positions = [100, 200, 300]
        for i in tower_positions:
            self.canvas.create_rectangle(i - 5, 25, i + 5, 100, fill='red')
            self.canvas.create_text(i, 100, text=str(int(i/100)), anchor='n')
    
    def draw_disks(self):
        self.canvas.delete('disk')
        tower_positions = [100, 200, 300]
        for i, j in enumerate(self.towers):
            for x, y in enumerate(j, start=1):
                self.canvas.create_rectangle(tower_positions[i] - (10 * y), 100 - 10 * x, \
                tower_positions[i] + (10 * y), 100 - (10 *(x - 1)), fill='blue', tags='disk')
    
    def check_win(self):
        return self.towers == [[], [], [4,3,2,1]]
    
    def make_move(self, num):
        if not self.to_turn:
            if len(self.towers[num]) == 0:
                self.error_var.set('That tower doesn\'t have any disks.')
            else:
                self.from_tower = num
                self.to_turn = True
                self.error_var.set('')
                self.turn_var.set(f'Select a tower to move the disk on tower {num+1} to:')
        else:
            if self.towers[num] and self.towers[num][-1] < self.towers[self.from_tower][-1]:
                self.error_var.set('You can\'t place a larger disk on top of a smaller disk.')
            else:
                self.to_tower = num
                self.to_turn = False
                self.error_var.set('')
                self.turn_var.set('Select a tower to move a disk from:')
                self.submit_move()
                if self.check_win():
                    self.button1.grid_remove()
                    self.button2.grid_remove()
                    self.button3.grid_remove()
                    self.turn_var.set('')
                    self.error_var.set('')
                    self.button_reset.grid()
        
    def submit_move(self):
        ready = False
        from_tower = self.from_tower
        to_tower = self.to_tower
        ##Uncomment code below to view move:
        #print(from_tower, to_tower
        
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
            #self.move_disks(self.from_tower, self.to_tower)
            #self.draw_disks()
        self.canvas.create_text(200, 50, text='You win!', font=('Helvetica', 30), fill='black')

class Intro():
    def __init__(self, root):
        self.root = root
        self.mainframe = Frame(root)
        self.mainframe.grid(sticky='nwes')
        self.root.title('Tower Of Hanoi')
        Label(self.mainframe, text='''This game is inspired by Al Sweigart\'s Tower Of Hanoi game,
available at https://nostarch.com/big-book-small-python-programming.
To play the original game, click Play Original.
To play my game, click Play.
Instructions:
Move the tower of disks, one disk at a time, to another tower. Larger
disks cannot rest on top of a smaller disk. To win, all of the disks must be
placed on the 3rd tower in order.''').grid(column=0, row=0, columnspan=2)
        Button(self.mainframe, text='Play', command=main).grid(column=0, row=1, pady=20)
        Button(self.mainframe, text='Play Original', command=self.original).grid(column=1, row=1, pady=20)

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
    instructions = Tk()
    intro = Intro(instructions)
    instructions.mainloop()

def main():
    global root
    try:
        instructions.destroy()
    except:
        pass
    try:
        root.destroy()
        del g
    except:
        pass
    root = Tk()
    root.title('Tower Of Hanoi')
    g = Tower_of_hanoi_game(root, 4)
    g.draw_towers()
    g.draw_disks()
    root.mainloop()
    

if __name__ == '__main__':
    start()