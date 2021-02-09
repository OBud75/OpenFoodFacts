# coding: utf-8
#! /usr/bin/env python3

"""Store model implementation
The information of each instance of this class
will be injected into the "stores" table
"""

class StoreModel:
    """Model of a store
    """
    def __init__(self, store_name, store_id=None):
        """The information relating to a store is
        The name of the store
        The store ID in the database

        Args:
            store_name (Str): Name of the shop
            store_id (Int, optional): Store ID in the database. None by default.
        """
        if store_id:
            self.store_id = store_id
        self.store_name = store_name
