

class ProductCategories:
    def __init__(self, product, *product_categories):
        self.product = product
        self.categories = [category for category in product_categories]