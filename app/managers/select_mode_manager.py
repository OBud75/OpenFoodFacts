# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la partie
Selection du mode
"""

# Standard library import
from app import constants

class SelectModeManager:
    """Gestionnaire du menu
    """
    def __init__(self, application_manager, view):
        """Instanciation du gestionnaire de la partie
        Sélection du mode

        Args:
            application_manager (ApplicationManager): Gestionnaire de l'application
            view (SelectModeView): Partie graphique de la partie sélection du mode
        """
        self.application_manager = application_manager
        self.view = view

    def setup_modes_values(self):
        """Valeurs à afficher dans le widget "select mode"
        """
        self.view.cbb_select_mode.addItems(constants.SELECT_MODE_LIST)

    def connections(self):
        """Définit les connections entre méthodes et actions sur les widgets
        """
        self.view.cbb_select_mode.activated.connect(self.compute_cbb_select_mode)

    def compute_cbb_select_mode(self):
        """Actions à effectuer lors de la selection d'un mode
        """
        # Suppression du widget
        widget = self.application_manager.select_mode_view.cbb_select_mode
        self.application_manager.window.delete_widget(widget)
        mode = self.view.cbb_select_mode.currentText()

        # L'utilisateur choisit "Quel aliment souhaitez-vous remplacer ?"
        if mode == constants.SELECT_MODE_LIST[0]:
            self.application_manager.find_substitutes()

        # L'utilisateur choisit "Retrouver mes aliments substitués"
        elif mode == constants.SELECT_MODE_LIST[1]:
            self.application_manager.saved_substitutes()
