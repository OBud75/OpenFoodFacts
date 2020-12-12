"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Standard library import

# Third party import
import mysql.connector

# Local application imports
from data import constants
from data.tables.products_table import ProductsTable
from data.tables.categories_table import CategoriesTable
from data.tables.stores_table import StoresTable

class DataBaseManager():
    """In this class we implement the SQL DataBase structure
    """
    def __init__(self, mode):
        # Creation and connection to the DataBase
        self.mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)
        self.cursor = self.mydb.cursor(buffered=True)
        
        if mode == "create":
            self.create_data_base()
        self.use_database()

        # Instantiation of the tables
        if mode == "create":
            self.products_table = ProductsTable(self)
            self.categories_table = CategoriesTable(self)
            self.stores_table = StoresTable(self)

            # Create tables, link them together and fill them
            self.create_tables()
            #self.create_relations()
            self.products_table.products_manager.create_products()
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
        self.categories_table.create_table()
        self.stores_table.create_table()

    def create_relations(self):
        self.products_table.create_relations()
        self.categories_table.create_relations()
        self.stores_table.create_relations()

    def delete_database(self, name=constants.DATABASE_NAME):
        self.cursor.execute(f"""
        DROP DATABASE IF EXISTS {name}
        """)
