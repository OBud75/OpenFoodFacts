"""
"""

# Standard library import
from app import constants


class SavedSubstitutesManager:
    def __init__(self, application_manager, view):
        self.application_manager = application_manager
        self.view = view

    def values(self):
        self.setup_products_values()

    def connections(self):
        self.view.cbb_products.activated.connect(self.compute_cbb_products)
        self.view.btn_delete_substitute.clicked.connect(self.compute_btn_delete_substitute)
        self.view.btn_return_select_mode.clicked.connect(self.compute_btn_return_select_mode)

    def setup_products_values(self):
        products = self.application_manager.database_manager.product_has_substitutes_manager.get_saved_products()
        for product in products:
            self.view.cbb_products.addItem(product.product_name)

    def setup_substitutes_values(self):
        product_name = self.view.cbb_products.currentText()
        self.product = self.application_manager.database_manager.products_manager.create_product_by_name(product_name)
        self.product.product_has_substitutes = self.application_manager.database_manager.product_has_substitutes_manager.get_saved_substitutes_of_product(self.product)
        for substitute in self.product.product_has_substitutes.substitutes:
            self.view.lw_substitutes.addItem(substitute.product_name)

    def compute_cbb_products(self):
        self.view.lw_substitutes.clear()
        self.setup_substitutes_values()

    def compute_btn_delete_substitute(self):
        # CurrentRow() returns -1 if no row is selected
        index = self.view.lw_substitutes.currentRow()
        if index != -1:
            substitute = self.product.product_has_substitutes.substitutes[index]
            self.application_manager.database_manager.product_has_substitutes_manager.delete_substitute(self.product, substitute)
        self.compute_btn_return_select_mode()

    def compute_btn_return_select_mode(self):
        self.view.window.delete_widget(self.view.cbb_products)
        self.view.window.delete_widget(self.view.lw_substitutes)
        self.view.window.delete_widget(self.view.btn_delete_substitute)
        self.view.window.delete_widget(self.view.btn_return_select_mode)
        self.application_manager.select_mode()
