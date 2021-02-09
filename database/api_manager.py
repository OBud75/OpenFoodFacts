# coding: utf-8
#! /usr/bin/env python3

"""Managing communication with the OpenFoodFacts API
We use the requests module
"""

# Third party import
import requests

# Local application imports
from database import constants

class ApiManager:
    """Object representing the communication manager with the OpenFoodFacts API
    """
    def get_categories(self):
        """Retrieving the names of the categories
        We filter to have only those starting with "fr"

        Returns:
            List: Categories names
        """
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name']
                for category in categories_tags
                if category['name'].startswith("fr:")]

    def get_products_of_categories(self):
        """Retrieving the names of the products of each category

        Returns:
            List: Names of products of all categories
        """
        return [requests.get(
            f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.get_categories()]

    def get_products_list(self):
        """Retrieving information for each product

        Returns:
            List: List of dictionaries containing product information
        """
        products_infos_list = list()
        for products in self.get_products_of_categories():
            for product in products:
                if all(product.get(key) for key in constants.API_MANDATORY_INFORMATIONS):
                    product_infos = {key: product.get(key)
                                     for key in constants.API_INFORMATIONS}

                    # Standardization of store names
                    if product_infos["stores_tags"]:
                        product_infos["stores_tags"] = [
                                store_name.capitalize().replace("-", " ")
                                for store_name in product_infos["stores_tags"]
                                if store_name
                                ]

                    # Sorting categories and standardizing their names
                    product_infos["categories_hierarchy"] = [
                        category_name[3:].capitalize().replace("-", " ")
                        for category_name in product_infos["categories_hierarchy"]
                        if category_name.startswith("fr:")
                        ]

                    if not product_infos["categories_hierarchy"]:
                        continue
                    products_infos_list.append(product_infos)
        return products_infos_list
