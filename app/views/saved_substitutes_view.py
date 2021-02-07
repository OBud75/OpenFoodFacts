# coding: utf-8
#! /usr/bin/env python3

"""Implémentation graphique de la partie
Retrouver mes aliments substitués
"""

# Third party import
from PySide6 import QtWidgets

class SavedSubstitutesView:
    """Partie graphique du mode
    Retrouver mes aliments substitués
    """
    def __init__(self, window):
        """Initialisation
        L'attribut window correspond à
        la fenètre de l'application

        Args:
            window (Window): Instance de la fenètre d'application
        """
        self.window = window

    def setup_saved_substitutes(self):
        """Disposition graphique du mode
        Retrouver mes aliments substitués
        """
        self.cbb_products = QtWidgets.QComboBox()
        self.lw_substitutes = QtWidgets.QListWidget()
        self.btn_delete_substitute = QtWidgets.QPushButton("Supprimer ce substitut")
        self.btn_return_select_mode = QtWidgets.QPushButton("Retourner au menu")

        self.window.layout.addWidget(self.cbb_products)
        self.window.layout.addWidget(self.lw_substitutes)
        self.window.layout.addWidget(self.btn_delete_substitute)
        self.window.layout.addWidget(self.btn_return_select_mode)
