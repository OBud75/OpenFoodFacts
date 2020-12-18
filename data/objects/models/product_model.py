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
        
        # classe intermediaire
        # ProductCategories
        # self.product
        # self.category 

        self.category = product_infos.get("category_name")
        self.store = product_infos.get("store_name")
