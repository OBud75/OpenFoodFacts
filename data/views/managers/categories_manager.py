"""
"""

# Local application imports
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

    def add_to_table(self, category):
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (category.category_name,)
        self.database_manager.cursor.execute(statement, data)

    def get_categories(self):
        query = ("""
            SELECT category_name
            FROM categories
        """)
        self.database_manager.cursor.execute(query)
        categories_names = self.database_manager.cursor.fetchall()
        return [CategoryModel(category_name[0]) for category_name in categories_names]

    def get_products(self, category):
        query = ("""
            SELECT product_name
            FROM products JOIN categories
            WHERE category_name = %s
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        products_names = self.database_manager.cursor.fetchall()
        return [ProductModel(**{"product_name": product_name[0]}) for product_name in products_names]
