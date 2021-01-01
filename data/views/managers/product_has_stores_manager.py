"""
"""

class ProductHasStoresManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage(self, product_has_stores):
        product_name = product_has_stores.product
        stores = product_has_stores.stores

        product_id = self.database_manager.products_manager.get_product_id_by_name(product_name)
        for store in stores:
            if store.store_name != None:
                store_id = self.database_manager.products_manager.stores_manager.get_store_id_by_name(store.store_name)
                self.add_to_table(product_id, store_id)

    def add_to_table(self, product_id, store_id):
        statement = (
            "INSERT INTO product_has_stores"
            "(product_id, store_id)"
            "VALUES (%s, %s)"
        )
        data = (
            product_id, store_id
        )
        self.database_manager.cursor.execute(statement, data)
