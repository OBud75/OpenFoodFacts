# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from data.views.models.product_model import ProductModel

class ProductHasSubstitutesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def save_substitute(self, product, substitute):
        product_id = self.database_manager.products_manager.get_product_id(product)
        substitute_id = self.database_manager.products_manager.get_product_id(substitute)
        statement = (
            "INSERT INTO product_has_substitutes"
            "(product_id, substitute_id)"
            "VALUES (%s, %s)"
        )
        data = (product_id, substitute_id)
        self.database_manager.cursor.execute(statement, data)
        self.database_manager.mydb.commit()

    def get_products_with_substitutes(self):
        self.database_manager.cursor.execute("""
            SELECT DISTINCT product_name
            FROM products JOIN product_has_substitutes
        """)
        products_names = self.database_manager.cursor.fetchall()
        return [ProductModel(**{"product_name": product_name[0]}) for product_name in products_names]

    def get_substitutes_of_product(self, product):
        query = ("""
            SELECT DISTINCT product_name
            FROM products JOIN product_has_categories JOIN categories
            WHERE category_name IN (SELECT category_name
                                    FROM products JOIN product_has_categories JOIN categories
                                    WHERE product_name = %s)
            AND nutrition_grades < %s
        """)
        data = (product.product_name, self.database_manager.products_manager.get_nutrition_grades(product))
        self.database_manager.cursor.execute(query, data)
        products_names = self.database_manager.cursor.fetchall()
        return [ProductModel(**{"product_name": product_name[0]}) for product_name in products_names]

    def get_saved_substitutes_of_product(self, product):
        query = ("""
            SELECT product_name
            FROM products
            WHERE product_id IN (SELECT substitute_id
                                 FROM product_has_substitutes
                                 WHERE product_id = %s)
        """)
        data = (self.database_manager.products_manager.get_product_id(product),)
        self.database_manager.cursor.execute(query, data)
        products_names = self.database_manager.cursor.fetchall()
        return [ProductModel(**{"product_name": product_name[0]}) for product_name in products_names]
