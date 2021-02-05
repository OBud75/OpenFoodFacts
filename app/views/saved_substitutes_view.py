# Third party import
from PySide6 import QtWidgets

# Standard library import
from app import constants

class SavedSubstitutesView:
    def __init__(self, window):
        self.window = window

    def setup_saved_substitutes(self):
        self.cbb_products = QtWidgets.QComboBox()
        self.lw_substitutes = QtWidgets.QListWidget()
        self.btn_delete_substitute = QtWidgets.QPushButton("Supprimer ce substitut")
        self.btn_return_select_mode = QtWidgets.QPushButton("Retourner au menu")

        self.window.layout.addWidget(self.cbb_products)
        self.window.layout.addWidget(self.lw_substitutes)
        self.window.layout.addWidget(self.btn_delete_substitute)
        self.window.layout.addWidget(self.btn_return_select_mode)
