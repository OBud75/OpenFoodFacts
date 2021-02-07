# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du gestionnaire principal de la base de données
Nous utilisons le module mysql.connector pour les requètes SQL
"""

# Third party import
import mysql.connector

# Local application imports
from database import constants
from database.api_manager import ApiManager
from database.managers.products_manager import ProductsManager
from database.managers.categories_manager import CategoriesManager
from database.managers.stores_manager import StoresManager
from database.managers.product_has_categories_manager import ProductHasCategoriesManager
from database.managers.category_has_categories_manager import CategoryHasCategoriesManager
from database.managers.product_has_stores_manager import ProductHasStoresManager
from database.managers.product_has_substitutes_manager import ProductHasSubstitutesManager

class DataBaseManager:
    """Objet représentant le gestionnaire de la base de données
    Nous implémentons les requètes nécessaires à:
    La création des tables
    Les relations entre elles
    La connection à la base de données
    """
    def __init__(self, mode):
        """Initialisation de l'instance du gestionnaire de base ded données

        Args:
            mode (Str): Création de la database ou utilisation normale
        """
        # Creation and/or connexion to the DataBase
        self.mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)
        self.cursor = self.mydb.cursor(buffered=True)

        if mode == "create":
            self.create_data_base()
        self.use_database()

        self.products_manager = ProductsManager(self)
        self.categories_manager = CategoriesManager(self)
        self.stores_manager = StoresManager(self)
        self.product_has_categories_manager = ProductHasCategoriesManager(self)
        self.category_has_categories_manager = CategoryHasCategoriesManager(self)
        self.product_has_stores_manager = ProductHasStoresManager(self)
        self.product_has_substitutes_manager = ProductHasSubstitutesManager(self)

        # Create and fills tables using API
        if mode == "create":
            self.create_tables()
            self.create_relations()
            self.api_manager = ApiManager()
            self.fill_tables()
            self.mydb.commit()

    def create_data_base(self, name=constants.DATABASE_NAME):
        """Création de la base de données sql si elle n'existe pas déja
        Nous définissons l'encodage en utf-8 pour assurer la compatibilité

        Args:
            name (Str): Nom de la base de données
        """
        self.cursor.execute(f"""
        CREATE DATABASE IF NOT EXISTS {name}
        CHARACTER SET 'utf8';
        """)

    def use_database(self, name=constants.DATABASE_NAME):
        """Connection à la base de données

        Args:
            name (Str): Nom de la base de données
        """
        self.cursor.execute(f"""
        USE {name};
        """)

    def create_tables(self):
        """Créé toutes les tables nécéssaires au programme
        products, categories, stores
        product_has_categories, category_has_categories,
        product_has_stores, product_has_substitutes
        """

        # Table contenant les produits
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            code BIGINT UNSIGNED UNIQUE NOT NULL,
            product_name LONGTEXT NOT NULL,
            ingredients_text LONGTEXT,
            nutrition_grades VARCHAR(1) NOT NULL,
            link LONGTEXT NOT NULL
            )
        ENGINE=INNODB;
        """)

        # # Table contenant les catégories
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name LONGTEXT NOT NULL
            )
        ENGINE=INNODB;
        """)

        # # Table contenant les magasins
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            store_name LONGTEXT
            )
        ENGINE=INNODB;
        """)

        # Table contenant la liaison entre produits et catégories
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_categories (
            product_id INT UNSIGNED,
            category_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Table contenant la liaison entre les catégories
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_has_categories (
            category_id INT UNSIGNED,
            child_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Table contenant la liaison entre les produits et les magasins
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_stores (
            product_id INT UNSIGNED,
            store_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Table contenant les substituts enregistrés
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_substitutes (
            product_id INT UNSIGNED,
            substitute_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        """Crée les relations entre les tables
        """

        # Table product_has_categories
        self.cursor.execute("""
        ALTER TABLE product_has_categories
            ADD CONSTRAINT fk_product_has_categories_category_id
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id),

            ADD CONSTRAINT fk_product_has_categories_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id),
        ENGINE=INNODB;
        """)

        # Table category_has_categories
        self.cursor.execute("""
        ALTER TABLE category_has_categories
            ADD CONSTRAINT fk_category_has_categories_category_id
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id),

            ADD CONSTRAINT fk_category_has_categories_child_id
            FOREIGN KEY (child_id)
            REFERENCES categories(category_id),
        ENGINE=INNODB;
        """)

        # Table product_has_store
        self.cursor.execute("""
        ALTER TABLE product_has_stores
            ADD CONSTRAINT fk_product_has_stores_store_id
            FOREIGN KEY (store_id)
            REFERENCES stores(store_id),

            ADD CONSTRAINT fk_product_has_stores_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id),
        ENGINE=INNODB;
        """)

        # Table product_has_substitutes
        self.cursor.execute("""
        ALTER TABLE product_has_substitutes
            ADD CONSTRAINT fk_product_has_substitute_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id),

            ADD CONSTRAINT fk_product_has_substitute_substitute_id
            FOREIGN KEY (substitute_id)
            REFERENCES products(product_id),
        ENGINE=INNODB;
        """)

    def fill_tables(self):
        """Injections des informations dans les différentes tables de données
        """
        # Produits
        for product_infos in self.api_manager.get_products_list():
            product = self.products_manager.manage(**product_infos)

        # Catégories
            categories = list()
            for category_has_categories in product.product_has_categories.categories_have_categories:
                categories.append(category_has_categories.category)
                for child in category_has_categories.childs:
                    if child:
                        categories.append(child)
            self.categories_manager.manage(*categories)

        # Relations entre produits et catégories
            self.product_has_categories_manager.manage(product.product_has_categories)

        # Relations entre les catégories
            self.category_has_categories_manager.manage(
                *product.product_has_categories.categories_have_categories)

        # Magasins et relations entre les produits et les magasins
            if product.product_has_stores is not None:
                self.stores_manager.manage(*product.product_has_stores.stores)
                self.product_has_stores_manager.manage(product.product_has_stores)
