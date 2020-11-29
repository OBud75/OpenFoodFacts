"""In this file we define the graphical part
"""

# Standard library import
import tkinter

# Third party import

# Local application imports

class Graphic:
    def __init__(self, substitution_finder):
        self.substitution_finder = substitution_finder

    def main_loop(self):
        self.substitution_finder.main_loop()