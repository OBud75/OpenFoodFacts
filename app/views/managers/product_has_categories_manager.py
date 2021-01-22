# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from app.views.models.product_has_categories_model import ProductHasCategoriesModel

class ProductHasCategoriesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product_has_categories):
        product = product_has_categories.product
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        for category_has_categories in product_has_categories.categories_have_categories:
            category = category_has_categories.category
            category.category_id = self.database_manager.categories_manager.get_category_id(category)
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
            SELECT *
            FROM products AS p
            JOIN product_has_categories AS phc
            ON p.product_id = phc.product_id
            JOIN categories AS c
            ON phc.category_id = c.category_id
            WHERE category_name = %s
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)

    def create_product_has_categories(self, product):
        query = ("""
            SELECT c.category_id, category_name
            FROM categories AS c
            JOIN product_has_categories AS phc
            ON c.category_id = phc.category_id
            JOIN products AS p
            ON phc.product_id = p.product_id
            WHERE product_name = %s
        """)
        data = (product.product_name,)
        self.database_manager.cursor.execute(query, data)
        categories_infos = self.database_manager.cursor.fetchall()
        categories = self.database_manager.categories_manager.create_categories(*categories_infos)

        categories_have_categories = list()
        for category in categories:
            category_has_categories = self.database_manager.category_has_categories_manager.create_category_has_categories(category)
            categories_have_categories.append(category_has_categories)
        return ProductHasCategoriesModel(product, *categories_have_categories)
