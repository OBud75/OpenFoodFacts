# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du modèle d'un substitut enregistré
Les informations de chaque instances de cette classe
seront injectées dans la table "product_has_substitutes"
"""

class ProductHasSubstitutesModel:
    """Modèle d'un substitut enregristré
    """
    def __init__(self, product, *substitutes):
        """Initialisation des instances

        Args:
            product (product): Produit auquel on à trouvé des substituts
            substitutes (products): Substituts du produit
        """
        self.product = product
        self.substitutes = [substitute for substitute in substitutes]
