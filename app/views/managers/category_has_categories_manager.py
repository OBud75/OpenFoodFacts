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
                self.add_to_table(category, child)

    def add_to_table(self, category, child):
        statement = (
            "INSERT INTO category_has_categories"
            "(category_id, child_id)"
            "VALUES (%s, %s)"
        )
        if child:
            data = (category.category_id, child.category_id)
        else:
            data = (category.category_id, None)
        self.database_manager.cursor.execute(statement, data)

    def create_category_has_categories(self, category):
        categories = self.get_categories_in_category(category)
        return CategoryHasCategoriesModel(category, *categories)

    def get_categories_in_category(self, category):
        query = ("""
            SELECT DISTINCT c.category_id, c.category_name
            FROM categories AS c
            JOIN category_has_categories AS chc
            ON c.category_id = chc.child_id
            JOIN categories AS c2
            ON c2.category_id = chc.category_id
            WHERE c2.category_name = %s
        """)
        data = (category.category_name,)
        self.database_manager.cursor.execute(query, data)
        categories_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.categories_manager.create_categories(*categories_infos)
