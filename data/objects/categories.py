"""In this file we put all the informations relatives to a category
"""

# Standard library import

# Third party import

# Local application imports


class Category:
    """Class representing a single category
    """
    categories = []

    def __new__(cls, category_name):
        """Check if category already exists

        Args:
            category_name (Str): Name of the category

        Returns:
            Object: Instance of category
        """
        # Pick category if already exists
        for category in cls.categories:
            if category.category_name == category_name:
                return category

        # Else, create new category and add it to the categories list
        category = super().__new__(cls)
        cls.categories.append(category)
        return category

    def __init__(self, category_name):
        self.category_name = category_name

    def get_categories_of_product(self, product):
        pass