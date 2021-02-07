# coding: utf-8
#! /usr/bin/env python3

"""Implémentation de la relation entre produits et catégories
Les informations de chaque instances de cette classe
seront injectées dans la table "product_has_catégories"
"""

class ProductHasCategoriesModel:
    def __init__(self, product, *categories_have_categories):
        """Initialisation des instances avec leurs attributs

        Args:
            product (Product): Instance de Product auquel on associe les catégories
            categories_have_categories (List): Instances de CategoryHasCategories associées
        """
        self.product = product
        self.categories_have_categories = [category_has_categories
                                           for category_has_categories
                                           in categories_have_categories]
