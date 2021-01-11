# coding: utf-8
#! /usr/bin/env python3

"""In this file we define the graphical part
"""

# Standard library import
import tkinter

# Third party import

# Local application imports

class Graphic:
    def __init__(self, substitution_finder):
        self.substitution_finder = substitution_finder
        #self.window = tkinter.Tk()
        #self.window_parameters()
        #self.window.mainloop()

    def main_loop(self):
        self.substitution_finder.select_mode()

    def window_parameters(self):
        self.window.title("OpenFactFood")
        #self.window.iconbitmap("URL")
        #self.window.minsize(640, 480)
        #self.window.geometry()

"""
frame = tkinter.Frame()
label = tkinter.Label(window, text, font=('Courrier', 40), bg='x00')
label.pack(expand="YES", side="LEFT")
label.grid(row=0, column=1, row=1)
    
button = tkinter.Button(frame, text)
button.pack()

answer = tkinter.Entry(self.window).get()
canvas = tkinter.Canvas(self.window, width, height)
"""