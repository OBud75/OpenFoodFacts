"""SQL relative table of products
Each product have an Id, a name,
A small description, and a link to the product
"""

# Standard library import

# Third party import
import requests

# Local application imports
from data.tables.categories_table import CategoriesTable
from data.objects.products_manager import ProductsManager

class ProductsTable:
    """Class representing the table products
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.products_manager = ProductsManager(self.database_manager)

        # Intantiation of the relatives tables
        self.categories_table = CategoriesTable(self.database_manager)
    
    def create_table(self):
        self.database_manager.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            code BIGINT UNSIGNED,
            product_name VARCHAR(100) NOT NULL,
            ingredients_text TEXT(100),
            nutrition_grades VARCHAR(1) NOT NULL,
            link VARCHAR(150) NOT NULL,
            category_name VARCHAR(500) NOT NULL,
            category_id INT UNSIGNED,
            store_name VARCHAR(45),
            store_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        self.database_manager.cursor.execute("""
        ALTER TABLE products
            ADD CONSTRAINT fk_products_has_categories_category_id
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id),

            ADD CONSTRAINT fk_products_has_stores_store_name
            FOREIGN KEY (store_id)
            REFERENCES stores(store_id),

            ADD CONSTRAINT fk_products_has_substitutes
            FOREIGN KEY (id)
            REFERENCES products(id),
        ENGINE=INNODB;
        """)

    def get_products_of_categories(self):
        return {category: requests.get(f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.categories_table.get_categories()}

    def get_products_list(self):
        products_infos_list = []
        for category, products in self.get_products_of_categories().items():
            for product in products:
                product_infos = {key: product.get(key)
                                 for key in ["code", "product_name", "description", "nutrition_grades", "store_name"]
                                 if product.get(key) != None}
                product_infos["category_name"] = category
                products_infos_list.append(product_infos)
        return products_infos_list
