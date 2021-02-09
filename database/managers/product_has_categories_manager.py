# coding: utf-8
#! /usr/bin/env python3

"""Implementation of the manager of the "product_has_categories" table
"""

# Local application imports
from database.models.product_has_categories_model import ProductHasCategoriesModel

class ProductHasCategoriesManager:
    """Manager of the" product_has_categories "table
    This table contains information on the relationships
    between products and categories
    """
    def __init__(self, database_manager):
        """Initialization of the manager instance
        of the "product_has_categories" table

        Args:
            database_manager (DatabaseManager): Instance of the database manager
        """
        self.database_manager = database_manager

    def manage(self, product_has_categories):
        """Method called from the database manager
        Checks of the "product_has_categories" table for injections

        Args:
            product_has_categories (ProductHasCategoriesModel): Object instance
        """
        product = product_has_categories.product
        product.product_id = self.database_manager.products_manager.get_product_id(product)

        for category_has_categories in product_has_categories.categories_have_categories:
            category = category_has_categories.category
            category_id = self.database_manager.categories_manager.get_id(category)
            category.category_id = category_id
            if not self.is_in_table(product, category):
                self.add_to_table(product, category)

    def is_in_table(self, product, category):
        """Search the "product_has_categories" table to find out if
        the relationship between product and category is already registered

        Args:
            product (ProductModel): ProductModel instance
            category (CategoryModel): CategoryModel instance

        Returns:
            Bool: Is the relationship already registered?
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT *
            FROM product_has_categories
            WHERE product_id = %s
            AND category_id = %s
        """)
        data = (product.product_id, category.category_id)
        cursor.execute(query, data)
        is_saved = cursor.fetchall()
        cursor.close()
        if is_saved:
            return True
        return False

    def add_to_table(self, product, category):
        """Injection of information on relations
        between products and categories
        in the "product_has_categories" table

        Args:
            product (ProductModel): ProductModel instance
            category (CategoryModel): CategoryModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        statement = (
            "INSERT INTO product_has_categories"
            "(product_id, category_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, category.category_id)
        cursor.execute(statement, data)
        cursor.close()

    def get_products_in_category(self, category):
        """Retrieval of products related to a given category

        Args:
            category (CategoryModel): Instance of the category whose products are wanted

        Returns:
            List: ProductModel instances of the products in the category
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT *
            FROM products AS p
            JOIN product_has_categories AS phc
            ON p.product_id = phc.product_id
            WHERE category_id = %s
        """)
        data = (category.category_id,)
        cursor.execute(query, data)
        products_infos = cursor.fetchall()
        cursor.close()
        return self.database_manager.products_manager.create_products(*products_infos)

    def create(self, product):
        """Creation of the relationship between a product and a category

        Args:
            product (ProductModel): ProductModel instance

        Returns:
            ProductHasCategoriesModel: ProductHasCategoriesModel instance
        """
        cursor = self.database_manager.mydb.cursor(buffered=True)
        query = ("""
            SELECT c.category_id, category_name
            FROM categories AS c
            JOIN product_has_categories AS phc
            ON c.category_id = phc.category_id
            JOIN products AS p
            ON phc.product_id = p.product_id
            WHERE product_name = %s
        """)
        data = (product.product_name,)
        cursor.execute(query, data)
        categories_infos = cursor.fetchall()
        cursor.close()
        categories = self.database_manager.categories_manager.create_categories(*categories_infos)

        # Creating CategoryModel and CategoryHasCategoriesModel instances
        categories_have_categories = list()
        for category in categories:
            cat_has_cats = self.database_manager.category_has_categories_manager.create(category)
            categories_have_categories.append(cat_has_cats)
        return ProductHasCategoriesModel(product, *categories_have_categories)
