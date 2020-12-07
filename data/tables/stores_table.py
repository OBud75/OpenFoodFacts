"""SQL relative table of stores
Each store have products you can buy
"""

# Standard library import

# Third party import

# Local application imports

class StoresTable():
    """Class representing the table stores
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def create_table(self):
        self.database_manager.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            store_name VARCHAR(45),
            product INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        self.database_manager.cursor.execute("""
        ALTER TABLE stores
            ADD CONSTRAINT fk_stores_has_products_product_code
            FOREIGN KEY (product)
            REFERENCES products(id),
        ENGINE=INNODB;
        """)

    def fill_table(self):
        for store in self.database_manager.singleton_checker._stores:
            statement = (
                "INSERT INTO stores"
                "(store_name)"
                "VALUES (%s)"
            )
            data = (
                store.store_name,
            )
            self.database_manager.cursor.execute(statement, data)

    def get_stores_of_product(self, product_name):
        pass
