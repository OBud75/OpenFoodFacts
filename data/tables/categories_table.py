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
    def __init__(self, cursor):
        self.cursor = cursor
        self.categories = self.get_categories()

    def get_categories(self):
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name'] for category in categories_tags]

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE categories (
            category TEXT NOT NULL,
            product_id SMALLINT UNSIGNED NOT NULL,
            FOREIGN KEY (category) REFERENCES products (id);
        """)

    def fill_table(self):
        for category in self.categories:
            self.cursor.execute(f"""
            INSERT INTO categories (category_id, category)
            VALUES ({category_id}, {category});
            """)
