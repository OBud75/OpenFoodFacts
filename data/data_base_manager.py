"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Standard library import

# Third party import
import mysql.connector

# Local application imports
from data import constants
from data.views.managers.products_manager import ProductsManager

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
            self.create_tables()
            #self.create_relations()
            self.products_manager = ProductsManager(self)
            self.products_manager.create_products()
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

    def delete_database(self, name=constants.DATABASE_NAME):
        self.cursor.execute(f"""
        DROP DATABASE IF EXISTS {name}
        """)

    def create_tables(self):
        # Create products table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            code BIGINT UNSIGNED,
            product_name VARCHAR(100) NOT NULL,
            ingredients_text TEXT(100),
            nutrition_grades VARCHAR(1) NOT NULL,
            link VARCHAR(150) NOT NULL,
            category_name VARCHAR(500) NOT NULL,
            category_id INT UNSIGNED,
            store_name VARCHAR(45),
            store_id INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Create categories table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL,
            products INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

        # Create stores table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            store_name VARCHAR(45),
            products INT UNSIGNED
            )
        ENGINE=INNODB;
        """)

    def create_relations(self):
        # For products tables
        self.cursor.execute("""
        ALTER TABLE products
            ADD CONSTRAINT fk_products_has_categories_category_id
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id),

            ADD CONSTRAINT fk_products_has_stores_store_name
            FOREIGN KEY (store_id)
            REFERENCES stores(store_id),

            ADD CONSTRAINT fk_products_has_substitutes
            FOREIGN KEY (id)
            REFERENCES products(id),
        ENGINE=INNODB;
        """)

        # For categories table
        self.cursor.execute("""
        ALTER TABLE categories
            ADD CONSTRAINT fk_categories_has_products_product_id
            FOREIGN KEY (products)
            REFERENCES products(id),
        ENGINE=INNODB;
        """)

        # For stores table
        self.cursor.execute("""
        ALTER TABLE stores
            ADD CONSTRAINT fk_stores_has_products_product_code
            FOREIGN KEY (products)
            REFERENCES products(id),
        ENGINE=INNODB;
        """)
