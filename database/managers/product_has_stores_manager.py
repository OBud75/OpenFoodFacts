# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "product_has_stores"
"""

from database.models.product_has_stores_model import ProductHasStoresModel

class ProductHasStoresManager:
    """Gestionnaire de la table "product_has_stores"
    Cette table contient les informations des relations entre produits et magasins
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "product_has_stores"

        Args:
            database_manager (DatabaseManager): Instance du gestionnaire de la database
        """
        self.database_manager = database_manager

    def manage(self, product_has_stores):
        """Méthode appelée depuis le gestionnaire de la database
        Vérifications de la table "product_has_stores" pour injections

        Args:
            product_has_stores (ProductHasStoresModel): Instance de ProductHasStoresModel
        """
        product = product_has_stores.product
        stores = product_has_stores.stores

        product.product_id = self.database_manager.products_manager.get_product_id(product)
        for store in stores:
            if store.store_name is not None:
                store.store_id = self.database_manager.stores_manager.get_store_id(store)
                self.add_to_table(product, store)

    def add_to_table(self, product, store):
        """Injection des informations des relations entre produits et magasins
        dans la table "product_has_stores"

        Args:
            product (ProductModel): Instance de ProductModel
            store (StoreModel): Instance de StoreModel
        """
        statement = (
            "INSERT INTO product_has_stores"
            "(product_id, store_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, store.store_id)
        self.database_manager.cursor.execute(statement, data)

    def create(self, product):
        """Créé une instance de ProductHasStoresModel
        Les arguments sont:
        L'instance de ProductModel
        Le noms des magasins liés au produit

        Args:
            product (ProductModel): Instance de ProductModel

        Returns:
            ProductHasStoresModel: Instance de ProductHasStores
        """
        query = ("""
            SELECT *
            FROM stores AS s
            JOIN product_has_stores AS phs
            ON s.store_id = phs.store_id
            WHERE product_id = %s
        """)
        data = (product.product_id,)
        self.database_manager.cursor.execute(query, data)
        stores_infos = self.database_manager.cursor.fetchall()
        if stores_infos:
            return ProductHasStoresModel(product, *stores_infos)
        return None
