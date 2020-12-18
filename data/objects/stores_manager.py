"""In this file we put all the informations relatives to a store
"""

# Standard library import

# Third party import

# Local application imports
from data.objects.models.store_model import StoreModel

class StoresManager:
    """Class representing a single store
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self._stores = list()

    def get_store(self, store_name):
        query = ("""
            SELECT store_id
            FROM stores
            WHERE store_name LIKE %s
        """)
        data = (store_name,)
        self.database_manager.cursor.execute(query, data)
        store = self.database_manager.cursor.fetchone()

        if store != None:
            return self.find_existing_store(store_name)
        return self.create_store(store_name)

    #def get_store_id()

    def create_store(self, store_name):
        store = StoreModel(store_name)
        self.add_to_table(store)
        self._stores.append(store)
        return store

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