# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from data.views.models.category_model import CategoryModel

class ProductHasCategories:
    def __init__(self, product, *product_categories):
        self.product = product
        self.categories = [CategoryModel(category_hierarchy, category_name)
                           for category_hierarchy, category_name in enumerate(product_categories)]
