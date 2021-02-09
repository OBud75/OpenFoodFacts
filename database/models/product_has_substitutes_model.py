# coding: utf-8
#! /usr/bin/env python3

"""Model implementation of a registered surrogate
The information of each instance of this class
will be injected into the "product_has_substitutes" table
"""

class ProductHasSubstitutesModel:
    """Model of a registered substitute
    """
    def __init__(self, product, *substitutes):
        """Initializing instances

        Args:
            product (product): Product for which we have found substitutes
            substitutes (products): Product substitutes
        """
        self.product = product
        self.substitutes = [substitute for substitute in substitutes]
