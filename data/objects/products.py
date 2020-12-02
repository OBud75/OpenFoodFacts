"""In this file we put all the informations relatives to a product
"""

# Standard library import

# Third party import

# Local application imports
from data.objects.categories import Category
from data.objects.stores import Store

class Product:
    """Class representing a product
    """
    def __init__(self, code, product_name, description, nutrition_grades, category_name, stores):
        self.code = code
        self.product_name = product_name
        self.description = description
        self.nutrition_grades = nutrition_grades
        self.category_name = category_name
        self.stores = stores
        self.link = f"https://world.openfoodfacts.org/product/{code}/{product_name}"
        self.is_saved = False

        # Check if category and score already exist, if yes pick them else create
    
    def __getattr__(self, attr):
        pass

    def get_products_of_category(self):
        pass

    def get_products_of_store(self):
        pass