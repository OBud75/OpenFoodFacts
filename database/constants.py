# coding: utf-8
#! /usr/bin/env python3

"""Constants relating to the creation and connection to the SQL database
"""

# Standard library import
import os

# API OpenFoodFacts
API_INFORMATIONS = [
    "code",
    "product_name",
    "ingredients_text",
    "nutrition_grades",
    "categories_hierarchy",
    "stores_tags"
    ]

API_MANDATORY_INFORMATIONS = [
    "code",
    "product_name",
    "nutrition_grades",
    "categories_hierarchy"
    ]

# MySQL configuration
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

MYSQL_CONFIG = {
    "user": "root",
    "password": MYSQL_PASSWORD,
    "host": "localhost",
    "auth_plugin": "mysql_native_password",
    }

DATABASE_NAME = "openfoodfacts"

# MySQL Tables
ALL_PRODUCTS_TABLE_COLUMNS = [
    "product_id",
    "code",
    "product_name",
    "ingredients_text",
    "nutrition_grades",
    "link"
    ]
