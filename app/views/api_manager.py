# coding: utf-8
#! /usr/bin/env python3

"""Requests to Openfoodfact's API
"""

# Third party import
import requests

class ApiManager:
    """Collects products data from OpenFoodFacts' API
    """
    def get_categories(self):
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name'] for category in categories_tags if category['name'].startswith("fr:")]

    def get_products_of_categories(self):
        return [requests.get(f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.get_categories()]

    def get_products_list(self):
        products_infos_list = []
        for products in self.get_products_of_categories():
            for product in products:
                if all(product.get(key) for key in ["code", "product_name", "nutrition_grades", "categories_hierarchy"]):
                    product_infos = {key: product.get(key)
                                     for key in ["code", "product_name", "ingredients_text",
                                     "nutrition_grades", "categories_hierarchy", "store_name"]}
                    product_infos["categories_hierarchy"] = [category_name[3:].capitalize().replace("-", " ")
                                                             for category_name in product_infos["categories_hierarchy"]
                                                             if category_name.startswith("fr:")]
                    if not product_infos["categories_hierarchy"]:
                        continue
                    products_infos_list.append(product_infos)
        return products_infos_list
