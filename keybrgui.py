from tkinter import Tk, Button, Label
keys = (tuple('qwertyuiop') + ('delete',),
        tuple('asdfghjkl') +('enter',) ,
        ('⇧ ',) + tuple('zxcvbnm,.⇧'))

num_keys = (tuple('789') + ('delete',),
            tuple('456-'),
            tuple('123'))
from itertools import cycle
caps_list = ('one_upper', 'upper', 'lower')
caps_cycle = cycle(caps_list)
display = caps_list[2]
symbol_display = False
letter_to_symbol_str= '''q1
w2
e3
r4
t5
y6
u7
i8
o9
p0
a@
s#
d$
f&
g*
h(
j)
k'
l"
z%
x-
c+
v=
b/
n;
m:
,,
..'''.splitlines()
letter_to_symbol = {}
for i in letter_to_symbol_str:
    letter_to_symbol[i[0]] = i[1]
letter_to_symbol['⇧'] = ']'
letter_to_symbol['⇧ '] = '['
def str_keyboard(head='Enter text', inittext=''):
    global exit
    global close
    global enteredtext, key_buttons
    exit = False
    close = False
    root = Tk()
    root.title(head)
    enteredtext = ''
    textlabel = Label(root, text=inittext, fg='gray')
    textlabel.grid(column=0, row=0, columnspan=11)
    key_buttons = {}
    for y, i in enumerate(keys, start=1):
        for x, j in enumerate(i):
            if y == 2 and x == 9:
                button = Button(root, text=j, width=10, height=3, command=_exit_str_keyboard)
                button.grid(column=x, row=y, columnspan=2)
            else:
                button = Button(root, text=j, width=3, height=3, command=lambda j=j : _respond_key(j))
                button.grid(column=x, row=y)
            key_buttons[j] = button
    button = Button(width=10, height=3, text='?123',command= lambda :_respond_key('?123'))
    button.grid(column=0, row=4, columnspan=2)
    key_buttons['?123'] = button
    button = Button(width=31, height=3, command = lambda : _respond_key(' '))
    button.grid(column=2, row=4, columnspan=5)
    button = Button(width=10, height=3, text='?123',command= lambda :_respond_key('?123'))
    button.grid(column=7, row=4, columnspan=2)
    key_buttons['?123 '] = button
    button = Button(width=10, height=3, text='close', command = _close)
    button.grid(column=9, row=4, columnspan=2)
    key_buttons['⇧ '].config(text='⇧')

    while True:
        if exit:
            if close:
                enteredtext = ''
            break
        else:
            if enteredtext:
                textlabel.config(text=enteredtext, fg='black')
            else:
                textlabel.config(text=inittext, fg='gray')
            root.update()
    root.destroy()
    return enteredtext

def _exit_str_keyboard():
    global exit
    exit = True

def _close():
    global exit, close
    exit = close = True

def _respond_key(key='?123'):
    global enteredtext, display, symbol_display
    if symbol_display == False:
        if key in 'abcdefghijklmnopqrstuvwxyz,. ':
            if display not in ('one_upper', 'upper'):
                enteredtext += key
            else:
                if key in(',.'):
                    enteredtext += {',':'!', '.':'?'}[key]
                else:
                    enteredtext += key.upper()
            if display == 'one_upper':
                for i in range(2): display = next(caps_cycle)
                _edit_caps(display)
        elif key == 'delete':
            enteredtext = list(enteredtext)
            try:
                enteredtext.pop()
            except:
                pass
            enteredtext = ''.join(enteredtext)
        elif key == '⇧' or key == '⇧ ':
            if display in caps_list:
                display = next(caps_cycle)
                _edit_caps(display)
        elif key == '?123':
            symbol_display = not symbol_display
            _edit_num(symbol_display)

    else:
        if key in ('abcdefghijklmnopqrstuvwxyz,.⇧') or key == '⇧ ':
            enteredtext += letter_to_symbol[key]
        elif key == 'delete':
            enteredtext = list(enteredtext)
            try:
                enteredtext.pop()
            except:
                pass
            enteredtext = ''.join(enteredtext)
        elif key == '?123':
            symbol_display = not symbol_display
            _edit_num(display)

def _edit_caps(display):
    key_buttons['⇧'].config(text={'lower': '⇧', 'one_upper': '⬆︎', 'upper': '⇪'}[display])
    key_buttons['⇧ '].config(text={'lower': '⇧', 'one_upper': '⬆︎', 'upper': '⇪'}[display])
    for i in 'abcdefghijklmnopqrstuvwxyz':
        if display in ('one_upper', 'upper'):
            key_buttons[i].config(text=i.upper())
            key_buttons[','].config(text='!')
            key_buttons['.'].config(text='?')
        else:
            key_buttons[i].config(text=i.lower())
            key_buttons[','].config(text=',')
            key_buttons['.'].config(text='.')

def _edit_num(num_display):
    if num_display == True:
        for i in list('abcdefghijklmnopqrstuvwxyz⇧'):
            key_buttons[i].config(text=letter_to_symbol[i])
        key_buttons['⇧ '].config(text=letter_to_symbol['⇧ '])
    else:
        for i in list('abcdefghijklmnopqrstuvwxyz'):
            key_buttons[i].config(text=i)
        key_buttons['⇧ '].config(text={'lower': '⇧', 'one_upper': '⬆︎', 'upper': '⇪'}[display])
        key_buttons['⇧'].config(text={'lower': '⇧', 'one_upper': '⬆︎', 'upper': '⇪'}[display])

def _respond_num_key(key='?123'):
    global enteredtext, display, symbol_display
    if key in ('1234567890'):
        enteredtext += key
    elif key == '.':
        if '.'  not in enteredtext:
            enteredtext += '.'
    elif key == 'delete':
        enteredtext = list(enteredtext)
        try:
            enteredtext.pop()
        except:
            pass
        enteredtext = ''.join(enteredtext)
    elif key == '-':
        if enteredtext.startswith('-'):
            enteredtext = list(enteredtext)
            enteredtext.pop(0)
            enteredtext = ''.join(enteredtext)
        else:
            enteredtext = '-' + enteredtext

def float_keyboard(head='Enter number', inittext=''):
    global exit
    global close
    global enteredtext, key_buttons
    exit = False
    close = False
    root = Tk()
    root.title(head)
    enteredtext = ''
    textlabel = Label(root, text=inittext, fg='gray')
    textlabel.grid(column=0, row=0, columnspan=11)
    key_buttons = {}
    for y, i in enumerate(num_keys, start=1):
        for x, j in enumerate(i):
            button = Button(root, text=j, width=3, height=3, command=lambda j=j : _respond_num_key(j))
            button.grid(column=x, row=y)
            key_buttons[j] = button
    button = Button(width=10, height=3, text='0',command= lambda :_respond_num_key('0'))
    button.grid(column=0, row=4, columnspan=2)
    key_buttons['0'] = button
    button = Button(width=3, height=3, text='.',command= lambda :_respond_num_key('.'))
    button.grid(column=2, row=4, columnspan=1)
    key_buttons['.'] = button
    button = Button(width=3, height=7, text='enter',command=_exit_str_keyboard)
    button.grid(column=3, row=3, rowspan=2)
    key_buttons['?123'] = button
    while True:
        if exit:
            if close:
                enteredtext = ''
            break
        else:
            if enteredtext:
                textlabel.config(text=enteredtext, fg='black')
            else:
                textlabel.config(text=inittext, fg='gray')
            root.update()
    root.destroy()
    try:
        return float(enteredtext)
    except:
        return 0.0
    
def int_keyboard(head='Enter number', inittext=''):
    return int(float_keyboard(head, inittext))

if __name__  == '__main__':
    raise TypeError('module must be imported, not run')