# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du modèle d'un magasin
Les informations de chaque instances de cette classe
seront injectées dans la table "stores"
"""

class StoreModel:
    """Modèle d'un magasin
    """
    def __init__(self, store_name, store_id=None):
        """Les informations relatives à un magasin sont
        Le nom du magasin
        L'ID du magasin dans la base de données

        Args:
            store_name (Str): Nom du magasin
            store_id (Int, optional): ID du magasin dans la database. None par défault.
        """
        if store_id:
            self.store_id = store_id
        self.store_name = store_name
