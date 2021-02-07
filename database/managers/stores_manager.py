# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire de la table "stores"
"""

class StoresManager:
    """Gestionnaire de la table "stores"
    Cette table contient les informations relatives aux magasins
    """
    def __init__(self, database_manager):
        """Initialisation de l'instance du gestionnaire de la table "stores"

        Args:
            database_manager (DatabaseManager): Gestionnaire de la database
        """
        self.database_manager = database_manager

    def manage(self, *stores):
        """Méthode appelée depuis le gestionnaire de la database
        Nous ajoutons les magasins à la base de données s'il n'y sont pas déja
        """
        for store in stores:
            if store.store_name and self.get_store_id(store) is None:
                self.add_to_table(store)

    def get_store_id(self, store):
        """Récupération de L'ID d'un magasin grâce à son nom

        Args:
            store (StoreModel): Instance de StoreModel
        """
        query = ("""
            SELECT store_id
            FROM stores
            WHERE store_name LIKE %s
        """)
        data = (store.store_name,)
        self.database_manager.cursor.execute(query, data)
        result = self.database_manager.cursor.fetchone()
        if result is not None:
            return result[0]
        return None

    def add_to_table(self, store):
        """Injection d'un magasin dans la table "stores"

        Args:
            store (Store): Instance de StoreModel
        """
        statement = (
            "INSERT INTO stores"
            "(store_name)"
            "VALUES (%s)"
        )
        data = (store.store_name,)
        self.database_manager.cursor.execute(statement, data)
