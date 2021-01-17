# coding: utf-8
#! /usr/bin/env python3

"""
"""

from data.views.models.product_has_substitute_model import ProductHasSubstituteModel

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

    def get_substitutes_of_product(self, product):
        # select product_name
        # where nutrition_grades < %s
        # and 5 plus hautes categories in requestes categories
        query = ("""
            SELECT DISTINCT(p.product_id), code, product_name, ingredients_text, nutrition_grades, link
            FROM product_has_categories AS phc
            INNER JOIN (SELECT DISTINCT(categories.category_id)
                        FROM categories
                        JOIN product_has_categories) AS c
            ON phc.category_id = c.category_id
            INNER JOIN products AS p
            ON phc.product_id = p.product_id
            WHERE nutrition_grades < %s
        """)
        data = (product.product_id,)
        self.database_manager.cursor.execute(query, data)
        substitutes_infos = self.database_manager.cursor.fetchall()
        substitutes = self.database_manager.products_manager.create_products(*substitutes_infos)
        return ProductHasSubstituteModel(product, *substitutes)

    def get_products_with_substitutes(self):
        self.database_manager.cursor.execute("""
            SELECT DISTINCT(p.product_id), code, product_name, ingredients_text, nutrition_grades, link
            FROM product_has_substitutes AS phs
            JOIN products AS p
            ON phs.product_id = p.product_id
        """)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)

    def get_saved_substitutes_of_product(self, product):
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        query = ("""
            SELECT *
            FROM products
            WHERE product_id IN (SELECT substitute_id
                                 FROM product_has_substitutes
                                 WHERE product_id = %s)
        """)
        data = (product.product_id,)
        self.database_manager.cursor.execute(query, data)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)
