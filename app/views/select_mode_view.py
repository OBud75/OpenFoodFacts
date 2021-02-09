# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the graphic part of the menu
"""

# Third party import
from PySide6 import QtWidgets

class SelectModeView:
    """Graphic part of the menu
    """
    def __init__(self, window):
        """Initialization
        The window attribute corresponds to
        the application window

        Args:
            window (Window): Application window instance
        """
        self.window = window

    def setup_select_mode(self):
        """Graphical menu layout
        """
        self.cbb_select_mode = QtWidgets.QComboBox()
        self.window.layout.addWidget(self.cbb_select_mode)
