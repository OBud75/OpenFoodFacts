# coding: utf-8
#! /usr/bin/env python3

"""Implémentation du modèle d'un produit
Les informations de chaque instances de cette classe
seront injectées dans la table "products"
"""

# Local application imports
from database.models.product_has_categories_model import ProductHasCategoriesModel
from database.models.category_has_categories_model import CategoryHasCategoriesModel
from database.models.product_has_stores_model import ProductHasStoresModel
from database.models.category_model import CategoryModel

class ProductModel:
    """Modèle d'un produit
    """
    def __init__(self, **product_infos):
        """Initialisation de l'instance avec les informations du produit
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
        """Création de l'attribut product_has_categories
        Cet attribut est une instance de ProductHasCategoriesModel
        ProductHasCategoriesModel a deux attributs:
        L'instance de ProductModel
        Une liste d'instances de category_has_categories,
        qui sont les catégories liées au produit
        Category_has_categories a deux attributs:
        L'instance de la catégorie
        Des instances des catégories (childs) liées à la première catégorie

        Args:
            categories_names (Str): Nom des catégories

        Returns:
            ProductHasCategoriesModel: Lien entre un produit et des catégories
        """
        categories_have_categories = list()
        last_category = CategoryModel(categories_names[-1])
        category_has_categories = CategoryHasCategoriesModel(last_category, None)
        categories_have_categories.append(category_has_categories)

        if len(categories_names) != 1:
            for parent_category in range(len(categories_names) - 1):
                category = CategoryModel(categories_names[parent_category])

                # Catégories liées à la première
                child_categories = list()
                for child_category in range(parent_category + 1, len(categories_names)):
                    child_category = CategoryModel(categories_names[child_category])
                    child_categories.append(child_category)

                category_has_categories = CategoryHasCategoriesModel(category, *child_categories)
                categories_have_categories.append(category_has_categories)
        return ProductHasCategoriesModel(self, *categories_have_categories)
