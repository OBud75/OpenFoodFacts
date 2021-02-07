# coding: utf-8
#! /usr/bin/env python3

"""Implémentation graphique de la partie
Quel aliment souhaitez-vous remplacer ?
"""

# Third party import
from PySide6 import QtWidgets

class FindSubstitutesView:
    """Partie graphique du mode
    Quel aliment souhaitez-vous remplacer ?
    """
    def __init__(self, window):
        """Initialisation
        L'attribut window correspond à
        la fenètre de l'application

        Args:
            window (Window): Instance de la fenètre d'application
        """
        self.window = window

    def setup_find_substitutes(self):
        """Disposition graphique du mode
        Quel aliment souhaitez-vous remplacer ?
        """
        self.cbb_starters_categories = QtWidgets.QComboBox()
        self.cbb_categories = QtWidgets.QComboBox()
        self.cbb_products = QtWidgets.QComboBox()
        self.lw_substitutes = QtWidgets.QListWidget()
        self.btn_save_substitute = QtWidgets.QPushButton("Enregistrer la substitution")
        self.btn_return_select_mode = QtWidgets.QPushButton("Retourner au menu")

        self.window.layout.addWidget(self.cbb_starters_categories)
        self.window.layout.addWidget(self.cbb_categories)
        self.window.layout.addWidget(self.cbb_products)
        self.window.layout.addWidget(self.lw_substitutes)
        self.window.layout.addWidget(self.btn_save_substitute)
        self.window.layout.addWidget(self.btn_return_select_mode)
