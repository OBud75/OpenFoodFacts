# coding: utf-8
#! /usr/bin/env python3

"""
"""

class StoreModel:
    def __init__(self, store_name, store_id=None):
        if store_id:
            self.store_id = store_id
        self.store_name = store_name
