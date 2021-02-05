"""
"""

# Standard library import
from app import constants


class FindSubstitutesManager:
    def __init__(self, application_manager, view):
        self.application_manager = application_manager
        self.view = view

    def values(self):
        self.setup_starters_categories_values()

    def connections(self):
        self.view.cbb_starters_categories.activated.connect(self.compute_cbb_starters_categories)
        self.view.cbb_categories.activated.connect(self.compute_cbb_categories)
        self.view.cbb_products.activated.connect(self.compute_cbb_products)
        self.view.btn_save_substitute.clicked.connect(self.compute_btn_save_substitute)
        self.view.btn_return_select_mode.clicked.connect(self.compute_btn_return_select_mode)

    def setup_starters_categories_values(self):
        starters_categories = self.application_manager.database_manager.categories_manager.create_categories(*constants.STARTERS_CATEGORIES)
        for starter_category in starters_categories:
            self.view.cbb_starters_categories.addItem(starter_category.category_name)

    def setup_categories_values(self):
        starter_category_name = self.view.cbb_starters_categories.currentText()
        starter_category = self.application_manager.database_manager.categories_manager.create_category(starter_category_name)
        category_has_categories = self.application_manager.database_manager.category_has_categories_manager.create_category_has_categories(starter_category)
        for category in category_has_categories.childs:
            self.view.cbb_categories.addItem(category.category_name)

    def setup_products_values(self):
        category_name = self.view.cbb_categories.currentText()
        category = self.application_manager.database_manager.categories_manager.create_category(category_name)
        products = self.application_manager.database_manager.product_has_categories_manager.get_products_in_category(category)
        for product in products:
            self.view.cbb_products.addItem(product.product_name)

    def setup_substitutes_values(self):
        product_name = self.view.cbb_products.currentText()
        self.product = self.application_manager.database_manager.products_manager.create_product_by_name(product_name)
        self.product.product_has_substitutes = self.application_manager.database_manager.product_has_substitutes_manager.get_substitutes_of_product(self.product)
        for substitute in self.product.product_has_substitutes.substitutes:
            self.view.lw_substitutes.addItem(substitute.product_name)

    def compute_cbb_starters_categories(self):
        self.view.cbb_categories.clear()
        self.view.cbb_products.clear()
        self.view.lw_substitutes.clear()
        self.setup_categories_values()

    def compute_cbb_categories(self):
        self.view.cbb_products.clear()
        self.view.lw_substitutes.clear()
        self.setup_products_values()

    def compute_cbb_products(self):
        self.view.lw_substitutes.clear()
        self.setup_substitutes_values()

    def compute_btn_save_substitute(self):
        index = self.view.lw_substitutes.currentRow()
        substitute = self.product.product_has_substitutes.substitutes[index]
        if not self.application_manager.database_manager.product_has_substitutes_manager.is_already_saved(self.product, substitute):
            self.application_manager.database_manager.product_has_substitutes_manager.save_substitute(self.product, substitute)
        self.compute_btn_return_select_mode()

    def compute_btn_return_select_mode(self):
        self.view.window.delete_widget(self.view.cbb_starters_categories)
        self.view.window.delete_widget(self.view.cbb_categories)
        self.view.window.delete_widget(self.view.cbb_products)
        self.view.window.delete_widget(self.view.lw_substitutes)
        self.view.window.delete_widget(self.view.btn_save_substitute)
        self.view.window.delete_widget(self.view.btn_return_select_mode)
        self.application_manager.select_mode()
