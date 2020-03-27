#!/usr/bin/python3
import pylab
import sys
import tkinter as tk
from tkinter import filedialog as fd




# def readfile(fname):
#     xrr = []
#     yrr = []
#     arr = []
#     lines = []
#     fin = open(fname, 'r')
#     lent = 40
#     while True:
#         i = fin.readline()
#         try:
#             a = float(i.split()[0])
#             b = float(i.split()[1])
#         except (ValueError, IndexError):
#             lines.append(i)
#             continue
#         lent = len(i)-1
#         arr.append((a, b))
#         break
#     arr.extend([i.split() for i in fin])
#     xrr, yrr = [float(i[0]) for i in arr], [float(i[1]) for i in arr]
#     return lines, xrr, yrr, lent

class Window():
    def __init__(self, master):
        self.master = master
        tk.Button(self.master)

    def __openfile(self):
        pass

def main():
    root = tk.Tk()
    window = Window(root)
    root.mainloop()



if __name__ == "__main__":
    main()
