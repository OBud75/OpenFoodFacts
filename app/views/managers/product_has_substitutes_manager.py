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

    def get_product_has_substitutes(self, product):
        query = ("""
            SELECT *
            FROM products AS p
            JOIN product_has_categories AS phc
            ON p.product_id = phc.product_id
            JOIN categories AS c
            ON c.category_id = phc.category_id
            WHERE nutrition_grades < %s
            AND p.product_id
            IN (SELECT phc.product_id
                FROM product_has_categories
                WHERE category_id
                IN (SELECT child_id
                    FROM category_has_categories
                    WHERE category_id
                    IN (SELECT category_id
                        FROM product_has_categories
                        WHERE product_id = %s)))
        """)
        data = (product.product_id, product.nutrition_grades)
        self.database_manager.cursor.execute(query, data)
        substitutes_infos = self.database_manager.cursor.fetchall()
        substitutes = self.database_manager.products_manager.create_products(*substitutes_infos)
        return ProductHasSubstitutesModel(product, *substitutes)

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

"""
SELECT c1.category_name, c2.category_name
FROM categories AS c1
JOIN category_has_categories AS chc
ON c1.category_id = chc.category_id
JOIN categories AS c2
ON chc.child_id = c2.category_id
"""