# coding: utf-8
#! /usr/bin/env python3

"""
"""

class ProductHasSubstitutesModel:
    def __init__(self, product, *substitutes):
        self.product = product
        self.substitutes = [substitute for substitute in substitutes]
