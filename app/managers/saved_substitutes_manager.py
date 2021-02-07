# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la partie
Retrouver mes aliments substitués
"""

class SavedSubstitutesManager:
    """Gestionnaire de la partie
    Retrouver mes aliments substitués
    """
    def __init__(self, application_manager, view):
        """Instanciation du gestionnaire de la partie
        Retrouver mes aliments substitués

        Args:
            application_manager (ApplicationManager): Gestionnaire de l'application
            view (SelectModeView): Vue de la partie "Retrouver mes aliments substitués"
        """
        self.application_manager = application_manager
        self.database_manager = self.application_manager.database_manager
        self.phs_manager = self.database_manager.product_has_substitutes_manager

        self.view = view

    def setup_products_values(self):
        """Valeurs à afficher dans le widget "products"
        """
        products = self.phs_manager.get_saved_products()
        for product in products:
            self.view.cbb_products.addItem(product.product_name)

    def connections(self):
        """Définit les connections entre méthodes et actions sur les widgets
        """
        self.view.cbb_products.activated.connect(self.compute_cbb_products)
        self.view.btn_delete_substitute.clicked.connect(self.compute_btn_delete_substitute)
        self.view.btn_return_select_mode.clicked.connect(self.compute_btn_return_select_mode)

    def setup_substitutes_values(self):
        """Valeurs à afficher dans le widget "substitutes"
        """
        product_name = self.view.cbb_products.currentText()
        product_manager = self.database_manager.products_manager
        self.product = product_manager.create_product_by_name(product_name)

        product_has_subs = self.phs_manager.get_saved_substitutes_of_product(self.product)
        self.product.product_has_substitutes = product_has_subs

        for substitute in self.product.product_has_substitutes.substitutes:
            self.view.lw_substitutes.addItem(substitute.product_name)

    def compute_cbb_products(self):
        """Actions à effectuer lors de la sélection d'un produit
        """
        self.view.lw_substitutes.clear()
        self.setup_substitutes_values()

    def compute_btn_delete_substitute(self):
        """Actions à effectuer lors d'un click sur "Supprimer le substitut"
        """
        # CurrentRow() renvoie -1 si aucun substitut n'est sélectionné
        index = self.view.lw_substitutes.currentRow()
        if index != -1:
            substitute = self.product.product_has_substitutes.substitutes[index]
            self.phs_manager.delete_substitute(self.product, substitute)
        self.compute_btn_return_select_mode()

    def compute_btn_return_select_mode(self):
        """Actions à effectuer lors d'un click sur "Retourner au menu"
        """
        self.view.window.delete_widget(self.view.cbb_products)
        self.view.window.delete_widget(self.view.lw_substitutes)
        self.view.window.delete_widget(self.view.btn_delete_substitute)
        self.view.window.delete_widget(self.view.btn_return_select_mode)
        self.application_manager.select_mode()
