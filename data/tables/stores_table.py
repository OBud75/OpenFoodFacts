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
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def create_table(self):
        self.database_manager.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED PRIMARY KEY,
            store_name VARCHAR(45),
            product BIGINT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        self.database_manager.cursor.execute("""
        ALTER TABLE stores
            ADD CONSTRAINT fk_stores_has_products_product_code
            FOREIGN KEY (product)
            REFERENCES products(code),
        ENGINE=INNODB;
        """)

    def fill_table(self):
        # for store in x:
        #   self.database_manager.insert_into_table("stores", column, value)
        pass

    def get_stores_of_product(self, product_name):
        pass
