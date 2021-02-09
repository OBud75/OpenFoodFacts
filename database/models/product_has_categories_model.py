# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the relationship between products and categories
The information of each instance of this class
will be injected into the "product_has_categories" table
"""

class ProductHasCategoriesModel:
    def __init__(self, product, *categories_have_categories):
        """Initializing instances with their attributes
        Args:
            product (Product): Product instance to which the categories are associated
            categories_have_categories (List): Associated CategoryHasCategories instances
        """
        self.product = product
        self.categories_have_categories = [category_has_categories
                                           for category_has_categories
                                           in categories_have_categories]
