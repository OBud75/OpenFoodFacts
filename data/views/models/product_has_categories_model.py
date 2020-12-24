from data.views.models.category_model import CategoryModel

class ProductCategories:
    def __init__(self, product, *product_categories):
        self.product = product
        self.categories = [CategoryModel(category_name) for category_name in product_categories]