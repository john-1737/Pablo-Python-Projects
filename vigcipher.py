import tkinter as tk
from tkinter import messagebox as mb
import pyperclip as cl

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def translate_message(message, key, encrypt):
    """Encrypt/decrypt the message using the key."""
    translated = []

    key_index = 0
    key = key.lower()
    for i in message:
        num = LETTERS.find(i.lower())
        if num != -1:
            if encrypt:
                num += LETTERS.find(key[key_index])
            else:
                num -= LETTERS.find(key[key_index])

            num %= len(LETTERS)

            if i.isupper():
                translated.append(LETTERS[num].upper())
            if i.islower():
                translated.append(LETTERS[num])

            key_index += 1
            if key_index == len(key):
                key_index = 0

        else:
            translated.append(i)

    return ''.join(translated)

def use_message(encrypt, text_var, key_var, trans_text_var):
    message = text_var.get()
    key = key_var.get()
    if key == '':
        mb.showwarning(message='Requires key')
        return
    trans_text_var.set(translate_message(message, key, encrypt))

def copy(message):
    cl.copy(message)
    mb.showinfo(message='Copied to clipboard')

def main():
    """Main program code"""
    root = tk.Tk()
    root.title('Vigenère Cipher')
    key_var = tk.StringVar()
    text_var = tk.StringVar()
    trans_text_var = tk.StringVar()
    tk.Label(root, text='Enter key (can be a word or letter combination of any kind):').grid(column=0, row=0, columnspan=2)
    tk.Entry(root, textvariable=key_var).grid(column=0, row=1, columnspan=2)
    tk.Label(root, text='Enter message to encrypt/decrypt').grid(column=0, row=2, columnspan=2)
    tk.Entry(root, textvariable=text_var).grid(column=0, row=3, columnspan=2)
    tk.Button(root, text='Encrypt', command=lambda:use_message(True, text_var, key_var, trans_text_var)).grid(column=0, row=4)
    tk.Button(root, text='Decrypt', command=lambda:use_message(False, text_var, key_var, trans_text_var)).grid(column=1, row=4)    
    tk.Label(root, text='Translated message:').grid(column=0, row=5, columnspan=2)
    tk.Label(root, textvariable=trans_text_var).grid(column=0, row=6, columnspan=2)
    tk.Button(root, text='Copy to clipboard', command=lambda:copy(trans_text_var.get())).grid(column=0, row=7, columnspan=2)
    tk.mainloop()

if __name__ == '__main__':
    main()