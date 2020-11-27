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
    def __init__(self, product_id, name, description, nutri_score, link, category, score):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.nutri_score = nutri_score
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