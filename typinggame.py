from tkinter import *
tk = Tk()
canvas = Canvas(tk, width=500, height=50)
canvas.pack()

keys = list('abcdefghijklmnopqrstuvwxyz1234567890;')
keys.append('Return')
typed_keys = []
enter_key = u'\u23ce'

keys_to_type = 'abcdef'
lessons = [
    ['teach(\'Use your left index finger to type the F key\', \'f\')','scrolling(\'ffffffff\')', 
     'teach(\'Use your right index finger to type the J key\', \'j\')', 
     'scrolling(\'jjjjjjjjfjfjfjfjjfjfjfjf\')', 
     'teach(\'Use your thumbs to type the space key\', \'space\')', 
     'standard(\'jf jf jf jf fj fj fj fj ffj ffj jjf jjf\')', 
     "game(')"]
]

def check_key():
    clickkey = ''
    for key in keys:
        canvas.bind_all(f'<KeyPress-{key}>', return_key)
    canvas.bind_all('<space>', return_key)
 
def return_key(evt):
    if evt.keysym == 'space':
        typed_keys.append(' ')
    elif evt.keysym == 'Return':
        typed_keys.append(enter_key)
    else:
        typed_keys.append(evt.keysym)

def get_key():
    typed_keys = []
    check_key()
    if len(typed_keys) == 1:
        return typed_keys[0]

def compare(input, correct):
    endletter = len(input) - 1
    if list(input)[endletter] == list(correct)[endletter]:
        canvas.itemconfig(bottom_text, fill='green')
    else:
        canvas.itemconfig(bottom_text, fill='red')

def typing_game(correct):
    count = 0    
    keys_on_screen = str

key_finger = {
    'key' : 'a', 'finger' : ['left','middle']}
    
key_finger = {'a' : 'Use your left pinky finger', 'b' : 'Move your right index finger'}


#key_finger['a']

def teach(finger_pos, key):
    typed_key = ''
    change_top(finger_pos)
    canvas.itemconfig(bottom_text, text=key)
    while typed_key != key:
        typed_key = get_key()
        if typed_key != key:
            canvas.itemconfig(bottom_text, fill='red')
        tk.update()
    canvas.itemconfig(bottom_text, fill='green')
    change_top('test')
    
    tk.update()

def change_top(text, font='Helvetica', color='black'):
    canvas.itemconfig(top_text, text=text, font=(font, 25), fill=color)

top_text = canvas.create_text(5, 0, text='', font=('Helvetica', 25), state='normal', anchor='nw')
bottom_text = canvas.create_text(5, 25, text='', font=('Helvetica', 25), state='normal', anchor='nw')
keys_to_type = f'abcd{enter_key}efgs'
teach('Use your thumbs to type the space key.', ' ')
while True:
    # change_top(keys_to_type)
    # typed_key_str = ''
    # check_key()
    # #if not k == None or k == 0 or k == '':
    #     #canvas.itemconfig(id, text=str(k))
    #     #print(k)                          s
    # for x in typed_keys:
    #     typed_key_str += x
    # if typed_key_str != '':
    #     compare(typed_key_str, keys_to_type)
    
    # canvas.itemconfig(bottom_text, text=typed_key_str)
    
    tk.update()