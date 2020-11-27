#! /usr/bin/env python3

"""File used to launch the app
"""

# Standard library import
import requests

# Third party import

# Local application imports
from data.tables.products_table import ProductsTable

def initializations():
    pass

def main():
    pass



if __name__ == "__main__":
    test = ProductsTable()
    test.get_products()
    for product in test.products_list:
        print(product.name)
    
    print(create_products())