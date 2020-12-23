import requests

class ApiManager:
    def __init__(self):
        pass

    def get_categories(self):
        categories_request = requests.get("https://world.openfoodfacts.org/categories.json").json()
        categories_tags = categories_request['tags']
        return [category['name'] for category in categories_tags][0:2]

    def get_products_of_categories(self):
        return {category: requests.get(f"https://world.openfoodfacts.org/category/{category}.json").json()['products']
                for category in self.get_categories()}

    def get_products_list(self):
        products_infos_list = []
        for category, products in self.get_products_of_categories().items():
            for product in products:
                product_infos = {key: product.get(key)
                                 for key in ["code", "product_name", "description", "nutrition_grades", "categories_hierarchy", "store_name"]
                                 if product.get(key) != None}
                products_infos_list.append(product_infos)
        return products_infos_list
