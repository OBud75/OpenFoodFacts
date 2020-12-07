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
2 - Retrouver mes aliments substitués.\n\
3 - Quitter le programme\n")

    def display_substitutions(self):
        query = ("""
            SELECT product_name
            FROM products
            WHERE 
        """)
        data = (, )
        self.database_manager.cursor.execute(query, data)
        results = self.database_manager.cursor.fetchall()[0]
        return results

    def get_substitutions(self, product_name, category):
        query = ("""
            SELECT product_name, link, store_name
            FROM products
            WHERE nutrition_grades < %s
            AND category_name LIKE %s
            ORDER BY nutrition_grades
        """)
        data = (self.get_nutrition_grades(product_name), category)
        self.database_manager.cursor.execute(query, data)
        results = self.database_manager.cursor.fetchall()

        numbers = []
        for number, product in enumerate(results):
            print(f"{number + 1}: {[product[i] for i in range(len(product))]}")
            numbers.append(number + 1)

        index = None
        while index not in numbers:
            index = int(input("\nChoose a product in the substitutes list: "))

        substitute = results[index]
        if input("\nSave product? (y|n) :") == "y":
            self.save_substitution(product_name, substitute)
        return results[index]

    def save_substitution(self, product_name, substitute):
        query = ("""
            ALTER %s
            FROM products
            WHERE product_name LIKE %s
        """)
        data = (substitute, product_name)
        self.database_manager.cursor.execute(query, data)

    def get_nutrition_grades(self, product_name):
        query = ("""
            SELECT nutrition_grades
            FROM products
            WHERE product_name LIKE %s
        """)
        data = (product_name,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchone()[0]
    
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

    def get_product(self, category):
        query = ("""
            SELECT product_name
            FROM products
            WHERE category_name LIKE %s
        """)
        data = (category,)
        self.database_manager.cursor.execute(query, data)
        products = self.database_manager.cursor.fetchall()

        print("\nProduct list: ")
        for number, product in enumerate(products):
            print(f"{number + 1}: {product}")
        index = int(input("\nChoose a substitute: ")) - 1
        return products[index][0]

    def main_loop(self):
        mode = None
        while mode not in ["1", "2", "3"]:
            mode = self.get_mode()
        if mode == "1":
            category = self.get_category()
            product_name = self.get_product(category)
            print(self.get_substitutions(product_name, category))
        elif mode == "2":
            print(self.display_substitutions())
        elif mode == "3":
            quit("See you next time")
        self.main_loop()


# input_categories = SELECT category FROM categories WHERE product_id in (SELECT id FROM products WHERE name = name)
# input_substitutions = SELECT name FROM products WHERE id IN (SELECT product_id FROM categories WHERE category IN input_categories)