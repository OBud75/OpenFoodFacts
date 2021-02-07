# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "categories"
"""

# Local application imports
from database.models.category_model import CategoryModel

class CategoriesManager:
    """Gestionnaire de la table "categories"
    Cette table contient les informations relatives aux catégories
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "categories"

        Args:
            database_manager (DatabaseManager): Instance du gestionnaire de la database
        """
        self.database_manager = database_manager

    def manage(self, *categories):
        """Méthode appelée depuis le gestionnaire de la database
        Nous ajoutons les catégories à la base de données si elles n'y sont pas déja
        """
        for category in categories:
            if not self.get_id(category):
                self.add_to_table(category)

    def get_id(self, category):
        """Récupération de L'ID d'une catégorie grâce à son nom

        Args:
            category (CategoryModel): Instance de CategoryModel
        """
        query = ("""
                SELECT category_id
                FROM categories
                WHERE category_name = %s
            """)
        if category:
            data = (category.category_name,)
            self.database_manager.cursor.execute(query, data)
            result = self.database_manager.cursor.fetchone()
            if result is not None:
                return result[0]
        return None

    def add_to_table(self, category):
        """Injection d'une catégorie dans la table "categories"

        Args:
            category (CategoryModel): Instance de CategoryModel
        """
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (category.category_name,)
        self.database_manager.cursor.execute(statement, data)

    def create_categories(self, *categories_infos):
        """Créé des instances de l'objet CtaegoryModel

        Args:
            categories_infos (List): Informations sur les categorie

        Returns:
            List: Instances de CategoryModel
        """
        categories = list()
        for category_infos in categories_infos:
            category = self.create(category_infos)
            categories.append(category)
        return categories

    def create(self, category_infos):
        """Créé une instance de l'objet CtaegoryModel
        Adaptation en fonction du nombre d'informations disponibles

        Args:
            category_infos (List): Informations sur la catégorie dans la database

        Returns:
            CategoryModel: Instance de CategoryModel
        """
        # Si l'on connait le nom et L'ID de la catégorie
        if len(category_infos) == 2:
            category = CategoryModel(category_name=category_infos[1],
                                     category_id=category_infos[0])

        # Si l'on connait uniquement le nom de la catégorie
        elif len(category_infos) == 1:
            category = CategoryModel(category_name=category_infos[0])
            category.category_id = self.get_id(category)
        else:
            category = CategoryModel(category_name=category_infos)
            category.category_id = self.get_id(category)
        return category
