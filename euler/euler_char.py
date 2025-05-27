from tkinter import Button, Label, Tk, StringVar
from PIL import ImageTk, Image
root = Tk()
root.title('Euler Characteristic')
cubepl = Image.open('cube.png')
tetrapl = Image.open('tetrahedron.jpeg')
octapl = Image.open('octahedron.png')
icosapl = Image.open('icosahedron.jpeg')
large_cubepl = cubepl.resize((180,180))
large_tetrapl = tetrapl.resize((180,180))
large_octapl = octapl.resize((180,180))
large_icosapl = icosapl.resize((180,180))
shapes = {'cube': {'image': ImageTk.PhotoImage(image=cubepl), 'large image': ImageTk.PhotoImage(image=large_cubepl), 'faces': 6, 'vertices': 8, 'edges': 12},
'tetrahedron': {'image': ImageTk.PhotoImage(image=tetrapl), 'large image': ImageTk.PhotoImage(image=large_tetrapl), 'faces': 4, 'vertices': 4, 'edges': 16},
'octahedron': {'image': ImageTk.PhotoImage(image=octapl), 'large image': ImageTk.PhotoImage(image=large_octapl), 'faces': 8, 'vertices': 6, 'edges': 12},
'icosahedron': {'image': ImageTk.PhotoImage(image=icosapl), 'large image': ImageTk.PhotoImage(image=large_icosapl), 'faces': 20, 'vertices': 12, 'edges': 30},}
def view_shape(shape):
    shape_dict = shapes[shape]
    info_var.set(f'''{shape}
Faces: {shape_dict['faces']}
Vertices: {shape_dict['vertices']}
Edges: {shape_dict['edges']}
Euler characteristic equation: {shape_dict['vertices']} - {shape_dict['edges']} + {shape_dict['faces']}
Euler characteristic: 2''')
    imagel['image'] = shape_dict['large image']

Label(root, text='Click on a shape to learn about it.').grid(column=0, row=0, columnspan=3)
info_var = StringVar()
Button(root, image=shapes['cube']['image'], command = lambda: view_shape('cube')).grid(column=0, row=1)
Button(root, image=shapes['tetrahedron']['image'], command = lambda: view_shape('tetrahedron')).grid(column=1, row=1)
Button(root, image=shapes['octahedron']['image'], command = lambda: view_shape('octahedron')).grid(column=2, row=1)
Button(root, image=shapes['icosahedron']['image'], command = lambda: view_shape('icosahedron')).grid(column=3, row=1)
Label(root, textvariable=info_var).grid(column=2, row=2, columnspan=2)
imagel = Label(root)
imagel.grid(column=0, row=2, columnspan=2)
root.mainloop()