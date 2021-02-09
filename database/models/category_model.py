# coding: utf-8
#! /usr/bin/env python3

"""Category model implementation
The information of each instance of this class
will be injected into the "categories" table
"""

class CategoryModel:
    def __init__(self, category_name, category_id=None):
        """Initializing instances with their attributes

        Args:
            category_name (Str): Category name
            category_id (Int, optional): ID in the database. Defaults to None.
        """
        if category_id:
            self.category_id = category_id
        self.category_name = category_name
