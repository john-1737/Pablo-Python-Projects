from tkinter import Tk, Canvas, filedialog, IntVar
from tkinter.ttk import Button, Label, LabeledScale, Frame
import re
from PIL import Image

def start():
    stop_frame.grid_remove()
    start_frame.grid()

def stop():
    start_frame.grid_remove()
    stop_frame.grid()

def toggle_cell(event):
    x, y = event.x, event.y
    cells[y//SIZE*80+x//SIZE] = not cells[y//SIZE*80+x//SIZE]
    draw_cells()

def draw_cells():
    c.delete('all')
    for i in range(50*80):
        if cells[i]:
            c.create_rectangle(i%80*SIZE, i//80*SIZE, i%80*SIZE+SIZE, i//80*SIZE+SIZE, fill='blue', tags='all')
    for i in range(-SIZE, SIZE*80+SIZE, SIZE):
        c.create_line(i, 0, i, SIZE*50, tags='all')
    for i in range(-SIZE, SIZE*50+SIZE, SIZE):
        c.create_line(0, i, SIZE*80, i, tags='all')
    c.move('all', 5, 5)

def clear():
    global cells
    cells = [False for i in range(80*50)]
    draw_cells()

def save_file():
    # Function by Google AI
    bits_tuple = tuple(cells)
    width, height = 80, 50
    output_path = filedialog.asksaveasfilename(title='Select file name to save as', filetypes=(('X bitmap images', '*.xbm'),))
    # Ensure the tuple length matches the total number of pixels

    # Create a new 1-bit black and white image
    img = Image.new("1", (width, height))
    
    # Put data takes a sequence where 0 is black and 255 (or 1) is white
    img.putdata(bits_tuple[:width * height])
    
    # Save the result
    img.save(output_path)

def load_file():
    global cells
    # Function by Google AI
    file_path = filedialog.askopenfilename(title='Select file to open', filetypes=(('X bitmap images', '*.xbm'),))
    with open(file_path, 'r') as f:
        content = f.read()
        
    # 1. Extract image width to handle row padding correctly
    width_match = re.search(r'_width\s+(\d+)', content)
    if not width_match:
        raise ValueError("Could not find width in XBM file")
    width = int(width_match.group(1))
    
    # 2. Extract all hexadecimal values
    hex_values = re.findall(r'0x[0-9a-fA-F]+', content)
    bytes_data = [int(h, 16) for h in hex_values]
    
    bits_list = []
    bits_in_current_row = 0
    
    # 3. Convert bytes to bits (LSB-first)
    for byte in bytes_data:
        for i in range(8):
            # Extract the i-th bit (LSB first)
            bit = (byte >> i) & 1
            bits_list.append(bit)
            bits_in_current_row += 1
            
            # XBM pads rows to byte boundaries; discard extra bits at row end
            if bits_in_current_row == width:
                bits_in_current_row = 0
                break # Move directly to the next byte for the next row
                
    cells = bits_list
    draw_cells()


SIZE = 15
root = Tk()
root.title('Conway\'s Game of Life')
f = Frame(root)
f.grid(sticky='nwes')
c = Canvas(f, width=SIZE*80+5, height=SIZE*50+5)
c.grid(column=0, row=0, columnspan=4, sticky='nwes', padx=0, pady=0)
cells = [False for i in range(80*50)]
c.bind('<Button-1>', toggle_cell)
c.focus()
stop_frame = Frame(f)
stop_frame.grid(column=0, row=1, sticky='nwes')
Label(stop_frame, width=SIZE*9).grid(column=0, row=0, columnspan=4)
Button(stop_frame, text='❎ Clear', command=clear).grid(column=0, row=0)
Button(stop_frame, text='▶️ Run', command=start).grid(column=1, row=0)
Button(stop_frame, text='📤 Open File', command=load_file).grid(column=2, row=0)
Button(stop_frame, text='📥 Save File', command=save_file).grid(column=3, row=0)

start_frame = Frame(f)
start_frame.grid(column=0, row=1, sticky='nwes')
start_frame.grid_remove()
Label(start_frame, width=SIZE*9).grid(column=0, row=0, columnspan=4)
Button(start_frame, text='❎ Clear', command=clear).grid(column=0, row=0, rowspan=2)
Button(start_frame, text='⏹️ Stop', command=stop).grid(column=1, row=0, rowspan=2)
fps = IntVar(value=1)
scale = LabeledScale(start_frame, from_=1, to=60, variable=fps)
scale.scale.configure(length=SIZE*40)
scale.grid(column=2, row=1, columnspan=2)
Label(start_frame, text='Frames per second:').grid(column=2, row=0, columnspan=2)
draw_cells()
root.mainloop()