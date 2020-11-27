"""In this file we put all the informations relatives to a store
"""

# Standard library import

# Third party import

# Local application imports
from data.tables.stores_table import StoresTable

class Store:
    """Class representing a single store
    """
    def __init__(self, store_name):
        self.store_name = store_name
        self.stores_table = StoresTable()

    def get_stores_of_product(self, product):
        pass
        """SELECT product
            FROM stores
            WHERE"""