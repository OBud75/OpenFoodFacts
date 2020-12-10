"""In this file we put all the informations relatives to a product
"""

# Standard library import

# Third party import

# Local application imports

class Product:
    """Class representing a product
    """
    def __init__(self, database_manager, **product_infos):
        """Initializing instances of products
        Category and store attribute are instances of their respectives class
        We want them to be singleton

        Args:
            singleton_checker ([type]): [description]
        """
        self.database_manager = database_manager

        self.code = product_infos.get("code")
        self.product_name = product_infos.get("product_name")
        self.description = product_infos.get("description")
        self.nutrition_grades = product_infos.get("nutrition_grades", "?")
        self.link = f"https://world.openfoodfacts.org/product/{self.code}/{self.product_name.replace(' ', '-')}"

        # Creating singleton instances for category and store
        self.category_name = self.database_manager.duplicate_checker.create_category(product_infos.get("category_name")).category_name
        self.store_name = self.database_manager.duplicate_checker.create_store(product_infos.get("store_name")).store_name

    def get_products_of_category(self):
        pass

    def get_products_of_store(self):
        pass
