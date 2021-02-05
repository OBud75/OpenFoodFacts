"""
"""

# Standard library import
from app import constants


class SelectModeManager:
    def __init__(self, application_manager, view):
        self.application_manager = application_manager
        self.view = view

    def values(self):
        self.view.cbb_select_mode.addItems(constants.SELECT_MODE_LIST)

    def connections(self):
        self.view.cbb_select_mode.activated.connect(self.compute_cbb_select_mode)
    
    def compute_cbb_select_mode(self):
        mode = self.view.cbb_select_mode.currentText()
        self.application_manager.window.delete_widget(self.application_manager.select_mode_view.cbb_select_mode)
        if mode == constants.SELECT_MODE_LIST[0]:
            self.application_manager.find_substitutes()
        elif mode == constants.SELECT_MODE_LIST[1]:
            self.application_manager.saved_substitutes()
