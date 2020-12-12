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
        self._products = list()
        self.categories_manager = CategoriesManager(self.database_manager)
        self.stores_manager = StoresManager(self.database_manager)

    def create_products(self):
        for product_infos in self.database_manager.products_table.get_products_list():
            category_name = product_infos.get('category_name')
            product_infos['category_name'] = self.categories_manager.get_category(category_name)
            
            store_name = product_infos.get('store_name')
            product_infos['store_name'] = self.stores_manager.get_store(store_name)

            if not self.is_product_in_table(product_infos['product_name']):
                product = ProductModel(**product_infos)
            else:
                product = self.find_existing_product(product_infos['product_name'])

            self.add_to_table(product)
            self._products.append(product)
    
    def is_product_in_table(self, product_name):
        query = ("""
            SELECT product_name
            FROM products
            WHERE product_name LIKE %s
        """)
        data = (product_name,)
        self.database_manager.cursor.execute(query, data)
        product = self.database_manager.cursor.fetchone()
        return product != None

    def find_existing_product(self, product_name):
        for product in self._products:
            if product.product_name == product_name:
                return product

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