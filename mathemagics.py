from matplotlib import pyplot as plt
from matplotlib import animation as anim
from math import floor, ceil
from tkinter import simpledialog

def update_dots(i):
    dot1.set_data(dot1list[i], 0)
    dot2.set_data(dot2list[i], 0)
    if i == len(dot1list) - 1:
        an.event_source.stop()
        text.set_text(f'{(len(dot1list) - 1)} hops\n\
({dot1list[-1]} ∙ {dot2list[-1]}) + ({(len(dot1list) - 1)}²)\n\
= {dot1list[-1] * dot2list[-1]} + {(len(dot1list) - 1) ** 2}\n\
= {(dot1list[-1] * dot2list[-1]) + ((len(dot1list) - 1) ** 2)}')
    return dot1, text

def find_stop(num):
    if num % 10 <= 5:
        return  num - floor(num/10) * 10
    else:
        return ceil(num/10) * 10 - num


num = simpledialog.askinteger('Enter a number', 'Enter a number to square using Arthur Benjamin\'s mathemagic trick')

xs = list((range(num-5, num+6)))
dot1list, dot2list = list(range(num, num + find_stop(num) + 1)), list(range(num - find_stop(num), num + 1))[::-1]
print(dot1list, dot2list)
ys = [0 for i in range(11)]
fig, ax = plt.subplots()
ax.plot(xs, ys)
ax.set_title('Arthur Benjamin\'s mathemagic trick')
ax.set_xticks(xs)
ax.set_ylim(-0.5, 0.5)
dot1, = ax.plot(num, 0, 'mo')
dot2, = ax.plot(num, 0, 'co')
text = ax.text(num, 0.25, '', fontsize=12, color='blue')
an = anim.FuncAnimation(fig, update_dots, frames=len(dot1list), interval=500)
plt.show()