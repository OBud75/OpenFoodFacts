# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the relationship between categories
The information of each instance of this class
will be injected into the "category_has_categories" table
"""

class CategoryHasCategoriesModel:
    def __init__(self, category, *categories):
        """Initializing instances with their attributes
        The category attribute is the category of a product
        The childs attribute is a list containing
        the categories following the categories put in first attribute
        in the list of product categories linked to this one

        Args:
            category (Category): CategoryModel instance
            categories (List): CategoryModel instances
        """
        self.category = category
        self.childs = [category for category in categories]
