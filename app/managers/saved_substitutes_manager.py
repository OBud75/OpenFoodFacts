# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager
For the mode "Find my substitutes"
"""

class SavedSubstitutesManager:
    """Mode "Find my substitutes" manager
    """
    def __init__(self, application_manager, view):
        """Instantiation of the
        "Find my substitutes" manager

        Args:
            application_manager (ApplicationManager): Application manager
            view (SelectModeView): Graphic part of the "Find my substitutes" mode
        """
        self.application_manager = application_manager
        self.database_manager = self.application_manager.database_manager
        self.phs_manager = self.database_manager.product_has_substitutes_manager

        self.view = view

    def setup_products_values(self):
        """Values ​​to display in the "products" widget
        """
        products = self.phs_manager.get_saved_products()
        for product in products:
            self.view.cbb_products.addItem(product.product_name)

    def connections(self):
        """Defines the connections between methods and actions on widgets
        """
        self.view.cbb_products.activated.connect(self.compute_cbb_products)
        self.view.btn_delete_substitute.clicked.connect(self.compute_btn_delete_substitute)
        self.view.btn_return_select_mode.clicked.connect(self.compute_btn_return_select_mode)

    def setup_substitutes_values(self):
        """Values ​​to display in the "substitutes" widget
        """
        product_name = self.view.cbb_products.currentText()
        product_manager = self.database_manager.products_manager
        self.product = product_manager.create_product_by_name(product_name)

        product_has_subs = self.phs_manager.get_saved_substitutes_of_product(self.product)
        self.product.product_has_substitutes = product_has_subs

        for substitute in self.product.product_has_substitutes.substitutes:
            self.view.lw_substitutes.addItem(substitute.product_name)

    def compute_cbb_products(self):
        """Actions to take when selecting a product
        """
        self.view.lw_substitutes.clear()
        self.setup_substitutes_values()

    def compute_btn_delete_substitute(self):
        """Actions to perform when clicking on "Remove substitute"
        """
        # CurrentRow() returns -1 if no row is selected
        index = self.view.lw_substitutes.currentRow()
        if index != -1:
            substitute = self.product.product_has_substitutes.substitutes[index]
            self.phs_manager.delete_substitute(self.product, substitute)
        self.compute_btn_return_select_mode()

    def compute_btn_return_select_mode(self):
        """Actions to be performed when clicking on "Return to menu"
        """
        self.view.window.delete_widget(self.view.cbb_products)
        self.view.window.delete_widget(self.view.lw_substitutes)
        self.view.window.delete_widget(self.view.btn_delete_substitute)
        self.view.window.delete_widget(self.view.btn_return_select_mode)
        self.application_manager.select_mode()
