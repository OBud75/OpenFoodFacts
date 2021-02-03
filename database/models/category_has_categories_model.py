# coding: utf-8
#! /usr/bin/env python3

"""
"""

class CategoryHasCategoriesModel:
    def __init__(self, category, *categories):
        self.category = category
        self.childs = [category for category in categories]
