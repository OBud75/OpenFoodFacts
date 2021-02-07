# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "products"
"""

# Local application imports
from database import constants
from database.models.product_model import ProductModel

class ProductsManager:
    """Gestionnaire de la table "products"
    Cette table contient les informations relatives aux produits
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "products"

        Args:
            database_manager (DatabaseManager): Gestionnaire de la database
        """
        self.database_manager = database_manager

    def manage(self, **product_infos):
        """Méthode appelée depuis le gestionnaire de la database
        Nous ajoutons les produits à la base de données s'il n'y sont pas déja
        """
        product = ProductModel(**product_infos)
        if self.get_product_id(product) is None:
            self.add_to_table(product)
        return product

    def get_product_id(self, product):
        """Récupération de L'ID d'un produit grâce à son nom
        """
        query = ("""
            SELECT product_id
            FROM products
            WHERE product_name = %s
        """)
        data = (product.product_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result is not None:
            return result[0]
        return None

    def add_to_table(self, product):
        """Injection d'un produit dans la table "products"

        Args:
            product (Product): Instance de ProductModel
        """
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

    def create_product_by_name(self, product_name):
        """Créé une instance de l'objet ProductModel
        Produit dont on ne connait que le nom

        Args:
            product_name (Str): Nom du produit
        """
        query = ("""
            SELECT product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM products
            WHERE product_name = %s
        """)
        data = (product_name,)
        self.database_manager.cursor.execute(query, data)
        product_infos_list = self.database_manager.cursor.fetchall()
        if product_infos_list:
            return self.create_product(product_infos_list[0])
        return None

    def create_products(self, *products_infos_list):
        """Créé des instances de l'objet ProductModel
        Produits dont on à toutes les informations

        Args:
            products_infos_list (Liste de dictionnaires): Informations des produits
        """
        products = list()
        for product_infos_list in products_infos_list:
            product = self.create_product(product_infos_list)
            products.append(product)
        return products

    def create_product(self, product_infos_list):
        """Créé une instance de l'objet ProductModel
        Produit dont on à toutes les informations

        Args:
            product_infos_list (Dict): Informations des produits
        """
        product_infos = {key: product_infos_list[index]
                         for index, key in enumerate(constants.ALL_PRODUCTS_TABLE_COLUMNS)}
        product = ProductModel(**product_infos)

        product_has_categories = self.database_manager.product_has_categories_manager.create(product)
        product.product_has_categories = product_has_categories

        product_has_stores = self.database_manager.product_has_stores_manager.create(product)
        product.product_has_stores = product_has_stores
        return product
