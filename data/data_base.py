"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Standard library import
from pprint import pprint

# Third party import
import requests
import mysql.connector

# Local application imports
from data import constants
from data.tables.products_table import ProductsTable
#from data.tables.categories_table import CategoryTable
#from data.tables.stores_table import StoreTable

class DataBaseManager():
    """In this class we implement the SQL DataBase structure
    """
    def __init__(self):
        # Creation and connection to the DataBase
        mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)
        self.cursor = mydb.cursor(buffered=True)
        self.create_data_base()

        # Instantiation of the tables
        self.products_table = ProductsTable(self.cursor)
        #self.category_table = CategoryTable(self.cursor)
        #self.stores_table = StoreTable(self.cursor)

        # Create and fill the tables
        #self.create_tables()
        #self.fill_data_base()

    def create_data_base(self):
        self.cursor.execute("""
        CREATE DATABASE IF NOT EXISTS openfoodfact CHARACTER SET 'utf8';
        USE openfoodfact;
        """, multi=True)

    def create_tables(self):
        self.products_table.create_table()
        self.category_table.create_table()
        self.stores_table.create_table()

    def fill_data_base(self):
        self.products_table.fill_table()
        #self.category_table.fill_table()
        #self.stores_table.fill_table()