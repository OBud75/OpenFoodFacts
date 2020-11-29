"""In this file we put all the informations relatives to a product
"""

# Standard library import

# Third party import

# Local application imports
from data.objects.categories import Category
from data.objects.stores import Store

class Product:
    """Class representing a single product
    """
    def __init__(self, code, product_name, stores, nutrition_grades, description, link):
        self.code = code
        self.product_name = product_name
        self.stores = stores
        self.nutrition_grades = nutrition_grades
        self.description = description
        self.link = link

        # Check if category and score already exist, if yes pick them else create
        if Category().category_name:
            pass 
        if Store().store_name:
            pass

    def get_products_of_category(self):
        pass

    def get_products_of_store(self):
        pass