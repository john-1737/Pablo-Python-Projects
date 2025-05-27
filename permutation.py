from tkinter import Entry, Button, Tk, Listbox, Label, StringVar

def find_permutations(word):
    print(word)
    global perms, perms_var
    perms = []
    wordlist = list(word)
    for i in list(word):
        wordlist = list(word)
        wordlist.remove(i)
        for j in wordlist:
            if wordlist.index(j) == 0:
                k = wordlist[1]
            else:
                k=wordlist[0]
            perm = i+j+k
            perms.append(perm)
    perms_var = StringVar(value=perms)
    lbox.config(listvariable=perms_var)
    print(perms)

def main():
    global perms, perms_var, lbox
    perms = []
    root = Tk()
    Label(root, text='Enter a 3-letter word').pack()
    word_var = StringVar()
    Entry(root, textvariable=word_var).pack()
    Button(root, text='Calculate All Permutations', command=lambda word_var = word_var : find_permutations(word_var.get())).pack()
    perms_var = StringVar(value=perms)
    lbox = Listbox(root, listvariable=perms_var, height=6)
    lbox.pack()
    root.mainloop()

if __name__ =='__main__':
    main()