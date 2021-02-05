# Third party import
from PySide6 import QtWidgets

# Standard library import
from app import constants

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.window_parameters()

    def window_parameters(self):
        self.setWindowTitle(constants.APP_NAME)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.resize(800, 600)

    def delete_widget(self, widget):
        self.layout.removeWidget(widget)
        widget.deleteLater()
        widget = None
