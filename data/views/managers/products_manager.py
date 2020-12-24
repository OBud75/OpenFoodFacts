"""In this file we put all the informations relatives to a product
"""

# Standard library import

# Third party import

# Local application imports
from data.views.models.product_model import ProductModel
from data.views.managers.categories_manager import CategoriesManager
from data.views.managers.stores_manager import StoresManager
from data.views.managers.product_has_categories_manager import ProductHasCategoriesManager
from data.api_manager import ApiManager

class ProductsManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.api_manager = ApiManager()
        self.categories_manager = CategoriesManager(self.database_manager)
        self.stores_manager = StoresManager(self.database_manager)
        self.product_has_categories_manager = ProductHasCategoriesManager(self.database_manager)

    def create_products(self):
        for product_infos in self.api_manager.get_products_list():
            # Products table
            product = ProductModel(**product_infos)
            if self.get_product_id_by_name(product.product_name) == None:
                self.add_to_table(product)

            # Categories table
            self.categories_manager.manage_categories(*product.product_has_categories.categories)
            
            # Link table product has categories
            self.product_has_categories_manager.manage(product.product_has_categories)

            # Stores
            store_name = product_infos.get('store_name')

    def get_product_id_by_name(self, product_name):
        query = ("""
            SELECT product_id
            FROM products
            WHERE product_name = %s
        """)
        data = (product_name,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchone()

    def add_to_table(self, product):
        statement = (
            "INSERT INTO products"
            "(product_name, ingredients_text, nutrition_grades, link)"
            "VALUES (%s, %s, %s, %s)"
        )
        data = (
            product.product_name, product.ingredients_text, product.nutrition_grades, product.link
        )
        self.database_manager.cursor.execute(statement, data)

    def update_table(self, product_id, category_id):
        pass