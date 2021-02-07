# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "product_has_substitutes"
"""

from database.models.product_has_substitutes_model import ProductHasSubstitutesModel

class ProductHasSubstitutesManager:
    """Gestionnaire de la table "product_has_substitutes"
    Cette table contient les informations des produits dont un substitut a été enregistré
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "product_has_substitutes"

        Args:
            database_manager (DatabaseManager): Instance du gestionnaire de la database
        """
        self.database_manager = database_manager

    def save_substitute(self, product, substitute):
        """Injection dans la table product_has_substitute
        d'un produit et du substitut séléctionné par l'utilisateur

        Args:
            product (Product): Instance de ProductModel du produit
            substitute (Product): Instance de ProductModel du substitut
        """
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
        """Recherche dans la table "product_has_substitutes"
        pour savoir si la substitution est déjà enregistrée

        Args:
            product (ProductModel): Instance de ProductModel du produit
            substitute (ProductModel): Instance de ProductModel du substitut

        Returns:
            Bool: La substitution est elle déjà enregistrée?
        """
        query = ("""
            SELECT *
            FROM product_has_substitutes
            WHERE product_id = %s
            AND substitute_id = %s
        """)
        data = (product.product_id, substitute.product_id)
        self.database_manager.cursor.execute(query, data)
        if self.database_manager.cursor.fetchall():
            return True
        return False

    def delete_substitute(self, product, substitute):
        """Suppression d'une substitution enregistrée

        Args:
            product (Product): Instance de ProductModel du produit
            substitute (Product): Instance de ProductModel du substitut
        """
        statement = ("""
            DELETE FROM product_has_substitutes
            WHERE product_id = %s
            AND substitute_id = %s
        """)
        data = (product.product_id, substitute.product_id)
        self.database_manager.cursor.execute(statement, data)
        self.database_manager.mydb.commit()

    def get_substitutes_of_product(self, product):
        """Récupère les substituts possibles d'un produits
        Crée une instance de ProductHasSubstitutesModel
        Les arguments sont:
        L'instance de ProductModel dont nous voulons les substituts
        Une liste d'instancecs de ProductModel des substitus possibles

        Args:
            product (ProductModel): Produit dont nous voulons les substitus possibles

        Returns:
            ProductHasSubstitutes: Instance de ProductHasSubstitutesModel
        """
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
        self.database_manager.cursor.execute(query, data)
        substitutes_infos = self.database_manager.cursor.fetchall()
        substitutes = self.database_manager.products_manager.create_products(*substitutes_infos)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_substitutes_of_product(self, product):
        """Récupère les substituts déjà enregistrés d'un produits
        Crée une instance de ProductHasSubstitutesModel
        Les arguments sont:
        L'instance de ProductModel dont nous voulons les substituts enregistrés
        Une liste d'instancecs de ProductModel des substitus déjà enregistrés

        Args:
            product (ProductModel): Produit dont nous voulons les substitus déjà enregistrés
        """
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

        # Création des instances de ProductModel des substituts
        substitutes = list()
        for substitute_infos in substitutes_infos:
            substitute = self.database_manager.products_manager.create_product(substitute_infos)
            substitutes.append(substitute)
        return ProductHasSubstitutesModel(product, *substitutes)

    def get_saved_products(self):
        """Récupère les produits qui ont un substitut d'enregistré

        Returns:
            List: Instances de ProductModel des produits qui ont un substitut d'enregistré
        """
        self.database_manager.cursor.execute("""
            SELECT phs.product_id, code, product_name, ingredients_text, nutrition_grades, link
            FROM products AS p
            JOIN product_has_substitutes AS phs
            ON phs.product_id = p.product_id
        """)
        products_infos = self.database_manager.cursor.fetchall()
        return self.database_manager.products_manager.create_products(*products_infos)
