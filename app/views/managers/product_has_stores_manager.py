# coding: utf-8
#! /usr/bin/env python3

"""
"""

from app.views.models.product_has_stores_model import ProductHasStoresModel


class ProductHasStoresManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product_has_stores):
        product = product_has_stores.product
        stores = product_has_stores.stores

        product.product_id = self.database_manager.products_manager.get_product_id(product)
        for store in stores:
            if store.store_name != None:
                store.store_id = self.database_manager.stores_manager.get_store_id(store)
                self.add_to_table(product, store)

    def add_to_table(self, product, store):
        statement = (
            "INSERT INTO product_has_stores"
            "(product_id, store_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, store.store_id)
        self.database_manager.cursor.execute(statement, data)

    def create_product_has_stores(self, product):
        query = ("""
            SELECT *
            FROM stores AS s
            JOIN product_has_stores AS phs
            ON s.store_id = phs.store_id
            WHERE product_id = %s
        """)
        data = (product.product_id,)
        self.database_manager.cursor.execute(query, data)
        stores_infos = self.database_manager.cursor.fetchall()
        if stores_infos:
            return ProductHasStoresModel(product, *stores_infos)
