"""
"""

class CategoriesManager:
    """Link between categories and database
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage_categories(self, *product_has_categories):
        for categories in product_has_categories:
            for category in categories.category_name:
                if not self.get_category_id_by_name(category):
                    self.add_to_table(category)

    def get_category_id_by_name(self, category):
        query = ("""
                SELECT category_id
                FROM categories
                WHERE category_name LIKE %s
            """)
        data = (category,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchone()

    def add_to_table(self, category):
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (
            category,
        )
        self.database_manager.cursor.execute(statement, data)
