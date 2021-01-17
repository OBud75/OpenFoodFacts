# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from data.views.models.category_model import CategoryModel

class CategoryHasCategoriesModel:
    def __init__(self, category, *categories):
        self.category = category
        self.childs = [category for category in categories]
