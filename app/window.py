# coding: utf-8
#! /usr/bin/env python3

"""Implémentation de la fenètre graphique de l'application
Utilisation de QtWidgets de PySide6
"""

# Third party import
from PySide6 import QtWidgets

# Standard library import
from app import constants

class Window(QtWidgets.QWidget):
    """Interface graphique utilisant QtWidgets

    Args:
        QtWidgets ([type]): [description]
    """
    def __init__(self):
        """Initialisation des attributs et méthodes QtWidget
        Paramètrages de la fenètres
        """
        super().__init__()
        self.window_parameters()

    def window_parameters(self):
        """Paramètres de la fenètre
        """
        self.setWindowTitle(constants.APP_NAME)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.resize(constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH)

    def delete_widget(self, widget):
        """Suppression complète d'un widget du layout

        Args:
            widget (QtWidget): Instance de QtWidget
        """
        self.layout.removeWidget(widget)
        widget.deleteLater()
        widget = None
