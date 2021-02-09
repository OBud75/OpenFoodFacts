# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager of the "product_has_stores" table
"""

from database.models.product_has_stores_model import ProductHasStoresModel

class ProductHasStoresManager:
    """Manager of the "product_has_stores" table
    This table contains information on the relationships between products and stores
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance of the "product_has_stores" table

        Args:
            database_manager (DatabaseManager): Instance of the database manager
        """
        self.database_manager = database_manager

    def manage(self, product_has_stores):
        """Method called from the database manager
        Checks of the "product_has_stores" table for injections

        Args:
            product_has_stores (ProductHasStoresModel): ProductHasStoresModel instance
        """
        product = product_has_stores.product
        stores = product_has_stores.stores

        product.product_id = self.database_manager.products_manager.get_product_id(product)
        for store in stores:
            if store.store_name is not None:
                store.store_id = self.database_manager.stores_manager.get_store_id(store)
                self.add_to_table(product, store)

    def add_to_table(self, product, store):
        """Injection of information on relations between
        products and stores in the "product_has_stores" table

        Args:
            product (ProductModel): ProductModel instance
            store (StoreModel): StoreModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = (
            "INSERT INTO product_has_stores"
            "(product_id, store_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, store.store_id)
        cursor.execute(statement, data)
        cursor.close()

    def create(self, product):
        """Creates an instance of ProductHasStoresModel
        The arguments are:
        The ProductModel instance
        The names of the stores linked to the product

        Args:
            product (ProductModel): ProductModel instance

        Returns:
            ProductHasStoresModel: ProductHasStoresModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT DISTINCT(store_name)
            FROM stores AS s
            JOIN product_has_stores AS phs
            ON s.store_id = phs.store_id
            WHERE product_id = %s
        """)
        data = (product.product_id,)
        cursor.execute(query, data)
        stores_names = cursor.fetchall()
        cursor.close()
        stores_names = [store_name[0] for store_name in stores_names]
        if stores_names:
            return ProductHasStoresModel(product, *stores_names)
        return None
