# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the "stores" table manager
"""

class StoresManager:
    """Manager of the "stores" table
    This table contains information about the stores
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance of the "stores" table

        Args:
            database_manager (DatabaseManager): Database manager
        """
        self.database_manager = database_manager

    def manage(self, *stores):
        """Method called from the database manager
        We add stores to the database if they are not already there
        """
        for store in stores:
            if store.store_name and self.get_store_id(store) is None:
                self.add_to_table(store)

    def get_store_id(self, store):
        """Retrieving the ID of a store from its name

        Args:
            store (StoreModel): StoreModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT store_id
            FROM stores
            WHERE store_name LIKE %s
        """)
        data = (store.store_name,)
        cursor.execute(query, data)
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            return result[0]
        return None

    def add_to_table(self, store):
        """Injection of a store in the "stores" table

        Args:
            store (Store): StoreModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = (
            "INSERT INTO stores"
            "(store_name)"
            "VALUES (%s)"
        )
        data = (store.store_name,)
        cursor.execute(statement, data)
        cursor.close()
