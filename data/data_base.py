"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Standard library import
from pprint import pprint
import os

# Third party import
import requests
import mysql.connector

# Local application imports
from data import constants
from data.tables.products_table import ProductsTable
from data.tables.categories_table import CategoriesTable
from data.tables.stores_table import StoresTable
from data.objects.models.singleton_checker import SingletonChecker

class DataBaseManager():
    """In this class we implement the SQL DataBase structure
    """
    def __init__(self):
        # Creation and connection to the DataBase
        self.mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)
        self.cursor = self.mydb.cursor(buffered=True)
        self.create_data_base()
        self.use_database()

        # Instantiation of the tables
        self.singleton_checker = SingletonChecker()
        self.products_table = ProductsTable(self)
        self.category_table = CategoriesTable(self)
        self.stores_table = StoresTable(self)

        # Create tables, link them together and fill them
        self.create_tables()
        #self.create_relations()
        self.fill_tables()
        #self.delete_database()

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
        self.products_table.create_table()
        self.category_table.create_table()
        self.stores_table.create_table()

    def create_relations(self):
        self.products_table.create_relations()
        self.category_table.create_relations()
        self.stores_table.create_relations()

    def insert_into_table(self, table, columns, values):
        pass

    def fill_tables(self):
        self.products_table.fill_table()
        self.category_table.fill_table()
        self.stores_table.fill_table()
        
        #for product in self.products_table.create_products():
        #    for key, value in product.__dict__.items():
        #        self.insert_into_table("products", key, value)
        #    self.insert_into_table("categories", "category_name", product.category_name)
        #    self.insert_into_table("stores", "store_name", product.store_name)

    def delete_database(self, name=constants.DATABASE_NAME):
        self.cursor.execute(f"""
        DROP DATABASE IF EXISTS {name}
        """)
