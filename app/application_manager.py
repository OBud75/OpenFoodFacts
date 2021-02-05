"""
"""

# Third party import
from PySide6 import QtWidgets

# Local application imports
from app.views.window import Window
from app.managers.select_mode_manager import SelectModeManager
from app.views.select_mode_view import SelectModeView
from app.managers.find_substitutes_manager import FindSubstitutesManager
from app.views.find_substitutes_view import FindSubstitutesView
from app.managers.saved_substitutes_manager import SavedSubstitutesManager
from app.views.saved_substitutes_view import SavedSubstitutesView

class ApplicationManager:
    def __init__(self, database_manager):
        self.qt_widget_app = QtWidgets.QApplication()
        self.database_manager = database_manager
        self.window = Window()
        self.window.show()

    def run(self):
        self.select_mode()
        exit(self.qt_widget_app.exec_())

    def select_mode(self):
        self.select_mode_view = SelectModeView(self.window)
        self.select_mode_manager = SelectModeManager(self, self.select_mode_view)
        self.select_mode_view.setup_select_mode()
        self.select_mode_manager.values()
        self.select_mode_manager.connections()

    def find_substitutes(self):
        self.find_substitutes_view = FindSubstitutesView(self.window)
        self.find_substitutes_manager = FindSubstitutesManager(self, self.find_substitutes_view)
        self.find_substitutes_view.setup_find_substitutes()
        self.find_substitutes_manager.values()
        self.find_substitutes_manager.connections()

    def saved_substitutes(self):
        self.saved_substitutes_view = SavedSubstitutesView(self.window)
        self.saved_substitutes_manager = SavedSubstitutesManager(self, self.saved_substitutes_view)
        self.saved_substitutes_view.setup_saved_substitutes()
        self.saved_substitutes_manager.values()
        self.saved_substitutes_manager.connections()
