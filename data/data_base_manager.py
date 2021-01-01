"""In this file we implement the database manager
Creation of the database and the tables
Use of MySQL (cursors, connector...)
"""

# Third party import
import mysql.connector

# Local application imports
from data import constants
from data.views.managers.products_manager import ProductsManager

class DataBaseManager:
    """In this class we implement the SQL DataBase structure
    """
    def __init__(self, mode):
        # Creation and connection to the DataBase
        self.mydb = mysql.connector.connect(**constants.MYSQL_CONFIG)
        self.cursor = self.mydb.cursor(buffered=True)
        self.products_manager = ProductsManager(self)

        if mode == "create":
            self.create_data_base()
        self.use_database()

        # Instantiation of the tables
        if mode == "create":
            self.create_tables()
            self.create_relations()
            self.products_manager.create_products()
            #self.delete_database()
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

    def delete_database(self, name=constants.DATABASE_NAME):
        self.cursor.execute(f"""
        DROP DATABASE IF EXISTS {name}
        """)

    def create_tables(self):
        # Create products table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            ingredients_text TEXT(100),
            nutrition_grades VARCHAR(1) NOT NULL,
            link VARCHAR(150) NOT NULL
            )
        ENGINE=INNODB;
        """)

        # Create categories table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL
            )
        ENGINE=INNODB;
        """)

        # Create stores table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            store_name VARCHAR(45)
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
