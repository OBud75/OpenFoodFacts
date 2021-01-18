# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from app.views.models.category_model import CategoryModel

class CategoriesManager:
    """Link between categories and database
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, *categories):
        for category in categories:
            if not self.get_category_id(category):
                self.add_to_table(category)

    def get_category_id(self, category):
        query = ("""
                SELECT category_id
                FROM categories
                WHERE category_name = %s
            """)
        if category:
            data = (category.category_name,)
            self.database_manager.cursor.execute(query, data)
            result = self.database_manager.cursor.fetchone()
            if result != None:
                return result[0]
        return None

    def add_to_table(self, category):
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (category.category_name,)
        self.database_manager.cursor.execute(statement, data)

    def get_categories(self):
        self.database_manager.cursor.execute("""
            SELECT *
            FROM categories
        """)
        categories_infos = self.database_manager.cursor.fetchall()
        return self.create_categories(*categories_infos)

    def count_products_in_category(self, category):
        query = ("""
            SELECT COUNT(*)
            FROM product_has_categories AS phc
            INNER JOIN (SELECT category_id
                        FROM categories
                        WHERE category_name = %s) AS c
            ON phc.category_id = c.category_id
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchone()[0]

    def create_categories(self, *categories_infos):
        categories = list()
        for category_infos in categories_infos:
            if len(category_infos) == 2:
                category = CategoryModel(category_name=category_infos[1],
                                         category_id=category_infos[0])
                categories.append(category)
            elif len(category_infos) == 1:
                category = CategoryModel(category_infos[0])
                category.category_id = self.get_category_id(category)
                categories.append(category)
        return categories
