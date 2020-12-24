"""In this file we put all the informations relatives to a store
"""

# Standard library import

# Third party import

# Local application imports
from data.views.models.store_model import StoreModel

class StoresManager:
    """Class representing a single store
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage_stores(self, stores):
        for store in stores:
            if self.get_store_id_by_name(store) == None:
                self.add_to_table(store)

    def get_store_id_by_name(self, store):
        query = ("""
            SELECT store_id
            FROM stores
            WHERE store_name LIKE %s
        """)
        data = (store.store_name,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchone()

    def add_to_table(self, store):
        statement = (
            "INSERT INTO stores"
            "(store_name)"
            "VALUES (%s)"
        )
        data = (
            store.store_name,
        )
        self.database_manager.cursor.execute(statement, data)

"""
        SI self.pk:
            UPDATE categories SET nom = self.name WHERE pk = self.pk
        SINON
            INSERT INTO categories ('nom') VALUES (self.name)
            self.pk = retour_sql['pk']
"""