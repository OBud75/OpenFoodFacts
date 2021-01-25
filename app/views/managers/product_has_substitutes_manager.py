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

    def create_product_has_substitutes(self, product):
        # SELECT *
        # FROM products
        #
        #
        # WHERE count(categories en commun entre le produit et la recherche) > 2
                            #select category_id            select category_id
        #
        # nutrition_grades < %s
        query = ("""
            SELECT *
            FROM products where nutrition_grades = %s
        """)
        data = (product.nutrition_grades,)
        self.database_manager.cursor.execute(query, data)
        substitutes_infos = self.database_manager.cursor.fetchall()
        substitutes = self.database_manager.products_manager.create_products(*substitutes_infos)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_substitutes_of_product(self, product):
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        query = ("""
            SELECT DISTINCT(product_id), code, product_name, ingredients_text, nutrition_grades, link
            FROM products
            WHERE product_id IN (SELECT substitute_id
                                 FROM product_has_substitutes
                                 WHERE product_id = %s)
        """)
        data = (product.product_id,)
        self.database_manager.cursor.execute(query, data)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)

    def get_saved_products_in_category(self, category):
        query = ("""
            SELECT DISTINCT(p.product_id), code, product_name, ingredients_text, nutrition_grades, link
            FROM product_has_substitutes AS phs
            JOIN product_has_categories AS phc
            ON phs.product_id = phc.product_id
            JOIN products AS p
            ON phs.product_id = p.product_id
            WHERE category_id = %s
        """)
        data = (category.category_id,)
        self.database_manager.cursor.execute(query, data)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)
