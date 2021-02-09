# coding: utf-8
#! /usr/bin/env python3

"""Product model implementation
The information of each instance of this class
will be injected into the "products" table
"""

# Local application imports
from database.models.product_has_categories_model import ProductHasCategoriesModel
from database.models.category_has_categories_model import CategoryHasCategoriesModel
from database.models.product_has_stores_model import ProductHasStoresModel
from database.models.category_model import CategoryModel

class ProductModel:
    """Model of a product
    """
    def __init__(self, **product_infos):
        """Initializing the instance with product information
        """
        self.product_id = product_infos.get("product_id")
        self.code = int(product_infos.get("code"))
        self.product_name = product_infos.get("product_name")
        self.ingredients_text = product_infos.get("ingredients_text")
        self.nutrition_grades = product_infos.get("nutrition_grades")

        no_space_name = self.product_name.replace(' ', '-')
        self.link = f"https://world.openfoodfacts.org/product/{self.code}/{no_space_name}"

        categories_names = product_infos.get("categories_hierarchy")
        if categories_names:
            self.product_has_categories = self.get_product_has_categories(categories_names)

        stores_names = product_infos.get("stores_tags")
        if stores_names:
            self.product_has_stores = ProductHasStoresModel(self, *stores_names)
        else:
            self.product_has_stores = None

    def get_product_has_categories(self, categories_names):
        """Creating the product_has_categories attribute
        This attribute is an instance of ProductHasCategoriesModel
        ProductHasCategoriesModel has two attributes:
        The ProductModel instance
        A list of instances of category_has_categories,
        which are the categories related to the product
        Category_has_categories has two attributes:
        Category instance
        Instances of categories (childs) linked to the first category

        Args:
            categories_names (Str): Categories names

        Returns:
            ProductHasCategoriesModel: Link between a product and categories
        """
        categories_have_categories = list()
        last_category = CategoryModel(categories_names[-1])
        category_has_categories = CategoryHasCategoriesModel(last_category, None)
        categories_have_categories.append(category_has_categories)

        if len(categories_names) != 1:
            for parent_category in range(len(categories_names) - 1):
                category = CategoryModel(categories_names[parent_category])

                # Categories linked to the first one
                child_categories = list()
                for child_category in range(parent_category + 1, len(categories_names)):
                    child_category = CategoryModel(categories_names[child_category])
                    child_categories.append(child_category)

                category_has_categories = CategoryHasCategoriesModel(category, *child_categories)
                categories_have_categories.append(category_has_categories)
        return ProductHasCategoriesModel(self, *categories_have_categories)
