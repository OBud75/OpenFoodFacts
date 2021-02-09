# coding: utf-8
#! /usr/bin/env python3

"""Main application manager implementation

The user has the following choices:
1 - Which product would you like to replace?
2 - Find my substitute foods.

The user selects 1:
The program asks the following questions to the user
Select category
Select the food

The program offers a substitute, its description,
a store to buy it (if applicable)
and a link to the Open Food Facts page for that food.

The user then has the option of saving the result in the database.
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
    """User-side application manager
    """
    def __init__(self, database_manager):
        """Application initialization
        Instantiating the graphics window
        and its different parts

        Args:
            database_manager (DatabaseManager): Database manager instance
        """
        self.qt_widget_app = QtWidgets.QApplication()
        self.database_manager = database_manager
        self.window = Window()

        # Select mode
        self.select_mode_view = SelectModeView(self.window)
        self.select_mode_manager = SelectModeManager(self, self.select_mode_view)

        # Find substitutes
        self.find_substitutes_view = FindSubstitutesView(self.window)
        self.find_substitutes_manager = FindSubstitutesManager(self, self.find_substitutes_view)

        # Saved substitutes
        self.saved_substitutes_view = SavedSubstitutesView(self.window)
        self.saved_substitutes_manager = SavedSubstitutesManager(self, self.saved_substitutes_view)

        self.window.show()

    def run(self):
        """Method called by the launcher to start the application
        """
        self.select_mode()
        exit(self.qt_widget_app.exec_())

    def select_mode(self):
        """Mode selection
        """
        self.select_mode_view.setup_select_mode()
        self.select_mode_manager.setup_modes_values()
        self.select_mode_manager.connections()

    def find_substitutes(self):
        """The user selects "Which product would you like to replace?"
        """
        self.find_substitutes_view.setup_find_substitutes()
        self.find_substitutes_manager.setup_starters_categories_values()
        self.find_substitutes_manager.connections()

    def saved_substitutes(self):
        """The user selects "Find my substituted foods."
        """
        self.saved_substitutes_view.setup_saved_substitutes()
        self.saved_substitutes_manager.setup_products_values()
        self.saved_substitutes_manager.connections()
