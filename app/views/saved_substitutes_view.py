# coding: utf-8
#! /usr/bin/env python3

"""Graphical implementation of the part
Find my substitutes
"""

# Third party import
from PySide6 import QtWidgets

class SavedSubstitutesView:
    """Graphic part of the mode
    Find my substitutes
    """
    def __init__(self, window):
        """Initialization
        The window attribute corresponds to
        the application window

        Args:
            window (Window): Application window instance
        """
        self.window = window

    def setup_saved_substitutes(self):
        """Graphic layout of the mode
        Find my substitutes
        """
        self.cbb_products = QtWidgets.QComboBox()
        self.lw_substitutes = QtWidgets.QListWidget()
        self.btn_delete_substitute = QtWidgets.QPushButton("Supprimer ce substitut")
        self.btn_return_select_mode = QtWidgets.QPushButton("Retourner au menu")

        self.window.layout.addWidget(self.cbb_products)
        self.window.layout.addWidget(self.lw_substitutes)
        self.window.layout.addWidget(self.btn_delete_substitute)
        self.window.layout.addWidget(self.btn_return_select_mode)
