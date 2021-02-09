# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the graphical window of the application
Using PySide6's QtWidgets
"""

# Third party import
from PySide6 import QtWidgets

# Standard library import
from app import constants

class Window(QtWidgets.QWidget):
    """GUI using QtWidgets

    Args:
        QtWidget (Widget): PySide6's Widget
    """
    def __init__(self):
        """Initialization of QtWidget attributes and methods
        """
        super().__init__()
        self.window_parameters()

    def window_parameters(self):
        """Window settings
        """
        self.setWindowTitle(constants.APP_NAME)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.resize(constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH)

    def delete_widget(self, widget):
        """Complete removal of a widget from the layout

        Args:
            widget (QtWidget): QtWidget instance
        """
        self.layout.removeWidget(widget)
        widget.deleteLater()
        widget = None
