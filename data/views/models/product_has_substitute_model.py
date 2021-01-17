

class ProductHasSubstituteModel:
    def __init__(self, product, *substitutes):
        self.product = product
        self.substitutes = [substitute for substitute in substitutes]