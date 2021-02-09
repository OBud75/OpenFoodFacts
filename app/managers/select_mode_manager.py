# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager
Part Select mode
"""

# Standard library import
from app import constants

class SelectModeManager:
    """Menu manager
    """
    def __init__(self, application_manager, view):
        """Instantiation of the menu manager

        Args:
            application_manager (ApplicationManager): Application manager
            view (SelectModeView): Graphic part of the menu
        """
        self.application_manager = application_manager
        self.view = view

    def setup_modes_values(self):
        """Values ​​to display in the "select mode" widget
        """
        self.view.cbb_select_mode.addItems(constants.SELECT_MODE_LIST)

    def connections(self):
        """Defines the connections between methods and actions on widgets
        """
        self.view.cbb_select_mode.activated.connect(self.compute_cbb_select_mode)

    def compute_cbb_select_mode(self):
        """Actions to perform when selecting a mode
        """
        # Removing the widget
        widget = self.view.cbb_select_mode
        self.application_manager.window.delete_widget(widget)
        mode = self.view.cbb_select_mode.currentText()

        # The user chooses "Which product do you want to replace?"
        if mode == constants.SELECT_MODE_LIST[0]:
            self.application_manager.find_substitutes()

        # The user chooses "Find my substitutes"
        elif mode == constants.SELECT_MODE_LIST[1]:
            self.application_manager.saved_substitutes()
