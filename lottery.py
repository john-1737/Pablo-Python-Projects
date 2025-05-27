import random
from tkinter import Tk, Button, Label, Listbox, IntVar, StringVar, Frame, ttk, messagebox, Scrollbar
from tkinter.ttk import Notebook
import lottery_games as lg
money = 10
def win_or_lose_lottery():
    num = lbox2.curselection()[0]
    price, pot = lotteries[num]
    global money
    if money - (price + pot) < 1 and not messagebox.askokcancel(message='Are you sure? This may make you lose.'):
        return
    money -= price
    if random.randint(0, 1):
        money += pot
    else:
        money -= pot
    moneyl['text'] = '$' + str(money)
    if money < 0:
        root.destroy()
        messagebox.showwarning(message='Game over! You lost all your money.')
def win_up_to_lottery():
    num = lbox1.curselection()[0]
    price, pot = lotteries[num]
    global money
    if money - (price) < 1 and not messagebox.askokcancel(message='Are you sure? This may make you lose.'):
        return    
    money -= price
    for i in range(pot, 0, -1000):
        if random.randint(0, i) == 0:
            money += i
            break
    moneyl['text'] = '$' + str(money)
    if money < 0:
        root.destroy()
        messagebox.showwarning(message=f'Game over! You lost all your money. You now have ${money}')
def play_game():
    global money
    num = lbox3.curselection()[0]
    x, func, max_lose, price = games[num]
    if money - (price + max_lose) < 1 and not messagebox.askokcancel(message='Are you sure? This may make you lose.'):
        return
    money -= price
    money += func()
    moneyl['text'] = '$' + str(money)
    if money < 0:
        root.destroy()
        messagebox.showwarning(message=f'Game over! You lost all your money. You now have ${money}')

root = Tk()
root.title('Lottery')
games = [('Taylor Swift quiz ($10 per point, win point for correct and lose for incorrect) for $5', lg.quiz, 70, 5),
         ('Bounce game ($20 per point, win point for bounce) for $10', lg.bounce, 0, 10),]
games_var = StringVar(value=[i[0] for i in games])
        
lotteries = [(i, i*1000000) for i in range(5, 105, 5)]
lose_lotteries = [(i, i*10) for i in range(5, 105, 5)]
Label(root, text='You now have:').pack()
moneyl=Label(root, text='$' + str(money), font=('Arial', 20))
moneyl.pack()
n = Notebook(root)
win_frame = Frame(n)
n.add(win_frame, text='Win pot lottery')
n.pack()
lotteries_var = StringVar(value=[f'Win up to ${i[1]} for ${i[0]}' for i in lotteries])
lose_lotteries_var = StringVar(value=[f'Win or lose ${i[1]} for ${i[0]}' for i in lose_lotteries])
lbox1 = Listbox(win_frame, listvariable=lotteries_var, height=20, width=25, selectmode='single')
lbox1.pack()
Button(win_frame, text='Buy ticket', command=win_up_to_lottery).pack()
lose_frame = Frame(n)
n.add(lose_frame, text='Win or lose pot lottery')
lbox2 = Listbox(lose_frame, listvariable=lose_lotteries_var, height=20, width=25, selectmode='single')
lbox2.pack()
Button(lose_frame, text='Buy ticket', command=win_or_lose_lottery).pack()
game_frame = Frame(n)
n.add(game_frame, text='Games')
lbox3 = Listbox(game_frame, listvariable=games_var, height=20, width=25, selectmode='single')
lbox3.pack()
scroll = Scrollbar(game_frame, orient='horizontal', command=lbox3.xview)
lbox3['xscrollcommand'] = scroll.set
scroll.pack()
Button(game_frame, text='Buy game', command=play_game).pack()
root.mainloop()