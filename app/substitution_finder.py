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
            self.display_substitutes()
        elif mode == "3":
            quit()
        self.select_mode()

    def select_category(self):
        categories = self.database_manager.categories_manager.get_categories()
        print("\nCategory list: ")

        indices = list()
        for index, category in enumerate(categories):
            print(f"{index + 1}: {category.category_name}")
            indices.append(index)

        index = None
        while index not in indices:
            index = int(input("\nChoose a category: ")) - 1
        return categories[index]

    def select_product(self, category):
        products = self.database_manager.categories_manager.get_products(category)
        print("\nProduct list: ")

        indices = list()
        for index, product in enumerate(products):
            print(f"{index + 1}: {product.product_name}")
            indices.append(index)

        index = None
        while index not in indices:
            index = int(input("\nSelect a product: ")) - 1
        return products[index]

    def select_substitute(self):
        category = self.select_category()
        product = self.select_product(category)
        print(product)
        substitutes = self.product_has_substitutes_manager.get_substitutes(product)

        indices = list()
        for index, product in enumerate(substitutes):
            print(f"{index + 1}: {product.product_name}")
            indices.append(index + 1)

        index = None
        while index not in indices:
            index = int(input("\nChoose a product in the substitutes list: "))
        substitute = substitutes[index]

        if input("\nSave product? (y|n): ") == "y":
            self.product_has_substitutes_manager.save_substitute(product.product_name, substitute.product_name)

    def display_substitutes(self):
        self.product_has_substitutes_manager.get_products_with_substitutes()
