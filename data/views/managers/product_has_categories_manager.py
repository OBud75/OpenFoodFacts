# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from data.views.models.product_model import ProductModel

class ProductHasCategoriesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product_has_categories):
        product = product_has_categories.product
        categories = product_has_categories.categories
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        for category in categories:
            category.category_id = self.database_manager.categories_manager.get_category_id_by_name(category)
            self.add_to_table(product, category)

    def add_to_table(self, product, category):
        statement = (
            "INSERT INTO product_has_categories"
            "(product_id, category_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, category.category_id)
        self.database_manager.cursor.execute(statement, data)

    def get_products_in_category(self, category):
        query = ("""
            SELECT product_name
            FROM products JOIN categories
            WHERE category_name = %s
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        products_names = self.database_manager.cursor.fetchall()
        return [ProductModel(**{"product_name": product_name[0]}) for product_name in products_names]

    def count_products_in_category(self, category):
        query = ("""
            SELECT COUNT(DISTINCT product_name)
            FROM products JOIN product_has_categories JOIN categories
            WHERE category_name = %s
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result != None:
            return result[0]
