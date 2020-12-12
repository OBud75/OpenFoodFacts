"""In this file we put all the informations relatives to a product
"""

# Standard library import

# Third party import

# Local application imports
from data.objects.models.product_model import ProductModel
from data.objects.categories_manager import CategoriesManager
from data.objects.stores_manager import StoresManager

class ProductsManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.categories_manager = CategoriesManager(self.database_manager)
        self.stores_manager = StoresManager(self.database_manager)

    def create_products(self):
        for product_infos in self.database_manager.products_table.get_products_list():
            category_name = product_infos.get('category_name')
            category = self.categories_manager.get_category(category_name)
            
            store_name = product_infos.get('store_name')
            store = self.stores_manager.get_store(store_name)

            product = ProductModel(**product_infos)
            self.add_to_table(product)

    def add_to_table(self, product):
        statement = (
            "INSERT INTO products"
            "(code, product_name, ingredients_text, nutrition_grades, link, category_name, store_name)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        data = (
            product.code, product.product_name, product.ingredients_text, product.nutrition_grades, product.link, product.category_name, product.store_name
        )
        self.database_manager.cursor.execute(statement, data)

    def modify_product(self, product_name, category_name, store_name):
        for product in self._products:
            if product.product_name == product_name:
                product.category_name = self.get_category_name(category_name)
                product.store_name = self.get_store_name(store_name)
                return product
