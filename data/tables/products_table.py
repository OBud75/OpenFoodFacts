"""SQL relative table of products
Each product have an Id, a name,
A small description, and a link to the product
"""

# Standard library import

# Third party import
import requests

# Local application imports
from data.tables import constants
from data.objects.products import Product
from data.tables.categories_table import CategoriesTable

class ProductsTable:
    """Class representing the table products
    """
    def __init__(self, cursor):
        self.cursor = cursor

        # Intantiation of the relatives tables
        self.categories_table = CategoriesTable(self.cursor)
    
    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            code INT UNSIGNED NOT NULL UNIQUE INDEX,
            product_name VARCHAR(45) NOT NULL,
            description TEXT(100) NOT NULL,
            nutrition_grades VARCHAR(1) NOT NULL,
            stores VARCHAR(45) NOT NULL,
            link VARCHAR(45) NOT NULL,
            categories_names VARCHAR(255) NOT NULL,
            PRIMARY KEY (code),
            FOREIGN KEY (categories_name) REFERENCES products (id),
            FOREIGN KEY (stores) REFERENCES products (id);
        """)

    def get_products_of_categories(self):
        return {category: requests.get(f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.categories_table.get_categories()}

    def get_products_list(self):
        products_list = []
        for category, products in self.get_products_of_categories().items():
            for product in products:
                for column in constants.PRODUCT_INFOS:
                    column = product.get(column)
                link = f"https://world.openfoodfacts.org/product/{code}/{product_name}"
                # categories = category

                new_product = Product((column for column in constants.PRODUCT_INFOS), link)
                products_list.append(new_product)

    def fill_table(self):
        for product in self.get_products_list():
            self.cursor.execute(f"""
            INSERT INTO products ({column for column in constants.PRODUCT_INFOS})
            VALUES ({product.column for column in constants.PRODUCT_INFOS});
            """)