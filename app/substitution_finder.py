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
            category = self.get_category()
            product_name = self.get_product(category)
            self.get_substitute(product_name, category)
        elif mode == "2":
            self.display_substitutes()
        elif mode == "3":
            quit()
        self.select_mode()

    def get_category(self):
        query = ("""
            SELECT category_name
            FROM categories
        """)
        self.database_manager.cursor.execute(query)
        categories = self.database_manager.cursor.fetchall()

        print("\nCategory list: ")
        for number, category in enumerate(categories):
            print(f"{number + 1}: {category[0]}")
        index = int(input("\nChoose a category: ")) - 1
        return categories[index][0]

    def get_product(self, category_name):
        query = ("""
            SELECT product_name
            FROM products JOIN categories
            WHERE category_name = %s
        """)
        data = (category_name,)
        self.database_manager.cursor.execute(query, data)
        products_names = self.database_manager.cursor.fetchall()

        print("\nProduct list: ")
        for number, product_name in enumerate(products_names):
            print(f"{number + 1}: {product_name[0]}")
        index = int(input("\nSelect a product: ")) - 1
        return products_names[index]

    def get_substitute(self, product_name, category_name):
        results = self.product_has_substitutes_manager.get_substitutes_of_product_in_category(product_name, category_name)
        numbers = []
        for number, product in enumerate(results):
            print(f"{number + 1}: {[product[i] for i in range(len(product))]}")
            numbers.append(number + 1)

        index = None
        while index not in numbers:
            index = int(input("\nChoose a product in the substitutes list: "))

        substitute = results[index]
        if input("\nSave product? (y|n) :") == "y":
            self.product_has_substitutes_manager.save_substitute(product_name[0], substitute[0])
        return results[index]

    def display_substitutes(self):
        self.product_has_substitutes_manager.get_products_with_substitutes()
