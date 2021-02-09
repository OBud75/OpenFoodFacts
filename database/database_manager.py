# coding: utf-8
#! /usr/bin/env python3

"""Main database manager implementation
We use the mysql.connector module for SQL queries
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
    """Object representing the database manager
    We implement the necessary queries to:
    The creation of tables
    Relationships between them
    Connection to the database
    """
    def __init__(self, mode):
        """Initializing the instance of the database manager

        Args:
            mode (Str): Database creation or normal use
        """
        # Creation and/or connexion to the DataBase
        self.mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)

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

            print("Création de la base de données en cours...")
            self.fill_tables()
            self.mydb.commit()

    def create_data_base(self, name=constants.DATABASE_NAME):
        """Creation of the sql database if it does not already exist
        We set the encoding to utf-8 to ensure compatibility

        Args:
            name (Str): Name of the data base
        """
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute(f"""
        CREATE DATABASE IF NOT EXISTS {name}
        CHARACTER SET 'utf8';
        """)
        cursor.close()

    def use_database(self, name=constants.DATABASE_NAME):
        """Connection to the database

        Args:
            name (Str): Name of the data base
        """
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute(f"""
        USE {name};
        """)
        cursor.close()

    def create_tables(self):
        """Create all the tables necessary for the program
        """

        # Products
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
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
        cursor.close()

        # Categories
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name LONGTEXT NOT NULL
            )
        ENGINE=INNODB;
        """)

        # Stores
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            store_name LONGTEXT
            )
        ENGINE=INNODB;
        """)
        cursor.close()

        # Product has categories
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_categories (
            product_id INT UNSIGNED,
            category_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)
        cursor.close()

        # Category has categories
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_has_categories (
            category_id INT UNSIGNED,
            child_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)
        cursor.close()

        # Product has stores
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_stores (
            product_id INT UNSIGNED,
            store_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)
        cursor.close()

        # Product has substitutes
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_substitutes (
            product_id INT UNSIGNED,
            substitute_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)
        cursor.close()

    def create_relations(self):
        """Creates relationships between tables
        """

        # Product_has_categories
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        ALTER TABLE product_has_categories
            ADD CONSTRAINT fk_product_has_categories_category_id
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id),

            ADD CONSTRAINT fk_product_has_categories_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id),
        ENGINE=INNODB;
        """)
        cursor.close()

        # Category_has_categories
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        ALTER TABLE category_has_categories
            ADD CONSTRAINT fk_category_has_categories_category_id
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id),

            ADD CONSTRAINT fk_category_has_categories_child_id
            FOREIGN KEY (child_id)
            REFERENCES categories(category_id),
        ENGINE=INNODB;
        """)
        cursor.close()

        # Product_has_store
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        ALTER TABLE product_has_stores
            ADD CONSTRAINT fk_product_has_stores_store_id
            FOREIGN KEY (store_id)
            REFERENCES stores(store_id),

            ADD CONSTRAINT fk_product_has_stores_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id),
        ENGINE=INNODB;
        """)
        cursor.close()

        # Product_has_substitutes
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""
        ALTER TABLE product_has_substitutes
            ADD CONSTRAINT fk_product_has_substitute_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id),

            ADD CONSTRAINT fk_product_has_substitute_substitute_id
            FOREIGN KEY (substitute_id)
            REFERENCES products(product_id),
        ENGINE=INNODB;
        """)
        cursor.close()

    def fill_tables(self):
        """Injections des informations dans les différentes tables de données
        """
        # Products
        for product_infos in self.api_manager.get_products_list():
            product = self.products_manager.manage(**product_infos)

        # Categories
            categories = list()
            for category_has_categories in product.product_has_categories.categories_have_categories:
                categories.append(category_has_categories.category)
                for child in category_has_categories.childs:
                    if child:
                        categories.append(child)
            self.categories_manager.manage(*categories)

        # Product has categories
            self.product_has_categories_manager.manage(product.product_has_categories)

        # Category has categories
            self.category_has_categories_manager.manage(
                *product.product_has_categories.categories_have_categories)

        # Stores and product has stores
            if product.product_has_stores is not None:
                self.stores_manager.manage(*product.product_has_stores.stores)
                self.product_has_stores_manager.manage(product.product_has_stores)
