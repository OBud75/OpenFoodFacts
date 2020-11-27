"""SQL relative table of stores
Each store have products you can buy
"""

# Standard library import

# Third party import

# Local application imports
import mysql.connector

class StoresTable():
    """Class representing the table stores
    """
    def __init__(self, data_base):
        self.data_base = data_base

    def create_table(self):
        self.data_base.cursor.execute("""
        CREATE TABLE stores (
            store_name TEXT NOT NULL,
            product_id SMALLINT UNSIGNED NOT NULL,
            FOREIGN KEY (category) REFERENCES products (id));
        """)

    def fill_table(self):
        for store in stores.split(", "):
            "INSERT INTO stores (store_name, product_id) VALUES (?, ?)", store, id;

    def get_stores_of_product(self, product_name):
        pass
