"""
"""
# Local application imports
from data.objects.categories import Category
from data.objects.stores import Store

class SingletonChecker():
    def __init__(self):
        self._products_codes = list()
        self._categories = list()
        self._stores = list()

    def is_product_duplicate(self, code):
        for product_code in self._products_codes:
            if product_code == code:
                return True
        self._products_codes.append(code)
        return False
    
    def create_category(self, category_name):
        for category in self._categories:
            if category.category_name == category_name:
                return category
        category = Category(category_name)
        self._categories.append(category)
        return category

    def create_store(self, store_name):
        for store in self._stores:
            if store.store_name == store_name:
                return store
        store = Store(store_name)
        self._stores.append(store)
        return store
