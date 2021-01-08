"""In this file we put all the informations relatives to a store
"""

# Local application imports
from data.views.models.store_model import StoreModel

class StoresManager:
    """Class representing a single store
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, *product_has_stores):
        for store in product_has_stores:
            if store.store_name and self.get_store_id_by_name(store) == None:
                self.add_to_table(store)

    def get_store_id_by_name(self, store):
        query = ("""
            SELECT store_id
            FROM stores
            WHERE store_name LIKE %s
        """)
        data = (store.store_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result != None:
            return result[0]

    def add_to_table(self, store):
        statement = (
            "INSERT INTO stores"
            "(store_name)"
            "VALUES (%s)"
        )
        data = (store.store_name,)
        self.database_manager.cursor.execute(statement, data)
