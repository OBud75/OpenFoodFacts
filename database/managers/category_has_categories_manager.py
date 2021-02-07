# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "category_has_categories"
"""

# Local application imports
from database.models.category_has_categories_model import CategoryHasCategoriesModel

class CategoryHasCategoriesManager():
    """Gestionnaire de la table "category_has_categories"
    Cette table contient les informations des relations entre les catégories
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "category_has_categories"

        Args:
            database_manager (DatabaseManager): Instance du gestionnaire de la database
        """
        self.database_manager = database_manager

    def manage(self, *categories_have_categories):
        """Méthode appelée depuis le gestionnaire de la database
        Vérifications de la table "category_has_categories" pour injections

        Args:
            categories_have_categories (List): Instances de CategoryHasCategoriesModel
        """
        # Catégorie liée au produit
        for category_has_categories in categories_have_categories:
            category = category_has_categories.category
            category.category_id = self.database_manager.categories_manager.get_id(category)

            # Catégories liées à la catégorie du produit
            for child in category_has_categories.childs:
                if child:
                    child.category_id = self.database_manager.categories_manager.get_id(child)
                    if not self.is_in_table(category, child):
                        self.add_to_table(category, child)

    def add_to_table(self, category, child):
        """Injection d'informations dans la table "category_has_categories"

        Args:
            category (CategoryModel): Instance de CategoryModel liée au produit
            child (CategoryModel): Instance de catégorie liée à la catégorie
        """
        statement = (
            "INSERT INTO category_has_categories"
            "(category_id, child_id)"
            "VALUES (%s, %s)"
        )
        data = (category.category_id, child.category_id)
        self.database_manager.cursor.execute(statement, data)

    def is_in_table(self, category, child):
        """Recherche dans la table "category_has_categories" pour savoir
        si la relation entre les catégories est déjà enregistrée

        Args:
            category (CategoryModel): Instance de la catégorie liée au produit
            child (CategoryModel): Instance de la catégorie liée à la catégorie

        Returns:
            Bool: La relation est elle déjà enregistrée?
        """
        query = ("""
            SELECT *
            FROM category_has_categories
            WHERE category_id = %s
            AND child_id = %s
        """)
        data = (category.category_id, child.category_id)
        self.database_manager.cursor.execute(query, data)
        if self.database_manager.cursor.fetchall():
            return True
        return False

    def create(self, category):
        """Création d'instance de CategoryHasCategories
        Représentant les catégories liées à une catégorie donnée

        Args:
            category (CategoryModel): Catégorie dont on veut les catégories liées

        Returns:
            CategoryHasCategoryModel: Lien entre une catégorie et celles liées à elle
        """
        query = ("""
            SELECT chc.child_id, category_name
            FROM categories AS c
            JOIN category_has_categories as chc
            ON chc.child_id = c.category_id
            WHERE chc.category_id = %s;
        """)
        data = (category.category_id,)
        self.database_manager.cursor.execute(query, data)
        categories_infos = self.database_manager.cursor.fetchall()

        # Création des instances de CategoryModel
        categories = self.database_manager.categories_manager.create_categories(*categories_infos)
        return CategoryHasCategoriesModel(category, *categories)
