"""
"""
# Local application imports

class ProductModel():
    def __init__(self, **product_infos):
        self.code = product_infos.get("code")
        self.product_name = product_infos.get("product_name")
        self.ingredients_text = product_infos.get("ingredients_text")
        self.nutrition_grades = product_infos.get("nutrition_grades", "?")
        self.link = f"https://world.openfoodfacts.org/product/{self.code}/{self.product_name.replace(' ', '-')}"
        self.category_name = product_infos.get("category_name").category_name
        self.store_name = product_infos.get("store_name").store_name
