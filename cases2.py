import pyperclip
from tkinter import Tk, StringVar, Toplevel
from tkinter.ttk import Frame, Label, Button, Entry

def help():
    win = Toplevel(root)
    win.title('Help')
    f = Frame(win)
    f.grid(sticky='nwes')
    Label(f, text='''Welcome to Cases!

In this program, you can convert a message into a variety of casing styles,
such as Snake Case, Upper Snake Case, Camel Case, and Pascal Case.

Snake Case separates words with an underscore, and makes them lowercase.
This style is named because it uses underscores, which look like snakes.
It is used to define variables and functions in the programming
language Python.
this_is_an_example_of_snake_case

Upper Snake Case separates words with an underscore, and makes them
uppercase. This style is named because it is all uppercase and uses
underscores, which look like snakes. It is used to define constant variables
in various languages.
THIS_IS_AN_EXAMPLE_OF_UPPER_SNAKE_CASE
          
Camel Case separates letters by capitalizing the first letter of each word
following the first one. This style is named because the uppercase letters
look like a camel's humps. It is used to define variables and functions in
various languages.
thisIsAnExampleOfCamelCase
          
Pascal Case is similar to Camel Case, only the first letter is capitalized
as well. This style is named for its use in the programming language Pascal.
It is used to define variables and functions in the programming language
Pascal, as well as classes in various languages.
ThisIsAnExampleOfPascalCase''').grid(column=0, row=0)

def snake_case():
    text = original.get().lower()
    returntext = text.replace(' ', '_')
    info.set(f'{original.get()} in snake_case is:')
    converted.set(returntext)
    b.grid()
    
def UPPER_SNAKE_CASE():
    text = original.get().upper()
    returntext = text.replace(' ', '_')
    info.set(f'{original.get()} in UPPER_SNAKE_CASE is:')
    converted.set(returntext)
    b.grid()

def camelCase():
    text = original.get().title()
    text = list(text)
    text[0] = text[0].lower()
    text = ''.join(text)
    returntext = text.replace(' ', '')
    info.set(f'{original.get()} in camelCase is:')
    converted.set(returntext)
    b.grid()

def PascalCase():
    text = original.get().title()
    returntext = text.replace(' ', '')
    info.set(f'{original.get()} in PascalCase is:')
    converted.set(returntext)
    b.grid()

def main():
    global root, original, converted, info, b
    root = Tk()
    root.title('Cases')
    f = Frame(root)
    f.grid(sticky='nwes')
    Label(f, text='Enter your message to convert to a different casing style:').grid(column=0, row=0)
    original = StringVar()
    converted = StringVar()
    info = StringVar()
    Entry(f, textvariable=original).grid(column=0, row=1)
    Button(f, text='Convert to snake_case', command=snake_case).grid(column=0, row=2)
    Button(f, text='Convert to UPPER_SNAKE_CASE', command=UPPER_SNAKE_CASE).grid(column=0, row=3)
    Button(f, text='Convert to camelCase', command=camelCase).grid(column=0, row=4)
    Button(f, text='Convert to PascalCase', command=PascalCase).grid(column=0, row=5)
    Label(f, textvariable=info).grid(column=0, row=6)
    Label(f, textvariable=converted).grid(column=0, row=7)
    b = Button(f, text='Copy to clipboard', command=copy_text)
    b.grid(column=0, row=8) ; b.grid_remove()
    Button(f, text='Help', command=help).grid(column=0, row=9)
    root.mainloop()

def copy_text():
    pyperclip.copy(converted.get())

if __name__ == '__main__':
    main()