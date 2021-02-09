# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager of the "product_has_substitutes" table
"""

from database.models.product_has_substitutes_model import ProductHasSubstitutesModel

class ProductHasSubstitutesManager:
    """Manager of the "product_has_substitutes" table
    This table contains the information of the products
    for which a substitute has been registered
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance
        of the "product_has_substitutes" table

        Args:
            database_manager (DatabaseManager): Instance of the database manager
        """
        self.database_manager = database_manager

    def save_substitute(self, product, substitute):
        """Injection into the product_has_substitute table
        of a product and substitute selected by the user

        Args:
            product (Product): ProductModel instance of the product
            substitute (Product): Substitute's ProductModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        substitute.product_id = self.database_manager.products_manager.get_product_id(substitute)
        statement = (
            "INSERT INTO product_has_substitutes"
            "(product_id, substitute_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, substitute.product_id)
        cursor.execute(statement, data)
        self.database_manager.mydb.commit()
        cursor.close()

    def is_already_saved(self, product, substitute):
        """Search in the "product_has_substitutes" table
        to know if the substitution is already registered

        Args:
            product (ProductModel): ProductModel instance of the product
            substitute (ProductModel): Substitute's ProductModel instance

        Returns:
            Bool: Is the substitution already registered?
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT *
            FROM product_has_substitutes
            WHERE product_id = %s
            AND substitute_id = %s
        """)
        data = (product.product_id, substitute.product_id)
        cursor.execute(query, data)
        is_saved = cursor.fetchall()
        cursor.close()
        if is_saved:
            return True
        return False

    def delete_substitute(self, product, substitute):
        """Delete a saved substitution

        Args:
            product (Product): ProductModel instance of the product
            substitute (Product): Substitute's ProductModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = ("""
            DELETE FROM product_has_substitutes
            WHERE product_id = %s
            AND substitute_id = %s
        """)
        data = (product.product_id, substitute.product_id)
        cursor.execute(statement, data)
        self.database_manager.mydb.commit()
        cursor.close()

    def get_substitutes_of_product(self, product):
        """Retrieves possible substitutes for a product
        Creates an instance of ProductHasSubstitutesModel
        The arguments are:
        The instance of ProductModel for which we want the substitutes
        A list of ProductModel instancecs of possible substitutes

        Args:
            product (ProductModel): Product for which we want possible substitutes

        Returns:
            ProductHasSubstitutes: ProductHasSubstitutesModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT *
            FROM products as p
            JOIN product_has_categories AS phc
            ON p.product_id = phc.product_id
            WHERE nutrition_grades < %s
            AND phc.category_id IN (SELECT child_id
                                    FROM category_has_categories AS chc
                                    JOIN product_has_categories AS phc
                                    ON chc.category_id = phc.category_id
                                    WHERE product_id = %s)
        """)
        data = (product.nutrition_grades, product.product_id)
        cursor.execute(query, data)
        substitutes_infos = cursor.fetchall()
        cursor.close()
        substitutes = self.database_manager.products_manager.create_products(*substitutes_infos)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_substitutes_of_product(self, product):
        """Retrieves already registered substitutes for a product
        Creates an instance of ProductHasSubstitutesModel
        The arguments are:
        The ProductModel instance for which we want registered substitutes
        A list of ProductModel instancecs of already registered surrogates

        Args:
            product (ProductModel): Product for which we want substitutes already registered

        Returns:
            ProductHasSubstitutesModel: Representation of a product with its substitutes
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        product.product_id = self.database_manager.products_manager.get_product_id(product)
        query = ("""
            SELECT p.product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM product_has_substitutes AS phs
            JOIN products AS p
            ON p.product_id = phs.substitute_id
            WHERE phs.product_id = %s
        """)
        data = (product.product_id,)
        cursor.execute(query, data)
        substitutes_infos = cursor.fetchall()
        cursor.close()

        # Creation of ProductModel instances of substitutes
        substitutes = list()
        for substitute_infos in substitutes_infos:
            substitute = self.database_manager.products_manager.create_product(substitute_infos)
            substitutes.append(substitute)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_products(self):
        """Retrieves products that have a registered substitute

        Returns:
            List: ProductModel instances of products that have a registered surrogate
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        cursor.execute("""
            SELECT phs.product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM products AS p
            JOIN product_has_substitutes AS phs
            ON phs.product_id = p.product_id
        """)
        products_infos = cursor.fetchall()
        cursor.close()
        return self.database_manager.products_manager.create_products(*products_infos)
