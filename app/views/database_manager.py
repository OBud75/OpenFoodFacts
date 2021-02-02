# coding: utf-8
#! /usr/bin/env python3

"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Third party import
import mysql.connector

# Local application imports
from app import constants
from app.views.api_manager import ApiManager
from app.views.managers.products_manager import ProductsManager
from app.views.managers.categories_manager import CategoriesManager
from app.views.managers.stores_manager import StoresManager
from app.views.managers.product_has_categories_manager import ProductHasCategoriesManager
from app.views.managers.category_has_categories_manager import CategoryHasCategoriesManager
from app.views.managers.product_has_stores_manager import ProductHasStoresManager
from app.views.managers.product_has_substitutes_manager import ProductHasSubstitutesManager

class DataBaseManager:
    """In this class we implement the SQL DataBase structure
    """
    def __init__(self, mode):
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
        self.cursor.execute(f"""
        CREATE DATABASE IF NOT EXISTS {name}
        CHARACTER SET 'utf8';
        """)

    def use_database(self, name=constants.DATABASE_NAME):
        self.cursor.execute(f"""
        USE {name};
        """)

    def create_tables(self):
        """Create all the tables needed in the database
        products, categories, stores
        product_has_categories, category_has_categories,
        product_has_stores, product_has_substitutes
        """

        # Create products table
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

        # Create categories table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name LONGTEXT NOT NULL
            )
        ENGINE=INNODB;
        """)

        # Create stores table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            store_name LONGTEXT
            )
        ENGINE=INNODB;
        """)

        # Create table product_has_categories
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_categories (
            product_id INT UNSIGNED,
            category_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Create table category_has_categories
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_has_categories (
            category_id INT UNSIGNED,
            child_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Create table product_has_stores
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_stores (
            product_id INT UNSIGNED,
            store_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Create table product_has_substitutes
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_has_substitutes (
            product_id INT UNSIGNED,
            substitute_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        """Create the relations between tables
        """

        # For table product_has_categories
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

        # For table category_has_categories
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

        # For table product_has_store
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

        # For table product_has_substitutes
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
        for product_infos in self.api_manager.get_products_list():
            product = self.products_manager.manage(**product_infos)

            categories = list()
            for category_has_categories in product.product_has_categories.categories_have_categories:
                categories.append(category_has_categories.category)
                for child in category_has_categories.childs:
                    if child:
                        categories.append(child)
            self.categories_manager.manage(*categories)

            self.product_has_categories_manager.manage(product.product_has_categories)
            self.category_has_categories_manager.manage(*product.product_has_categories.categories_have_categories)
            if product.product_has_stores != None:
                self.stores_manager.manage(*product.product_has_stores.stores)
                self.product_has_stores_manager.manage(product.product_has_stores)
