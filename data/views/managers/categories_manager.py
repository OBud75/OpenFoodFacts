# Standard library import

# Third party import

# Local application imports
from data.views.models.category_model import CategoryModel
from data.views.models.product.product_categories import ProductCategories

class CategoriesManager:
    """Link between categories and database
    """
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def manage_categories(self, *categories_hierarchy):
        categories_id = list()
        for category_name in categories_hierarchy:
            if self.get_category_id_by_name(category_name) == None:
                self.create_category(category_name)

            category_id = self.get_category_id_by_name(category_name)
            categories_id.append(category_id)
            #self.update_table(category_id)
        return categories_id

    def get_category_id_by_name(self, category_name):
        query = ("""
                SELECT category_id
                FROM categories
                WHERE category_name LIKE %s
            """)
        data = (category_name,)
        self.database_manager.cursor.execute(query, data)
        return self.database_manager.cursor.fetchone()

    def create_category(self, category_name):
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