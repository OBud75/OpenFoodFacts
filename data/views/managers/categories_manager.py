# coding: utf-8
#! /usr/bin/env python3

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
                WHERE category_name = %s
            """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result != None:
            return result[0]

    def add_to_table(self, category):
        statement = (
            "INSERT INTO categories"
            "(category_name, category_hierarchy)"
            "VALUES (%s, %s)"
        )
        data = (category.category_name, category.category_hierarchy)
        self.database_manager.cursor.execute(statement, data)

    def get_categories(self):
        query = ("""
            SELECT category_name
            FROM categories
            WHERE category_hierarchy = 0
        """)
        self.database_manager.cursor.execute(query)
        categories_names = self.database_manager.cursor.fetchall()
        return [CategoryModel(0, category_name[0]) for category_name in categories_names]

    def get_categories_in_category(self, category):
        query = ("""
            SELECT DISTINCT category_name
            FROM products JOIN product_has_categories JOIN categories
            WHERE product_name IN (SELECT product_name
                                   FROM products JOIN product_has_categories JOIN categories
                                   WHERE category_name = %s)
            AND category_hierarchy = %s
        """)
        data = (category.category_name, category.category_hierarchy + 1)
        self.database_manager.cursor.execute(query, data)
        categories_names = self.database_manager.cursor.fetchall()
        return [CategoryModel(category.category_hierarchy + 1, category_name[0])
                for category_name in categories_names]
