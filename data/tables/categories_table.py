"""SQL relative table of categories
Each category have differents products
"""

# Standard library import

# Third party import
import requests

# Local application imports
from data.objects.categories import Category

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
            products BIGINT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        self.database_manager.cursor.execute("""
        ALTER TABLE categories
            ADD CONSTRAINT fk_categories_has_products_product_code
            FOREIGN KEY (products)
            REFERENCES products(code),
        ENGINE=INNODB;
        """)

    def fill_table(self):
        for category in self.create_categories():
            self.database_manager.insert_into_table("categories", "category_name", category.category_name)

    def get_categories(self):
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name'] for category in categories_tags][0:2]

    def create_categories(self):
        return [Category(name) for name in self.get_categories()]
