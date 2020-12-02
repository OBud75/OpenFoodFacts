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
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def get_mode(self):
        return input("1 - Quel aliment souhaitez-vous remplacer ?\n\
2 - Retrouver mes aliments substitués.\n")

    def display_substitutions(self):
        pass

    def recommend_product(self, product, category):
        # nutritional_grade = get_nutritional_grades(product)
        # recommendations = get_recommendations(nutritional_grade, category)
        # return recommendations
        pass
    
    def get_nutritional_grades(self, product):
        pass
        # return nutritional_grade
    
    def get_recommendations(self, nutritional_grade, category):
        pass
    
    def get_category(self):
        pass

    def get_product(self, category):
        pass

    def main_loop(self):
        mode = None
        while mode not in ["1", "2"]:
            mode = self.get_mode()
        if mode == "1":
            category = self.get_category()
            product = self.get_product(category)
            self.recommend_product(product, category)
        elif mode == "2":
            self.display_substitutions()


# input_categories = SELECT category FROM categories WHERE product_id in (SELECT id FROM products WHERE name = name)
# input_substitutions = SELECT name FROM products WHERE id IN (SELECT product_id FROM categories WHERE category IN input_categories)
