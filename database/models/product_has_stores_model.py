# coding: utf-8
#! /usr/bin/env python3

"""Implémentation de la relation entre produits et magasins
Les informations de chaque instances de cette classe
seront injectées dans la table "product_has_stores"
"""

# Local application imports
from database.models.store_model import StoreModel

class ProductHasStoresModel:
    """Initialisation des instances
    L'attribut product est une instance d'objet ProductModel
    Nous créons des instances de StoreModel pour l'attribut stores

    Args:
        product (Product): Produit auquel on à trouvé des substituts
        stores_names (Str): Nom des magasins associés
    """
    def __init__(self, product, *stores_names):
        self.product = product
        self.stores = [StoreModel(store_name) for store_name in stores_names]
