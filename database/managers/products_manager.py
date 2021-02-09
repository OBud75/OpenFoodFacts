# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the "products" table manager
"""

# Local application imports
from database import constants
from database.models.product_model import ProductModel

class ProductsManager:
    """Manager of the "products" table
    This table contains information about the products
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance of the "products" table

        Args:
            database_manager (DatabaseManager): Database manager
        """
        self.database_manager = database_manager

    def manage(self, **product_infos):
        """Method called from the database manager
        We add the products to the database if they are not already there

        Args:
            product_infos (Dict): Product information in the API
        """
        product = ProductModel(**product_infos)
        if self.get_product_id(product) is None:
            self.add_to_table(product)
        return product

    def get_product_id(self, product):
        """Retrieving the ID of a product from its name

        Returns:
            Int: Product ID in the database
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT product_id
            FROM products
            WHERE product_name = %s
        """)
        data = (product.product_name,)
        cursor.execute(query, data)
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            return result[0]
        return None

    def add_to_table(self, product):
        """Injecting a product into the "products" table

        Args:
            product (Product): ProductModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = (
            "INSERT IGNORE INTO products"
            "(code, product_name, ingredients_text, nutrition_grades, link)"
            "VALUES (%s, %s, %s, %s, %s)"
        )
        data = (
            product.code,
            product.product_name,
            product.ingredients_text,
            product.nutrition_grades,
            product.link
        )
        cursor.execute(statement, data)
        cursor.close()

    def create_product_by_name(self, product_name):
        """Creates an instance of the ProductModel object
        Product of which we only know the name

        Args:
            product_name (Str): Product name
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM products
            WHERE product_name = %s
        """)
        data = (product_name,)
        cursor.execute(query, data)
        product_infos_list = cursor.fetchall()
        cursor.close()
        if product_infos_list:
            return self.create_product(product_infos_list[0])
        return None

    def create_products(self, *products_infos_list):
        """Creates instances of the ProductModel object
        Products for which we have all the information

        Args:
            products_infos_list (Liste de dictionnaires): Products informations
        """
        products = list()
        for product_infos_list in products_infos_list:
            product = self.create_product(product_infos_list)
            products.append(product)
        return products

    def create_product(self, product_infos_list):
        """Creates an instance of the ProductModel object
        Product for which we have all the information

        Args:
            product_infos_list (Dict): Product informations
        """
        product_infos = {key: product_infos_list[index]
                         for index, key in enumerate(constants.ALL_PRODUCTS_TABLE_COLUMNS)}
        product = ProductModel(**product_infos)

        product_has_categories = self.database_manager.product_has_categories_manager.create(product)
        product.product_has_categories = product_has_categories

        product_has_stores = self.database_manager.product_has_stores_manager.create(product)
        product.product_has_stores = product_has_stores
        return product
