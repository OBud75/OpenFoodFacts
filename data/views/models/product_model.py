# coding: utf-8
#! /usr/bin/env python3

"""
"""

# Local application imports
from data.views.models.product_has_categories_model import ProductHasCategoriesModel
from data.views.models.category_has_categories_model import CategoryHasCategoriesModel
from data.views.models.product_has_stores_model import ProductHasStoresModel
from data.views.models.category_model import CategoryModel

class ProductModel:
    def __init__(self, **product_infos):
        self.product_id = product_infos.get("product_id", None)
        self.code = int(product_infos.get("code"))
        self.product_name = product_infos.get("product_name")
        self.ingredients_text = product_infos.get("ingredients_text")
        self.nutrition_grades = product_infos.get("nutrition_grades")
        self.link = f"https://world.openfoodfacts.org/product/{self.code}/{self.product_name.replace(' ', '-')}"
        
        categories_names = product_infos.get("categories_hierarchy")
        if categories_names:
            self.product_has_categories = self.get_product_has_categories(categories_names)
    
        self.product_has_stores = ProductHasStoresModel(self, product_infos.get("store_name", "None"))

    def get_product_has_categories(self, categories_names):
            categories_have_categories = list()
            last_category = CategoryModel(categories_names[-1])
            category_has_categories = CategoryHasCategoriesModel(last_category, None)
            categories_have_categories.append(category_has_categories)

            if len(categories_names) != 1:
                for parent_category in range(len(categories_names) - 1):
                    category = CategoryModel(categories_names[parent_category])

                    child_categories = list()
                    for child_category in range(parent_category + 1, len(categories_names)):
                        child_category = CategoryModel(categories_names[child_category])
                        child_categories.append(child_category)

                    category_has_categories = CategoryHasCategoriesModel(category, *child_categories)
                    categories_have_categories.append(category_has_categories)

            return ProductHasCategoriesModel(self, *categories_have_categories)
