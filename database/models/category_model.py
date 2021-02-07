# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du modèle d'une catégorie
Les informations de chaque instances de cette classe
seront injectées dans la table "categories"
"""

class CategoryModel:
    def __init__(self, category_name, category_id=None):
        """Initialisation des instances avec leurs attributs

        Args:
            category_name (Str): Nom de la catégorie
            category_id (Int, optional): ID dans la database. Defaults to None.
        """
        if category_id:
            self.category_id = category_id
        self.category_name = category_name
