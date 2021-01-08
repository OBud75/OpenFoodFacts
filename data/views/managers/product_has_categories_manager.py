"""
"""

class ProductHasCategoriesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product_has_categories):
        product = product_has_categories.product
        categories = product_has_categories.categories

        product.product_id = self.database_manager.products_manager.get_product_id_by_name(product)
        for category in categories:
            category.category_id = self.database_manager.categories_manager.get_category_id_by_name(category)
            self.add_to_table(product, category)

    def add_to_table(self, product, category):
        statement = (
            "INSERT INTO product_has_categories"
            "(product_id, category_id)"
            "VALUES (%s, %s)"
        )
        data = (product.product_id, category.category_id)
        self.database_manager.cursor.execute(statement, data)

"""
        SI self.pk:
            UPDATE categories SET nom = self.name WHERE pk = self.pk
        SINON
            INSERT INTO categories ('nom') VALUES (self.name)
            self.pk = retour_sql['pk']
"""