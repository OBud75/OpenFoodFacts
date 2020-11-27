"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Standard library import
from pprint import pprint

# Third party import
import requests
from MySQLdb import _mysql
import mysql.connector

# Local application imports
from data.tables.products_table import ProductsTable
from data.tables.categories_table import CategoryTable
from data.tables.stores_table import StoreTable

class DataBaseManager():
    """In this class we implement the SQL DataBase structure
    """
    def __init__(self):
        self.mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)
        self.cursor = self.mydb.cursor(buffered=True)

        self.create_data_base()

        self.products_table = ProductsTable(self)
        self.category_table = CategoryTable(self)
        self.stores_table = StoreTable(self)

        self.create_tables()
        self.fill_data_base()

    def create_data_base(self):
        self.cursor.execute("""
        CREATE DATABASE openfoodfact CHARACTER SET 'utf8';
        USE openfoodfact;
        """)

    def create_tables(self):
        self.products_table.create_table()
        self.category_table.create_table()
        self.stores_table.create_table()

    def fill_data_base(self):
        self.products_table.fill_table()
        self.category_table.fill_table()
        self.stores_table.fill_table()