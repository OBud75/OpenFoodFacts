# coding: utf-8
#! /usr/bin/env python3

"""Implémentation de la partie graphique du menu
"""

# Third party import
from PySide6 import QtWidgets

class SelectModeView:
    """Partie graphique du menu
    """
    def __init__(self, window):
        """Initialisation
        L'attribut window correspond à
        la fenètre de l'application

        Args:
            window (Window): Instance de la fenètre d'application
        """
        self.window = window

    def setup_select_mode(self):
        """Mise en place graphique du menu
        """
        self.cbb_select_mode = QtWidgets.QComboBox()
        self.window.layout.addWidget(self.cbb_select_mode)
