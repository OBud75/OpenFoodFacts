"""In this file we put all the informations relatives to a product
"""

# Local application imports
from data.views.models.product_model import ProductModel

class ProductsManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, **product_infos):
        product = ProductModel(**product_infos)
        if self.get_product_id_by_name(product) == None:
            self.add_to_table(product)
        return product

    def get_product_id_by_name(self, product):
        query = ("""
            SELECT product_id
            FROM products
            WHERE product_name = %s
        """)
        data = (product.product_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result != None:
            return result[0]
        return False

    def add_to_table(self, product):
        statement = (
            "INSERT INTO products"
            "(product_name, ingredients_text, nutrition_grades, link)"
            "VALUES (%s, %s, %s, %s)"
        )
        data = (product.product_name, product.ingredients_text, product.nutrition_grades, product.link)
        self.database_manager.cursor.execute(statement, data)
