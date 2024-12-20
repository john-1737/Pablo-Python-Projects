import tkinter as tk

H_LINE = chr(196)
V_LINE = chr(179)
T_LINE = chr(194)

def math_to_py_func(math_func):
    return lambda x: eval(math_func)

print(H_LINE, V_LINE, T_LINE)