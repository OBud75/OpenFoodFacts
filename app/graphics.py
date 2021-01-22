# coding: utf-8
#! /usr/bin/env python3

"""In this file we define the graphical part
"""

# Standard library import
from app import constants

# Third party import
from PySide6 import QtWidgets

# Local application imports

class Graphic(QtWidgets.QWidget):
    def __init__(self, database_manager):
        self.database_manager = database_manager
        super().__init__()
        self.window_parameters()
        self.setup_select_mode()

    def window_parameters(self):
        self.setWindowTitle("OpenFoodFacts")
        self.layout = QtWidgets.QVBoxLayout(self)

    def setup_select_mode(self):
        self.setup_select_mode_ui()
        #self.setup_select_mode_css()
        self.setup_select_mode_values()
        self.setup_select_mode_connections()

    def setup_select_mode_ui(self):
        self.cbb_select_mode = QtWidgets.QComboBox()
        self.layout.addWidget(self.cbb_select_mode)

    def setup_select_mode_css(self):
        self.setStyleSheet("""
        background-color: rgb(240, 240, 240);
        color: rgb(30, 30, 30);
        border: none;
        """)
        #self.btn_inverser.setStyleSheet("background-color: red;")

    def setup_select_mode_values(self):
        self.cbb_select_mode.addItems(constants.SELECT_MODE_LIST)

    def setup_select_mode_connections(self):
        self.cbb_select_mode.activated.connect(self.compute_cbb_select_mode)

    def compute_cbb_select_mode(self):
        mode = self.cbb_select_mode.currentText()
        if mode == "Quel aliment souhaitez-vous remplacer ?":
            self.layout.removeWidget(self.cbb_select_mode)
            self.setup_find_substitutes()
        elif mode == "Retrouver mes aliments substitués.":
            self.layout.removeWidget(self.cbb_select_mode)
            self.setup_saved_substitutes()

    def setup_find_substitutes(self):
        self.setup_find_substitutes_ui()
        self.setup_find_substitutes_css()
        self.setup_find_substitutes_values()
        self.setup_find_substitutes_connections()

    def setup_find_substitutes_ui(self):
        self.cbb_find_substitutes_starters_categories = QtWidgets.QComboBox()
        self.cbb_find_substitutes_categories = QtWidgets.QComboBox()
        self.cbb_find_substitutes_products = QtWidgets.QComboBox()
        self.lw_find_substitutes_substitutes = QtWidgets.QListWidget()
        self.btn_find_substitutes_save_substitute = QtWidgets.QPushButton("Enregistrer la substitution")
        self.btn_find_substitutes_return_select_mode = QtWidgets.QPushButton("Retourner au menu")

        self.layout.addWidget(self.cbb_find_substitutes_starters_categories)
        self.layout.addWidget(self.cbb_find_substitutes_categories)
        self.layout.addWidget(self.cbb_find_substitutes_products)
        self.layout.addWidget(self.lw_find_substitutes_substitutes)
        self.layout.addWidget(self.btn_find_substitutes_save_substitute)
        self.layout.addWidget(self.btn_find_substitutes_return_select_mode)

    def setup_find_substitutes_css(self):
        pass

    def setup_find_substitutes_values(self):
        self.setup_find_substitutes_starters_categories_values()

    def setup_find_substitutes_starters_categories_values(self):
        starters_categories = self.database_manager.categories_manager.create_categories(*constants.STARTERS_CATEGORIES)
        for starter_category in starters_categories:
            self.cbb_find_substitutes_starters_categories.addItem(starter_category.category_name)

    def setup_find_substitutes_categories_values(self):
        starter_category_name = self.cbb_find_substitutes_starters_categories.currentText()
        starter_category = self.database_manager.categories_manager.create_category(starter_category_name)
        category_has_categories = self.database_manager.category_has_categories_manager.create_category_has_categories(starter_category)
        for category in category_has_categories.childs:
            self.cbb_find_substitutes_categories.addItem(category.category_name)

    def setup_find_substitutes_products_values(self):
        category_name = self.cbb_find_substitutes_categories.currentText()
        category = self.database_manager.categories_manager.create_category(category_name)
        products = self.database_manager.product_has_categories_manager.get_products_in_category(category)
        for product in products:
            self.cbb_find_substitutes_products.addItem(product.product_name)

    def setup_find_substitutes_substitutes_values(self):
        product_name = self.cbb_find_substitutes_products.currentText()
        self.product = self.database_manager.products_manager.create_product_by_name(product_name)
        product_has_substitute = self.database_manager.product_has_substitutes_manager.create_product_has_substitutes(self.product)
        for substitute in product_has_substitute.substitutes:
            self.lw_find_substitutes_substitutes.addItem(substitute.product_name)

    def setup_find_substitutes_connections(self):
        self.cbb_find_substitutes_starters_categories.activated.connect(self.compute_cbb_find_substitutes_starters_categories)
        self.cbb_find_substitutes_categories.activated.connect(self.compute_cbb_find_substitutes_categories)
        self.cbb_find_substitutes_products.activated.connect(self.compute_cbb_find_substitutes_products)
        self.btn_find_substitutes_save_substitute.clicked.connect(self.compute_btn_find_substitutes_save_substitute)
        self.btn_find_substitutes_return_select_mode.clicked.connect(self.compute_btn_find_substitutes_return_select_mode)

    def compute_cbb_find_substitutes_starters_categories(self):
        self.cbb_find_substitutes_categories.clear()
        self.cbb_find_substitutes_products.clear()
        self.lw_find_substitutes_substitutes.clear()
        self.setup_find_substitutes_categories_values()

    def compute_cbb_find_substitutes_categories(self):
        self.cbb_find_substitutes_products.clear()
        self.lw_find_substitutes_substitutes.clear()
        self.setup_find_substitutes_products_values()

    def compute_cbb_find_substitutes_products(self):
        self.lw_find_substitutes_substitutes.clear()
        self.setup_find_substitutes_substitutes_values()

    def compute_btn_find_substitutes_save_substitute(self):
        substitute_names = self.lw_find_substitutes_substitutes.selectedIndexes()
        print(self.product.product_name)
        print(substitute_names)
        self.database_manager.product_has_substitutes_manager.save_substitute(self.product, substitute)

    def compute_btn_find_substitutes_return_select_mode(self, mode):
        self.layout.removeWidget(self.cbb_find_substitutes_starters_categories)
        self.layout.removeWidget(self.cbb_find_substitutes_categories)
        self.layout.removeWidget(self.cbb_find_substitutes_products)
        self.layout.removeWidget(self.lw_find_substitutes_substitutes)
        self.layout.removeWidget(self.btn_find_substitutes_save_substitute)
        self.layout.removeWidget(self.btn_find_substitutes_return_select_mode)

        self.setup_select_mode()

    def setup_saved_substitutes(self):
        self.setup_saved_substitutes_ui()
        self.setup_saved_substitutes_css()
        self.setup_saved_substitutes_values()
        self.setup_saved_substitutes_connections()

    def setup_saved_substitutes_ui(self):
        self.cbb_saved_substitutes_categories = QtWidgets.QComboBox()
        self.cbb_saved_substitutes_products = QtWidgets.QComboBox()
        self.lw_saved_substitutes_substitutes = QtWidgets.QListWidget()
        self.btn_saved_substitutes_delete_substitute = QtWidgets.QPushButton("Supprimer ce substitut")
        self.btn_saved_substitutes_return_select_mode = QtWidgets.QPushButton("Retourner au menu")

        self.layout.addWidget(self.cbb_saved_substitutes_categories)
        self.layout.addWidget(self.cbb_saved_substitutes_products)
        self.layout.addWidget(self.lw_saved_substitutes_substitutes)
        self.layout.addWidget(self.btn_saved_substitutes_delete_substitute)
        self.layout.addWidget(self.btn_saved_substitutes_return_select_mode)

    def setup_saved_substitutes_css(self):
        pass
    
    def setup_saved_substitutes_values(self):
        self.setup_saved_substitutes_categories_values()

    def setup_saved_substitutes_categories_values(self):
        products = self.database_manager.product_has_substitutes_manager.get_products_with_substitutes()
        for product in products:
            for category in product.product_has_categories.categories:
                self.cbb_saved_substitutes_categories.addItem(category.category_name)

    def setup_saved_substitutes_products_values(self):
        category_name = self.cbb_saved_substitutes_categories.currentText()
        category = self.database_manager.categories_manager.create_category(category_name)
        products = self.database_manager.product_has_categories_manager.get_products_in_category(category)
        for product in products:
            self.cbb_saved_substitutes_products.addItem(product.product_name)

    def setup_saved_substitutes_substitutes_values(self):
        product_name = self.cbb_saved_substitutes_products.currentText()
        product = self.database_manager.products_manager.create_product_by_name(product_name)
        product_has_substitute = self.database_manager.product_has_substitutes_manager.create_product_has_substitutes(product)
        for substitute in product_has_substitute.substitutes:
            self.lw_saved_substitutes_substitutes.addItem(substitute.product_name)

    def setup_saved_substitutes_connections(self):
        self.cbb_saved_substitutes_categories.activated.connect(self.compute_cbb_saved_substitutes_categories)
        self.cbb_saved_substitutes_products.activated.connect(self.compute_cbb_saved_substitutes_products)
        self.btn_saved_substitutes_delete_substitute.clicked.connect(self.compute_btn_saved_substitutes_delete_substitute)
        self.btn_saved_substitutes_return_select_mode.clicked.connect(self.compute_btn_saved_substitutes_return_select_mode)

    def compute_cbb_saved_substitutes_categories(self):
        self.cbb_saved_substitutes_categories.clear()
        self.cbb_saved_substitutes_products.clear()
        self.lw_saved_substitutes_substitutes.clear()
        self.setup_saved_substitutes_categories_values()

    def compute_cbb_saved_substitutes_products(self):
        self.cbb_saved_substitutes_products.clear()
        self.lw_saved_substitutes_substitutes.clear()
        self.setup_saved_substitutes_products_values()

    def compute_btn_saved_substitutes_delete_substitute(self):
        pass

    def compute_btn_saved_substitutes_return_select_mode(self):
        self.layout.removeWidget(self.cbb_saved_substitutes_categories)
        self.layout.removeWidget(self.cbb_saved_substitutes_products)
        self.layout.removeWidget(self.lw_saved_substitutes_substitutes)
        self.layout.removeWidget(self.btn_saved_substitutes_delete_substitute)
        self.layout.removeWidget(self.btn_saved_substitutes_return_select_mode)

        self.setup_select_mode()
