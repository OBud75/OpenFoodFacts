

class ProductHasCategoriesManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product):
        product_name = product.product_name
        categories = product.categories