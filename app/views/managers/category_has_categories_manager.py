# coding: utf-8
#! /usr/bin/env python3

"""
"""

# 
from app.views.models.category_has_categories_model import CategoryHasCategoriesModel

class CategoryHasCategoriesManager():
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, *categories_have_categories):
        for category_has_categories in categories_have_categories:
            category = category_has_categories.category
            category.category_id = self.database_manager.categories_manager.get_category_id(category)
            for child in category_has_categories.childs:
                if child:
                    child.category_id = self.database_manager.categories_manager.get_category_id(child)
                    if not self.is_in_table(category, child):
                        self.add_to_table(category, child)

    def add_to_table(self, category, child):
        statement = (
            "INSERT INTO category_has_categories"
            "(category_id, child_id)"
            "VALUES (%s, %s)"
        )
        data = (category.category_id, child.category_id)
        self.database_manager.cursor.execute(statement, data)

    def is_in_table(self, category, child):
        query = ("""
            SELECT *
            FROM category_has_categories
            WHERE category_id = %s
            AND child_id = %s
        """)
        data = (category.category_id, child.category_id)
        self.database_manager.cursor.execute(query, data)
        if self.database_manager.cursor.fetchall():
            return True

    def create_category_has_categories(self, category):
        query = ("""
            SELECT chc.child_id, category_name
            FROM categories AS c
            JOIN category_has_categories as chc
            ON chc.child_id = c.category_id
            WHERE chc.category_id = %s;
        """)
        data = (category.category_id,)
        self.database_manager.cursor.execute(query, data)
        categories_infos = self.database_manager.cursor.fetchall()
        categories = self.database_manager.categories_manager.create_categories(*categories_infos)
        return CategoryHasCategoriesModel(category, *categories)
