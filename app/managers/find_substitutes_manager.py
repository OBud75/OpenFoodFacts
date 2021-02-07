# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la partie
Quel aliment souhaitez-vous remplacer ?
"""

# Standard library import
from app import constants

class FindSubstitutesManager:
    """Gestionnaire de la partie
    Quels aliments souhaitez-bous remplacer ?
    """
    def __init__(self, application_manager, view):
        """Instanciation du gestionnaire de la partie
        Quel aliment souhaitez-vous remplacer ?

        Args:
            application_manager (ApplicationManager): Gestionnaire de l'application
            view (SelectModeView): Vue de la partie "Quel aliment souhaitez-vous remplacer ?"
        """
        self.application_manager = application_manager
        self.database_manager = self.application_manager.database_manager
        self.c_manager = self.database_manager.categories_manager
        self.p_manager = self.database_manager.products_manager
        self.phs_manager = self.database_manager.product_has_substitutes_manager
        self.phc_manager = self.database_manager.product_has_categories_manager
        self.chc_manager = self.database_manager.category_has_categories_manager

        self.view = view

    def connections(self):
        """Définit les connections entre méthodes et actions sur les widgets
        """
        self.view.cbb_starters_categories.activated.connect(self.compute_cbb_starters_categories)
        self.view.cbb_categories.activated.connect(self.compute_cbb_categories)
        self.view.cbb_products.activated.connect(self.compute_cbb_products)
        self.view.btn_save_substitute.clicked.connect(self.compute_btn_save_substitute)
        self.view.btn_return_select_mode.clicked.connect(self.compute_btn_return_select_mode)

    def setup_starters_categories_values(self):
        """Valeurs à afficher dans le widget "starters_categories"
        """
        starters_categories = self.c_manager.create_categories(*constants.STARTERS_CATEGORIES)
        for starter_category in starters_categories:
            self.view.cbb_starters_categories.addItem(starter_category.category_name)

    def setup_categories_values(self):
        """Valeurs à afficher dans le widget "categories"
        """
        starter_category_name = self.view.cbb_starters_categories.currentText()
        starter_category = self.c_manager.create(starter_category_name)
        category_has_categories = self.chc_manager.create(starter_category)
        for category in category_has_categories.childs:
            self.view.cbb_categories.addItem(category.category_name)

    def setup_products_values(self):
        """Valeurs à afficher dans le widget "products"
        """
        category_name = self.view.cbb_categories.currentText()
        category = self.c_manager.create(category_name)
        products = self.phc_manager.get_products_in_category(category)
        for product in products:
            self.view.cbb_products.addItem(product.product_name)

    def setup_substitutes_values(self):
        """Valeurs à afficher dans le widget "substitutes"
        """
        product_name = self.view.cbb_products.currentText()
        self.product = self.p_manager.create_product_by_name(product_name)

        # Instanciation de ProductHasSubstitutesModel
        phs = self.phs_manager.get_substitutes_of_product(self.product)
        self.product.product_has_substitutes = phs

        for substitute in self.product.product_has_substitutes.substitutes:
            # Liste des magasins
            stores = list()
            if substitute.product_has_stores is not None:
                for store in substitute.product_has_stores.stores:
                    stores.append(store.store_name)
            if len(stores) == 0:
                stores = "Aucun magasin trouvé"

            # Affichage des informations du substituts
            self.view.lw_substitutes.addItem(
                f"{substitute.product_name}\n\
                \t{substitute.ingredients_text}\n\
                \t{substitute.link}\n\
                \t{stores}\n")

    def compute_cbb_starters_categories(self):
        """Actions à effectuer lors de la sélection d'une catégorie de départ
        """
        self.view.cbb_categories.clear()
        self.view.cbb_products.clear()
        self.view.lw_substitutes.clear()
        self.setup_categories_values()

    def compute_cbb_categories(self):
        """Actions à effectuer lors de la sélection d'une catégorie
        """
        self.view.cbb_products.clear()
        self.view.lw_substitutes.clear()
        self.setup_products_values()

    def compute_cbb_products(self):
        """Actions à effectuer lors de la sélection d'un produit
        """
        self.view.lw_substitutes.clear()
        self.setup_substitutes_values()

    def compute_btn_save_substitute(self):
        """Actions à effectuer lors d'un click sur "Enregistrer le substitut"
        """
        # Récupération du produit et substitut sélectionnés
        index = self.view.lw_substitutes.currentRow()
        substitute = self.product.product_has_substitutes.substitutes[index]

        if not self.phs_manager.is_already_saved(self.product, substitute):
            self.phs_manager.save_substitute(self.product, substitute)

        # Retour au au menu de sélection du mode
        self.compute_btn_return_select_mode()

    def compute_btn_return_select_mode(self):
        """Actions à effectuer lors d'un click sur "Retourner au menu"
        """
        # Suppression des widgets
        self.view.window.delete_widget(self.view.cbb_starters_categories)
        self.view.window.delete_widget(self.view.cbb_categories)
        self.view.window.delete_widget(self.view.cbb_products)
        self.view.window.delete_widget(self.view.lw_substitutes)
        self.view.window.delete_widget(self.view.btn_save_substitute)
        self.view.window.delete_widget(self.view.btn_return_select_mode)

        # Retour au au menu de sélection du mode
        self.application_manager.select_mode()
