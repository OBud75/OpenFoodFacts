"""
"""

class ProductHasSubstitutesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def get_substitutes_of_product_in_category(self, product_name, category_name):
        query = ("""
            SELECT DISTINCT product_name, link, nutrition_grades
            FROM products JOIN product_has_categories JOIN categories
            WHERE categories.category_id IN (SELECT category_id FROM categories WHERE category_name = %s)
            AND products.nutrition_grades <= (SELECT nutrition_grades FROM products WHERE product_name = %s)
            ORDER BY nutrition_grades
        """)
        data = (category_name, product_name[0])
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
        data = (
            product_id[0], substitute_id[0]
        )
        self.database_manager.cursor.execute(statement, data)
        self.database_manager.mydb.commit()

    def get_products_with_substitutes(self):
        self.database_manager.cursor.execute("""
            SELECT *
            FROM product_has_substitutes
        """)
        results = self.database_manager.cursor.fetchall()
        print(results)
        return results
