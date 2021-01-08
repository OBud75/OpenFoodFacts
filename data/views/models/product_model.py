"""
"""

# Local application imports
from data.views.models.product_has_categories_model import ProductHasCategories
from data.views.models.product_has_stores_model import ProductHasStores

class ProductModel:
    def __init__(self, **product_infos):
        self.code = product_infos.get("code")
        self.product_name = product_infos.get("product_name")
        self.ingredients_text = product_infos.get("ingredients_text")
        self.nutrition_grades = product_infos.get("nutrition_grades", "?")
        self.link = f"https://world.openfoodfacts.org/product/{self.code}/{self.product_name.replace(' ', '-')}"

        self.product_has_categories = ProductHasCategories(self, *product_infos.get("categories_hierarchy", "None"))
        self.product_has_stores = ProductHasStores(self, product_infos.get("store_name", "None"))
