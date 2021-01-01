"""
"""

class ProductHasCategoriesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product_has_categories):
        product_name = product_has_categories.product
        categories = product_has_categories.categories

        product_id = self.database_manager.products_manager.get_product_id_by_name(product_name)[0]
        for category in categories:
            for category_name in category.category_name:
                category_id = self.database_manager.products_manager.categories_manager.get_category_id_by_name(category_name)[0]
                self.add_to_table(product_id, category_id)

    def add_to_table(self, product_id, category_id):
        statement = (
            "INSERT INTO product_has_categories"
            "(product_id, category_id)"
            "VALUES (%s, %s)"
        )
        data = (
            product_id, category_id
        )
        self.database_manager.cursor.execute(statement, data)


# UPDATE table
# SET categories_id = categories_id + 'nouvelle valeur'
# WHERE product_id = retour sql

"""
        SI self.pk:
            UPDATE categories SET nom = self.name WHERE pk = self.pk
        SINON
            INSERT INTO categories ('nom') VALUES (self.name)
            self.pk = retour_sql['pk']
"""