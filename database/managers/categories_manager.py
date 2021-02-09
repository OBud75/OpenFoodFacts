# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager of the "categories" table
"""

# Local application imports
from database.models.category_model import CategoryModel

class CategoriesManager:
    """Manager of the "categories" table
    This table contains information about the categories
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance of the "categories" table

        Args:
            database_manager (DatabaseManager): Instance of the database manager
        """
        self.database_manager = database_manager

    def manage(self, *categories):
        """Method called from the database manager
        We add the categories to the database if they are not already there
        """
        for category in categories:
            if not self.get_id(category):
                self.add_to_table(category)

    def get_id(self, category):
        """Retrieving the ID of a category from its name

        Args:
            category (CategoryModel): CategoryModel instance

        Returns:
            Int: Category ID in the database
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
                SELECT category_id
                FROM categories
                WHERE category_name = %s
            """)
        if category:
            data = (category.category_name,)
            cursor.execute(query, data)
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                return result[0]
        return None

    def add_to_table(self, category):
        """Injection of a category into the "categories" table

        Args:
            category (CategoryModel): CategoryModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (category.category_name,)
        cursor.execute(statement, data)
        cursor.close()

    def create_categories(self, *categories_infos):
        """Creates instances of the CategoryModel object

        Args:
            categories_infos (List): Categories informations

        Returns:
            List: CategoryModel instances
        """
        categories = list()
        for category_infos in categories_infos:
            category = self.create(category_infos)
            categories.append(category)
        return categories

    def create(self, category_infos):
        """Creates an instance of the CtaegoryModel object
        Adaptation according to the amount of information available

        Args:
            category_infos (List): Category information in the database

        Returns:
            CategoryModel: CategoryModel instance
        """
        # If we know the name and the ID of the category
        if len(category_infos) == 2:
            category = CategoryModel(category_name=category_infos[1],
                                     category_id=category_infos[0])

        # If we only know the name of the category
        elif len(category_infos) == 1:
            category = CategoryModel(category_name=category_infos[0])
            category.category_id = self.get_id(category)
        else:
            category = CategoryModel(category_name=category_infos)
            category.category_id = self.get_id(category)
        return category
