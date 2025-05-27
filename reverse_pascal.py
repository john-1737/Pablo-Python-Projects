from tkinter import Tk, Entry, Text, Label, IntVar, Button
def calculate_triangle():
    topnums = []
    for i in topnum_vars:
        topnums.append(i.get())
    nums = {}
    for i, j in enumerate(topnums, start=1):
        nums[1, i] = j
    for i in range(2, 11):
        for j in range(1, 12-i):
            nums[i, j] = nums[i-1, j] + nums[i-1, j + 1]
    for i in nums:
        nums[i] = str(nums[i]).ljust(7)
    t.delete('1.0', 'end')
    t.insert('1.0', '''#{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#
#################################################################################
    #{}#{}#{}#{}#{}#{}#{}#{}#{}#
    #########################################################################
        #{}#{}#{}#{}#{}#{}#{}#{}#
        #################################################################
            #{}#{}#{}#{}#{}#{}#{}#
            #########################################################
                #{}#{}#{}#{}#{}#{}#
                #################################################
                    #{}#{}#{}#{}#{}#
                    #########################################
                        #{}#{}#{}#{}#
                        #################################
                            #{}#{}#{}#
                            #########################
                                #{}#{}#
                                ################
                                    #{}#
                                    #########'''.format(*nums.values()).replace('#', chr(9608)))

root = Tk()
root.title('Reverse Pascal Triangle')
topnum_vars = []
for i in range(1, 11):
    Label(root, text=f'Top number {i}:').pack()
    x = IntVar()
    Entry(root, textvariable=x).pack()
    topnum_vars.append(x)
Button(root, text='Calculate', command=calculate_triangle).pack()
t = Text(root, width=81, height=20)
t.pack()
root.mainloop()