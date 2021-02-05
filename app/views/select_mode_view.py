
# Third party import
from PySide6 import QtWidgets

# Standard library import
from app import constants

class SelectModeView:
    def __init__(self, window):
        self.window = window

    def setup_select_mode(self):
        self.cbb_select_mode = QtWidgets.QComboBox()

        self.window.layout.addWidget(self.cbb_select_mode)
