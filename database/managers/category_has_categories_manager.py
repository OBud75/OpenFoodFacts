# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager of the "category_has_categories" table
"""

# Local application imports
from mysql.connector.cursor import CursorBase
from database.models.category_has_categories_model import CategoryHasCategoriesModel

class CategoryHasCategoriesManager():
    """Manager of the "category_has_categories" table
    This table contains information on the relationships between categories
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance
        of the "category_has_categories" table

        Args:
            database_manager (DatabaseManager): Instance of the database manager
        """
        self.database_manager = database_manager

    def manage(self, *categories_have_categories):
        """Method called from the database manager
        Checks of the "category_has_categories" table for injections

        Args:
            categories_have_categories (List): CategoryHasCategoriesModel instance
        """
        # Category related to product
        for category_has_categories in categories_have_categories:
            category = category_has_categories.category
            category.category_id = self.database_manager.categories_manager.get_id(category)

            # Categories related to product category
            for child in category_has_categories.childs:
                if child:
                    child.category_id = self.database_manager.categories_manager.get_id(child)
                    if not self.is_in_table(category, child):
                        self.add_to_table(category, child)

    def add_to_table(self, category, child):
        """Injection of information into the "category_has_categories" table

        Args:
            category (CategoryModel): CategoryModel instance linked to the product
            child (CategoryModel): Category instance linked to the category
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = (
            "INSERT INTO category_has_categories"
            "(category_id, child_id)"
            "VALUES (%s, %s)"
        )
        data = (category.category_id, child.category_id)
        cursor.execute(statement, data)
        cursor.close()

    def is_in_table(self, category, child):
        """Search in the "category_has_categories" table to find out
        if the relationship between categories is already saved

        Args:
            category (CategoryModel): CategoryModel instance linked to the product
            child (CategoryModel): Category instance linked to the category

        Returns:
            Bool: Is the relationship already registered?
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT *
            FROM category_has_categories
            WHERE category_id = %s
            AND child_id = %s
        """)
        data = (category.category_id, child.category_id)
        cursor.execute(query, data)
        is_saved = cursor.fetchall()
        cursor.close()
        if is_saved:
            return True
        return False

    def create(self, category):
        """Creating a CategoryHasCategories instance
        Representing categories linked to a given category

        Args:
            category (CategoryModel): Category of which we want linked categories

        Returns:
            CategoryHasCategoryModel: Link between a category and those linked to it
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT chc.child_id, category_name
            FROM categories AS c
            JOIN category_has_categories as chc
            ON chc.child_id = c.category_id
            WHERE chc.category_id = %s;
        """)
        data = (category.category_id,)
        cursor.execute(query, data)
        categories_infos = cursor.fetchall()
        cursor.close()

        # Creation of CategoryModel instances
        categories = self.database_manager.categories_manager.create_categories(*categories_infos)
        return CategoryHasCategoriesModel(category, *categories)
