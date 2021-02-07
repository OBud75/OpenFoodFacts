# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "product_has_categories"
"""

# Local application imports
from database.models.product_has_categories_model import ProductHasCategoriesModel

class ProductHasCategoriesManager:
    """Gestionnaire de la table "product_has_categories"
    Cette table contient les informations des relations entre produits et catégories
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "product_has_categories"

        Args:
            database_manager (DatabaseManager): Instance du gestionnaire de la database
        """
        self.database_manager = database_manager

    def manage(self, product_has_categories):
        """Méthode appelée depuis le gestionnaire de la database
        Vérifications de la table "product_has_categories" pour injections

        Args:
            product_has_categories (ProductHasCategoriesModel): Instance d'objet
        """
        product = product_has_categories.product
        product.product_id = self.database_manager.products_manager.get_product_id(product)

        for category_has_categories in product_has_categories.categories_have_categories:
            category = category_has_categories.category
            category_id = self.database_manager.categories_manager.get_category_id(category)
            category.category_id = category_id
            if not self.is_in_table(product, category):
                self.add_to_table(product, category)

    def is_in_table(self, product, category):
        """Recherche dans la table "product_has_categories" pour savoir si
        la relation entre le produit et la catégorie est déjà enregistrée

        Args:
            product (ProductModel): Instance de ProductModel
            category (CategoryModel): Instance de CategoryModel

        Returns:
            Bool: La relation est elle déjà enregistrée?
        """
        query = ("""
            SELECT *
            FROM product_has_categories
            WHERE product_id = %s
            AND category_id = %s
        """)
        data = (product.product_id, category.category_id)
        self.database_manager.cursor.execute(query, data)
        if self.database_manager.cursor.fetchall():
            return True
        return False

    def add_to_table(self, product, category):
        """Injection des informations des relations entre produits et categories
        dans la table "product_has_categories"

        Args:
            product (ProductModel): Instance de ProductModel
            category (CategoryModel): Instance de CategoryModel
        """
        statement = (
            "INSERT INTO product_has_categories"
            "(product_id, category_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, category.category_id)
        self.database_manager.cursor.execute(statement, data)

    def get_products_in_category(self, category):
        """Récupération des produits en relation avec une catégorie donnée

        Args:
            category (CategoryModel): Instance de la catégorie dont on veut les produits liés

        Returns:
            List: Instances de ProductModel des produits dans la catégorie
        """
        query = ("""
            SELECT *
            FROM products AS p
            JOIN product_has_categories AS phc
            ON p.product_id = phc.product_id
            WHERE category_id = %s
        """)
        data = (category.category_id,)
        self.database_manager.cursor.execute(query, data)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)

    def create(self, product):
        """Création de la relation entre un produit et une catégorie

        Args:
            product (ProductModel): Instance de ProductModel

        Returns:
            ProductHasCategoriesModel: Instance de ProductHasCategoriesModel
        """
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
        self.database_manager.cursor.execute(query, data)
        categories_infos = self.database_manager.cursor.fetchall()
        categories = self.database_manager.categories_manager.create_categories(*categories_infos)

        # Création des instances de CategoryModel et CategoryHasCategoriesModel
        categories_have_categories = list()
        for category in categories:
            cat_has_cats = self.database_manager.category_has_categories_manager.create(category)
            categories_have_categories.append(cat_has_cats)
        return ProductHasCategoriesModel(product, *categories_have_categories)
