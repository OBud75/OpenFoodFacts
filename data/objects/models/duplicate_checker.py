"""
"""
# Local application imports
from data.objects.categories import Category
from data.objects.stores import Store

class DuplicateChecker():
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def is_product_duplicate(self, **product_infos):
        if any(product_infos.values() == product.values() for product in self._products):
            return True
        self._products.append({**product_infos})
        return False

    def create_category(self, category_name):
        query = ("""
            SELECT category_name
            FROM categories
            WHERE category_name LIKE %s
        """)
        data = (category_name,)
        self.database_manager.cursor.execute(query, data)
        if self.database_manager.cursor.fetchone():
            return self.database_manager.cursor.fetchone()

        category = Category(category_name)
        return category

    def create_store(self, store_name):
        for store in self._stores:
            if store.store_name == store_name:
                return store
        store = Store(store_name)
        self._stores.append(store)
        return store
