# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from database.models.store_model import StoreModel

class ProductHasStoresModel:
    def __init__(self, product, *stores_names):
        self.product = product
        self.stores = [StoreModel(store_name) for store_name in stores_names]
