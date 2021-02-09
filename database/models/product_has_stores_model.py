# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the relationship between products and stores
The information of each instance of this class
will be injected into the "product_has_stores" table
"""

# Local application imports
from database.models.store_model import StoreModel

class ProductHasStoresModel:
    """Initializing instances
    The product attribute is a ProductModel object instance
    We create StoreModel instances for the stores attribute

    Args:
        product (Product): Product for which we have stores associated
        stores_names (Str): Name of associated stores
    """
    def __init__(self, product, *stores_names):
        self.product = product
        self.stores = [StoreModel(store_name) for store_name in stores_names]
