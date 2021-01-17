# coding: utf-8
#! /usr/bin/env python3

"""In this file we put all the informations relatives to a product
"""

# Local application imports
from data.views.models.product_model import ProductModel

class ProductsManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, **product_infos):
        product = ProductModel(**product_infos)
        if self.get_product_id(product) == None:
            self.add_to_table(product)
        return product

    def get_product_id(self, product):
        query = ("""
            SELECT product_id
            FROM products
            WHERE product_name = %s
        """)
        data = (product.product_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result != None:
            return result[0]

    def add_to_table(self, product):
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
        self.database_manager.cursor.execute(statement, data)

    def create_products(self, *products_infos_list):
        products = list()
        for product_infos_list in products_infos_list:
            product_infos = {key: product_infos_list[index] for index, key in enumerate(
                            ["product_id", "code", "product_name", "ingredients_text", "nutrition_grades", "link"])}
            product = ProductModel(**product_infos)
            product.product_has_categories = self.database_manager.product_has_categories_manager.create_product_has_categories(product)
            #product.product_has_stores = self.database_manager.product_has_stores_manager.get_product_has_stores(product)
            products.append(product)
        return products
