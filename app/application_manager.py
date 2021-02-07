# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire principal de l'application
L'utilisateur a les choix suivants :
1 - Quel aliment souhaitez-vous remplacer ?
2 - Retrouver mes aliments substitués.

L'utilisateur sélectionne 1:
Le programme pose les questions suivantes à l'utilisateur
Sélectionnez la catégorie
Sélectionnez l'aliment

Le programme propose un substitut, sa description,
un magasin où l'acheter (le cas échéant)
et un lien vers la page d'Open Food Facts concernant cet aliment.

L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.
"""

# Standard library import
from sys import exit

# Third party import
from PySide6 import QtWidgets

# Local application imports
from app.window import Window
from app.managers.select_mode_manager import SelectModeManager
from app.views.select_mode_view import SelectModeView
from app.managers.find_substitutes_manager import FindSubstitutesManager
from app.views.find_substitutes_view import FindSubstitutesView
from app.managers.saved_substitutes_manager import SavedSubstitutesManager
from app.views.saved_substitutes_view import SavedSubstitutesView

class ApplicationManager:
    """Gestionnaire de l'application côté utilisateur
    """
    def __init__(self, database_manager):
        """Initialisation de l'application
        Instanciation de la fenètre graphique
        et de ses différentes parties

        Args:
            database_manager (DatabaseManager): Gestionnaire de la base de données
        """
        self.qt_widget_app = QtWidgets.QApplication()
        self.database_manager = database_manager
        self.window = Window()

        # Menu
        self.select_mode_view = SelectModeView(self.window)
        self.select_mode_manager = SelectModeManager(self, self.select_mode_view)

        # Remplacer un aliment
        self.find_substitutes_view = FindSubstitutesView(self.window)
        self.find_substitutes_manager = FindSubstitutesManager(self, self.find_substitutes_view)

        # Retrouver mes aliments substitués
        self.saved_substitutes_view = SavedSubstitutesView(self.window)
        self.saved_substitutes_manager = SavedSubstitutesManager(self, self.saved_substitutes_view)

        # Affiche la fenètre
        self.window.show()

    def run(self):
        """Méthode apellée par le launcher pour démarrer l'application
        """
        self.select_mode()
        exit(self.qt_widget_app.exec_())

    def select_mode(self):
        """Selection du mode
        """
        self.select_mode_view.setup_select_mode()
        self.select_mode_manager.setup_modes_values()
        self.select_mode_manager.connections()

    def find_substitutes(self):
        """L'utilisateur sélectionne "Quel aliment souhaitez-vous remplacer ?"
        """
        self.find_substitutes_view.setup_find_substitutes()
        self.find_substitutes_manager.setup_starters_categories_values()
        self.find_substitutes_manager.connections()

    def saved_substitutes(self):
        """L'utilisateur sélectionne "Retrouver mes aliments substitués."
        """
        self.saved_substitutes_view.setup_saved_substitutes()
        self.saved_substitutes_manager.setup_products_values()
        self.saved_substitutes_manager.connections()
