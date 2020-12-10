"""SQL relative table of categories
Each category have differents products
"""

# Standard library import

# Third party import
import requests

# Local application imports

class CategoriesTable():
    """Class representing the table categories
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def create_table(self):
        self.database_manager.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL,
            products INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        self.database_manager.cursor.execute("""
        ALTER TABLE categories
            ADD CONSTRAINT fk_categories_has_products_product_id
            FOREIGN KEY (products)
            REFERENCES products(id),
        ENGINE=INNODB;
        """)

    def fill_table(self):
        for category in self.database_manager.duplicate_checker._categories:
            statement = (
                "INSERT INTO categories"
                "(category_name)"
                "VALUES (%s)"
            )
            data = (
                category.category_name,
            )
            self.database_manager.cursor.execute(statement, data)

    def get_categories(self):
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name'] for category in categories_tags][0:2]
