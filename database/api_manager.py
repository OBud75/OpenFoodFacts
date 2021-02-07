# coding: utf-8
#! /usr/bin/env python3

"""Gestion de la communication avec L'API OpenFoodFacts
Nous utilisons du module requests
"""

# Third party import
import requests

# Local application imports
from database import constants

class ApiManager:
    """Objet représentant le gestionnaire de la communication avec l'API OpenFoodFacts
    """
    def get_categories(self):
        """Récupération des noms des catégories
        Nous filtrons pour avoir uniquement celles commencant par "fr"

        Returns:
            List: Nom des catégories
        """
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name']
                for category in categories_tags
                if category['name'].startswith("fr:")]

    def get_products_of_categories(self):
        """Récupération des noms des produits de chaque catégorie

        Returns:
            List: Noms des noms des produits de toutes les catégories
        """
        return [requests.get(
            f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.get_categories()]

    def get_products_list(self):
        """Récupérations des informations de chaque produit

        Returns:
            List: Liste de dictionnaires contenant les informations des produits
        """
        products_infos_list = list()
        for products in self.get_products_of_categories():
            for product in products:
                if all(product.get(key) for key in constants.API_MANDATORY_INFORMATIONS):
                    product_infos = {key: product.get(key)
                                     for key in constants.API_INFORMATIONS}

                    # Uniformisation des noms des magasins
                    product_infos["stores_tags"] = [
                            store_name.capitalize().replace("-", " ")
                            for store_name in product_infos["stores_tags"]
                        ]

                    # Tri des catégories et uniformisation de leurs noms
                    product_infos["categories_hierarchy"] = [
                        category_name[3:].capitalize().replace("-", " ")
                        for category_name in product_infos["categories_hierarchy"]
                        if category_name.startswith("fr:")
                        ]

                    if not product_infos["categories_hierarchy"]:
                        continue
                    products_infos_list.append(product_infos)
        return products_infos_list
