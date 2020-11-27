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

# Standard library import

# Third party import

# Local application imports

class SubstitutionFinder():
    """Class representing the needs of the user
    """
    def __init__(self):
        pass

    def find_better_nutri_scores(self, product):
        recommended_products = []
        return recommended_products

    def get_mode(self):
        return input("1 - Quel aliment souhaitez-vous remplacer ?\n\
                      2 - Retrouver mes aliments substitués.")

    def show_substitutions(self):
        pass

    def main_loop(self):
        while not self.get_mode.isdigit():
            self.get_mode()
        if self.get_mode() ==


# input_categories = SELECT category FROM categories WHERE product_id in (SELECT id FROM products WHERE name = name)
# input_substitutions = SELECT name FROM products WHERE id IN (SELECT product_id FROM categories WHERE category IN input_categories)
