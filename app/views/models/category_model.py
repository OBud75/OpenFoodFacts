# coding: utf-8
#! /usr/bin/env python3

"""
"""

class CategoryModel:
    def __init__(self, category_name, category_id=None):
        if category_id:
            self.category_id = category_id
        self.category_name = category_name
