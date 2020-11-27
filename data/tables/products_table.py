"""SQL relative table of products
Each product have an Id, a name,
A small description, and a link to the product
"""

# Standard library import

# Third party import
import requests


# Local application imports
from data.objects.products import Product
from data.tables.categories_table import CategoriesTable

class ProductsTable:
    """Class representing the table products
    """
    def __init__(self, data_base):
        self.data_base = data_base
        self.products_list = []
        self.categories_table = CategoriesTable()
    
    def create_table(self):
        self.data_base.cursor.execute("""
        CREATE TABLE products (
            category TEXT NOT NULL,
            product_id SMALLINT UNSIGNED NOT NULL,
            FOREIGN KEY (category) REFERENCES products (id);
        """)

    def get_products_of_categories(self):
        return {category: requests.get(f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.categories_table.get_categories()}

    def create_products(self):
        for category, products in self.get_products_of_categories().items():
            for product in products:
                code = product.get('code')
                name = product.get('product_name')
                description = []
                stores = product.get('stores')
                nutri_score  = product.get('nutrition_grades')
                link = f"https://world.openfoodfacts.org/product/{code}/{name}"

                new_product = Product(code, name, description, nutri_score, link)
                self.products_list.append(new_product)


if __name__ == "__main__":
    test = ProductsTable()
    test.create_products()
    for product in test.products_list:
        print(product.name)
