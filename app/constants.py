# coding: utf-8
#! /usr/bin/env python3

"""Constants
"""

# Standard library import
import os

# MySQL configuration
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_CONFIG = {
            "user": "root",
            "password": MYSQL_PASSWORD,
            "host": "localhost",
            "auth_plugin": "mysql_native_password",
        }
DATABASE_NAME = "openfoodfacts"

STARTERS_CATEGORIES = [
            "Produits labellisés",
            "Bio",
            "Plats cuisinees",
            "100 % légumes",
            "Barquettes",
            "Cremes entieres",
            "Desserts sucrés",
            "Preparations pour desserts lactes",
            "Mélanges de fruits",
            "Multifruits",
            "Boissons salées",
            "Préparations pour boissons",
            "Boissons froides",
            "Lait à boire",
            "Spécialités laitières"
        ]

# Substitutions
SELECT_MODE_LIST = [
            "Quel aliment souhaitez-vous remplacer ?",
            "Retrouver mes aliments substitués."
        ]
