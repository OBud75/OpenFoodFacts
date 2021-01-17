# coding: utf-8
#! /usr/bin/env python3

"""In this file we define our business model

1 - Quel aliment souhaitez-vous remplacer ?
2 - Retrouver mes aliments substitués.

L'utilisateur sélectionne 1. Le programme pose les questions suivantes à l'utilisateur
et ce dernier sélectionne les réponses :

Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre.
L'utilisateur entre le chiffre correspondant et appuie sur entrée]
Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre.
L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant)
et un lien vers la page d'Open Food Facts concernant cet aliment.
L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.
"""

# Local application imports
from data.views.managers.product_has_substitutes_manager import ProductHasSubstitutesManager

class SubstitutionFinder:
    """Class representing the needs of the user
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.product_has_substitutes_manager = ProductHasSubstitutesManager(self.database_manager)

    def select_mode(self):
        mode = None
        while mode not in ["1", "2", "3"]:
            mode = input("\n\
1 - Quel aliment souhaitez-vous remplacer ?\n\
2 - Retrouver mes aliments substitués.\n\
3 - Quitter le programme\n")
        if mode == "1":
            self.select_substitute()
        elif mode == "2":
            self.display_saved_substitutes()
        elif mode == "3":
            quit()
        self.select_mode()

    def select_category(self):
        categories = self.database_manager.categories_manager.get_categories()
        category = self.select_in_list("categories", categories)

        while self.database_manager.categories_manager.count_products_in_category(category) > 30:
            categories = self.database_manager.category_has_categories_manager.get_categories_in_category(category)
            category = self.select_in_list("categories", categories)
        return category

    def select_product(self, category):
        products = self.database_manager.product_has_categories_manager.get_products_in_category(category)
        return self.select_in_list("products", products)

    def select_substitute(self):
        category = self.select_category()
        product = self.select_product(category)

        product_has_substitutes = self.product_has_substitutes_manager.get_substitutes_of_product(product)
        substitutes = product_has_substitutes.substitutes
        substitute = self.select_in_list("substitutes", substitutes)

        # Asks if the user wants to save his choice
        if substitute:
            answer = None
            while answer not in ["y", "n"]:
                answer = input("\nSave product? (y|n): ")
            if answer == "y":
                self.product_has_substitutes_manager.save_substitute(product, substitute)

    def display_saved_substitutes(self):
        products = self.product_has_substitutes_manager.get_products_with_substitutes()
        product = self.select_in_list("products", products)
        for product in self.product_has_substitutes_manager.get_saved_substitutes_of_product(product):
            print(product.product_name)

    def select_in_list(self, mode, inputs):
        indices = list()
        if mode == "products" or mode == "substitutes":
            for index, product in enumerate(inputs):
                print(f"{index + 1}: {product.product_name}")
                indices.append(index + 1)

        elif mode == "categories":
            for index, category in enumerate(inputs):
                print(f"{index + 1}: {category.category_name}")
                indices.append(index + 1)

        if not indices:
            print(f"Sorry, no {mode} for this product")
            self.select_mode()

        index = None
        while index not in indices:
            index = input(f"\nMake your selection in the {mode} list: ")
            if index.isdigit():
                index = int(index)
        return inputs[index - 1]
