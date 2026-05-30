from tkinter import Tk, Toplevel, Text, messagebox, StringVar, PhotoImage, simpledialog
from tkinter.ttk import Entry, Frame, Label, Button, Scrollbar, Notebook
from tkinter import Button as Tkbutton
from tkinter.font import Font, nametofont
from csv import writer, reader
from time import localtime

def load_files():
    with open('accounts.csv', 'r') as f:
        accounts = list(reader(f))
    with open('posts.csv', 'r') as f:
        posts = list(reader(f))
    return accounts, posts

def save_files():
    with open('accounts.csv', 'w') as f:
        writer(f).writerows(accounts)
    with open('posts.csv', 'w') as f:
        writer(f).writerows(posts)
    root.destroy()

def sign_up():
    win = Toplevel(root)
    win.title('Sign Up')
    f = Frame(win)
    f.grid(sticky='nwes')
    username = StringVar()
    password = StringVar()
    confirm = StringVar()
    error = StringVar()
    Label(f, text='Username:').grid(column=0, row=0)
    Entry(f, textvariable=username).grid(column=0, row=1)
    Label(f, text='Password:').grid(column=0, row=2)
    Entry(f, textvariable=password, show='•').grid(column=0, row=3)
    Label(f, text='Confirm password:').grid(column=0, row=4)
    Entry(f, textvariable=confirm, show='•').grid(column=0, row=5)
    Label(f, textvariable=error, foreground='red').grid(column=0, row=7)
    Button(f, text='Sign up', command=lambda: confirm_sign_up(username, password, confirm, error, win)).grid(column=0, row=8)

def confirm_sign_up(username, password, confirm, error, win):
    global account
    if username.get() == '' or password.get() == '':
        error.set('Fill out all fields')
        return
    elif password.get() != confirm.get():
        error.set('Passwords must match')
        return
    elif username.get() in [i[0] for i in accounts]:
        error.set('Username already in use')
        return
    accounts.append([username.get(), password.get()])
    account = username.get()
    account_var.set(f'Signed in as {account}')
    account_image.configure(file='account_circle.png')
    sign_out_frame.grid_remove()
    sign_in_frame.grid()
    win.destroy()

def sign_in():
    win = Toplevel(root)
    win.title('Sign In')
    f = Frame(win)
    f.grid(sticky='nwes')
    username = StringVar()
    password = StringVar()
    error = StringVar()
    Label(f, text='Username:').grid(column=0, row=0)
    Entry(f, textvariable=username).grid(column=0, row=1)
    Label(f, text='Password:').grid(column=0, row=2)
    Entry(f, textvariable=password, show='•').grid(column=0, row=3)
    Label(f, textvariable=error, foreground='red').grid(column=0, row=4)
    Button(f, text='Sign in', command=lambda: confirm_sign_in(username, password, error, win)).grid(column=0, row=6)

def confirm_sign_in(username, password, error, win):
    global account
    if username.get() == '' or password.get() == '':
        error.set('Fill out all fields')
        return
    elif not [username.get(), password.get()] in accounts:
        error.set('Invalid username or password')
        return
    account = username.get()
    account_var.set(f'Signed in as {account}')
    account_image.configure(file='account_circle.png')
    sign_out_frame.grid_remove()
    sign_in_frame.grid()
    win.destroy()

def get_date():
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    now = localtime()
    return f'{month[now.tm_mon-1]} {now.tm_mday}, {now.tm_year}'

def sign_out():
    global account
    account = None
    account_var.set('You\'re signed out')
    account_image.configure(file='no_account.png')
    sign_in_frame.grid_remove()
    sign_out_frame.grid()

def update_search(*args):
    search_posts = [i for i in posts if search.get().lower() in i[0].lower() or search.get().lower() in i[1].lower() or search.get().lower() in i[2].lower()]
    for i in windows:
        i.destroy()
    postlist.delete('1.0', 'end')
    for i, j in enumerate(search_posts, start=1):
        b = Tkbutton(postlist, text=f'{j[0]}\nBy: {j[2]}', width=15, command=lambda index= i-1 : view_post(index))
        windows.append(b)
        postlist.window_create(f'{i}.0', window=b)

def create_post():
    win = Toplevel(root)
    win.title('Create Post')
    f = Frame(win)
    f.grid(sticky='nwes')
    title = StringVar()
    Label(f, text='Post title:').grid(column=0, row=0, columnspan=2)
    Entry(f, textvariable=title).grid(column=0, row=1, columnspan=2)
    post = Text(f, highlightthickness=0, width=20, height=15, wrap='word', font='TkTextFont')
    post.grid(column=0, row=2)
    s = Scrollbar(f, command=post.yview, orient='vertical')
    s.grid(column=1, row=2, sticky='ns')
    post['yscrollcommand'] = s.set
    Button(f, text='Create post', command=lambda: add_post(title.get(), post.get('1.0', 'end'), account, win)).grid(column=0, row=3, columnspan=2)

def edit_post(index, win2):
    info = posts[index]
    win = Toplevel(root)
    win.title('Edit Post')
    f = Frame(win)
    f.grid(sticky='nwes')
    title = StringVar(value=info[0])
    Label(f, text='Post title:').grid(column=0, row=0, columnspan=2)
    Entry(f, textvariable=title).grid(column=0, row=1, columnspan=2)
    post = Text(f, highlightthickness=0, width=20, height=15, wrap='word', font='TkTextFont')
    post.insert('0.0', info[1])
    post.grid(column=0, row=2)
    s = Scrollbar(f, command=post.yview, orient='vertical')
    s.grid(column=1, row=2, sticky='ns')
    post['yscrollcommand'] = s.set
    Button(f, text='Edit post', command=lambda: confirm_edit(index, title.get(), post.get('1.0', 'end'), win, win2)).grid(column=0, row=3, columnspan=2)

def confirm_edit(index, title, text, win, win2):
    posts[index][0] = title
    posts[index][1] = text
    posts[index][3] = posts[index][3].split('\n')[0] + f'\nLast edited {get_date()}'
    win.destroy()
    win2.destroy()
    update_search()
    view_post(index)

def view_post(index):
    win = Toplevel(root)
    post_info = posts[index]
    win.title(post_info[0])
    f = Frame(win)
    f.grid(sticky='nwes')
    title = StringVar()
    font_dict = nametofont('TkDefaultFont').actual()
    font_dict['size'] *= 2
    large_font = Font(**font_dict)
    Label(f, text=post_info[0], font=large_font).grid(column=0, row=0, columnspan=2)
    Label(f, text=f'By: {post_info[2]}\n{post_info[3]}').grid(column=0, row=1, columnspan=2)
    post = Text(f, highlightthickness=0, width=20, height=15, wrap='word', font='TkTextFont')
    post.insert('0.0', post_info[1])
    post['state'] = 'disabled'
    post.grid(column=0, row=2)
    s = Scrollbar(f, command=post.yview, orient='vertical')
    s.grid(column=1, row=2, sticky='ns')
    post['yscrollcommand'] = s.set
    if post_info[2] == str(account):
        Button(f, text='Edit post', command=lambda: edit_post(index, win)).grid(column=0, row=3, columnspan=2)
        Button(f, text='Delete post', command=lambda: delete_post(index, win)).grid(column=0, row=4, columnspan=2)

def add_post(title, text, creator, win):
    posts.append([title, text, str(creator), f'Added {get_date()}'])
    win.destroy()
    update_search()

def delete_post(index, win):
    if messagebox.askyesno(message='Delete post?', detail='This will delete the post. This action cannot be undone.'):
        del posts[index]
        win.destroy()
        update_search()

def account_info(account):
    for i, j in enumerate(accounts):
        if j[0] == account:
            account_index = i
            break
    font_dict = nametofont('TkDefaultFont').actual()
    font_dict['size'] *= 2
    large_font = Font(**font_dict)
    win = Toplevel(root)
    win.title('Account')
    f = Frame(win)
    f.grid(sticky='nwes')
    posts_posted = 0
    for i in posts:
        if i[2] == account:
            posts_posted += 1
    Label(f, text=account, font=large_font).grid(column=0, row=0)
    Label(f, text=f'{posts_posted} posts posted').grid(column=0, row=1)
    Button(f, text='Delete account', command= lambda: delete_account(account_index, win)).grid(column=0, row=2)

def delete_account(index, win):
    global posts
    if simpledialog.askstring('Password', 'Enter password to delete account:', show='•') == accounts[index][1] \
    and messagebox.askyesno(message='Delete account?', detail='This will delete your account and all your posts. This action cannot be undone.'):
        sign_out()
        account = accounts.pop(index)[0]
        posts = [i for i in posts if i[2] != account]
        win.destroy()
        update_search()

root = Tk()
root.title('PyLog')
accounts, posts = load_files()
account = None
windows = []
account_var = StringVar(value='You\'re signed out')
account_image = PhotoImage(file='no_account.png')
pylog_image = PhotoImage(file='pylog.png')
f = Frame(root)
f.grid(sticky='nwes')
Label(f, image=pylog_image).grid(column=0, row=0, columnspan=2)
Label(f, textvariable=account_var, image=account_image, compound='left').grid(column=0, row=1, columnspan=2)
sign_in_frame = Frame(f)
sign_in_frame.grid(column=0, row=2, columnspan=2)
sign_out_frame = Frame(f)
sign_out_frame.grid(column=0, row=2, columnspan=2)
sign_in_frame.grid_remove()
Button(sign_out_frame, text='Sign up', command=sign_up).grid(column=0, row=0)
Button(sign_out_frame, text='Sign in', command=sign_in).grid(column=1, row=0)
Button(sign_in_frame, text='Account', command=lambda: account_info(account)).grid(column=0, row=0)
Button(sign_in_frame, text='Sign out', command=sign_out).grid(column=1, row=0)
Button(sign_in_frame, text='Create post', command=create_post).grid(column=0, row=1, columnspan=2)
Label(f, text='Search posts:').grid(column=0, row=3, columnspan=2)
search = StringVar()
search.trace_add('write', update_search)
Entry(f, textvariable=search).grid(column=0, row=4, columnspan=2)
postlist = Text(f, highlightthickness=0, width=25, height=20, state='disabled', background='gray90')
postlist.grid(column=0, row=5)
s = Scrollbar(f, command=postlist.yview, orient='vertical')
s.grid(column=1, row=5, sticky='ns')
postlist['yscrollcommand'] = s.set
root.protocol('WM_DELETE_WINDOW', save_files)
update_search()
root.mainloop()