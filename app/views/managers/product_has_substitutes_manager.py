# coding: utf-8
#! /usr/bin/env python3

"""
"""

from app.views.models.product_has_substitutes_model import ProductHasSubstitutesModel

class ProductHasSubstitutesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def save_substitute(self, product, substitute):
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        substitute.product_id = self.database_manager.products_manager.get_product_id(substitute)
        statement = (
            "INSERT INTO product_has_substitutes"
            "(product_id, substitute_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, substitute.product_id)
        self.database_manager.cursor.execute(statement, data)
        self.database_manager.mydb.commit()

    def is_already_saved(self, product, substitute):
        query = ("""
            SELECT *
            FROM product_has_substitutes
            WHERE product_id = %s
            AND substitute_id = %s
        """)
        data = (product.product_id, substitute.product)
        self.database_manager.cursor.execute(query, data)
        if self.database_manager.cursor.fetchall():
            return True

    def delete_substitute(self, product, substitute):
        statement = ("""
            DELETE FROM product_has_substitutes
            WHERE product_id = %s
            AND substitute_id = %s
        """)
        data = (product.product_id, substitute.product_id)
        self.database_manager.cursor.execute(statement, data)
        self.database_manager.mydb.commit()

    def get_substitutes_of_product(self, product):
        """ product en entrée --> nutrition grade, categories
            product_has_categories 
        """
        for category_h_c in product.product_has_categories.categories_have_categories:
            print(1, category_h_c.category.category_name)
            for category in category_h_c.childs:
                print(2, category.category_name)
                print(3, category.category_id)
        quit()
        query = ("""
            SELECT *
            FROM products as p
            JOIN product_has_categories AS phc
            ON p.product_id = phc.product_id
            WHERE chc.category_id = 
            WHERE nutrition_grades = %s
        """)
        data = (product.nutrition_grades,)
        self.database_manager.cursor.execute(query, data)
        substitutes_infos = self.database_manager.cursor.fetchall()
        substitutes = self.database_manager.products_manager.create_products(*substitutes_infos)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_substitutes_of_product(self, product):
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        query = ("""
            SELECT p.product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM product_has_substitutes AS phs
            JOIN products AS p
            ON p.product_id = phs.substitute_id
            WHERE phs.product_id = %s
        """)
        data = (product.product_id,)
        self.database_manager.cursor.execute(query, data)
        substitutes_infos = self.database_manager.cursor.fetchall()
        substitutes = list()
        for substitute_infos in substitutes_infos:
            substitute = self.database_manager.products_manager.create_product(substitute_infos)
            substitutes.append(substitute)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_products(self):
        self.database_manager.cursor.execute("""
            SELECT phs.product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM products AS p
            JOIN product_has_substitutes AS phs
            ON phs.product_id = p.product_id
        """)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)
