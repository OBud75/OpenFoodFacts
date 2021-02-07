# coding: utf-8
#! /usr/bin/env python3

"""Implémentation de la relation entre les catégories
Les informations de chaque instances de cette classe
seront injectées dans la table "category_has_categories"
"""

class CategoryHasCategoriesModel:
    def __init__(self, category, *categories):
        """Initialisation des instances avec leurs attributs
        L'attribut category est la catégorie d'un produit
        L'attribut childs est une liste contenant
        les categories qui suivent la catégories mise en premier attribut
        dans la liste des catégories du produit lié à celle ci

        Args:
            category (Category): Instance de Category
            categories (List): Instances de Category
        """
        self.category = category
        self.childs = [category for category in categories]
