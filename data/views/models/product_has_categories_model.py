# coding: utf-8
#! /usr/bin/env python3

"""
"""

class ProductHasCategoriesModel:
    def __init__(self, product, *categories_have_categories):
        self.product = product
        self.categories_have_categories = [category_has_categories
                                           for category_has_categories
                                           in categories_have_categories]
