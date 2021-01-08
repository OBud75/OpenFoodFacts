"""
"""

from data.views.models.category_model import CategoryModel
from data.views.models.product_model import ProductModel

class CategoriesManager:
    """Link between categories and database
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, *categories):
        for category in categories:
            if not self.get_category_id_by_name(category):
                self.add_to_table(category)

    def get_category_id_by_name(self, category):
        query = ("""
                SELECT category_id
                FROM categories
                WHERE category_name LIKE %s
            """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result != None:
            return result[0]
        return False

    def add_to_table(self, category):
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (category.category_name,)
        self.database_manager.cursor.execute(statement, data)

    def get_categories_names(self):
        query = ("""
            SELECT category_name
            FROM categories
        """)
        self.database_manager.cursor.execute(query)
        return self.database_manager.cursor.fetchall()[0]

    def get_categories(self):
        categories = list()
        for category_name in self.get_categories_names():
            category = CategoryModel(category_name)
            category.category_id = self.get_category_id_by_name(category.category_name)
            categories.append(category)
        return categories

    def get_products_in_category(self, category):
        query = ("""
            SELECT product_name
            FROM products JOIN categories
            WHERE category_name = %s
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchall()

    def get_products(self, category):
        products = list()
        for product_name in self.get_products_in_category(category):
            print(product_name[0])
            product = ProductModel(product_name=product_name[0])
            product.product_id = self.database_manager.products_manager.get_product_id_by_name(product_name[0])
            products.append(product)
        return products
