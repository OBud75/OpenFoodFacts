# Standard library import

# Third party import

# Local application imports
from data.objects.models.category_model import CategoryModel

class CategoriesManager:
    """Link between categories and database
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def get_category(self, category_name):
        query = ("""
            SELECT category_name
            FROM categories
            WHERE category_name LIKE %s
        """)
        data = (category_name,)
        self.database_manager.cursor.execute(query, data)
        category = self.database_manager.cursor.fetchone()
        
        if category != None:
            return category
        return self.create_store(category_name)
    
    def create_store(self, category_name):
        category = CategoryModel(category_name)
        self.add_to_table(category)
        return category

    def add_to_table(self, category):
        statement = (
            "INSERT INTO categories"
            "(category_name)"
            "VALUES (%s)"
        )
        data = (
            category.category_name,
        )
        self.database_manager.cursor.execute(statement, data)
"""
        SI self.pk:
            UPDATE categories SET nom = self.name WHERE pk = self.pk
        SINON
            INSERT INTO categories ('nom') VALUES (self.name)
            self.pk = retour_sql['pk']
"""