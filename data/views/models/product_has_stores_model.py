# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from data.views.models.store_model import StoreModel

class ProductHasStores:
    def __init__(self, product, *product_stores):
        self.product = product
        self.stores = [StoreModel(store_name) for store_name in product_stores]
