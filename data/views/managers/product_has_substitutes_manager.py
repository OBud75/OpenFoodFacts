"""
"""

from data.views.models.product_model import ProductModel

class ProductHasSubstitutesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def get_substitutes(self, product):
        return [substitute for substitute in [self.database_manager.category_manager.get_products(category)
                for category in product.product_has_categories.categories]
                if self.has_categories_in_commun(substitute.product_has_categories, product.product_has_categories)]

    def has_categories_in_commun(self, substitute_has_categories, product_has_categories, nb_categories=5):
        # SELECT product_name
        # FROM products
        # WHERE COUNT(SELECT category_name
        #             FROM categories JOIN product_has_catgories JOIN products
        #             WHERE product_name IN blabla and category_name IN substitute_categories)
        
        query = ("""
            SELECT COUNT(category_name)
            FROM products JOIN product_has_categories JOIN categories
            WHERE 
        """)
        data = (product.product_name,)
        self.database_manager.cursor.execute(query, data)
        results = self.database_manager.cursor.fetchall()
        return results

    def save_substitute(self, product_name, substitute_name):
        product_id = self.database_manager.products_manager.get_product_id_by_name(product_name)
        substitute_id = self.database_manager.products_manager.get_product_id_by_name(substitute_name)
        statement = (
            "INSERT INTO product_has_substitutes"
            "(product_id, substitute_id)"
            "VALUES (%s, %s)"
        )
        data = (product_id[0], substitute_id[0])
        self.database_manager.cursor.execute(statement, data)
        self.database_manager.mydb.commit()

    def get_products_names_with_substitutes_names(self):
        self.database_manager.cursor.execute("""
            SELECT p1.product_name, p2.product_name
            FROM product_has_substitutes JOIN products AS p1 JOIN products as p2
        """)
        results = self.database_manager.cursor.fetchall()
        return results

    def get_products_with_substitutes(self):
        products = list()
        for product_with_substitute in self.get_products_names_with_substitutes_names():
            product = ProductModel(product_name=product_with_substitute[0])
            product.product_id = self.database_manager.products_manager.get_product_id_by_name(product_with_substitute[0])

            substitute = ProductModel(product_name=product_with_substitute[1])
            substitute.product_id = self.database_manager.products_manager.get_product_id_by_name(product_with_substitute[1])

            products.append((product, substitute))
        return products
