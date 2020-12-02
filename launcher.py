#! /usr/bin/env python3
"""File used to launch the app
"""

# Standard library import

# Third party import

# Local application imports
from data.data_base import DataBaseManager
from app.substitution_finder import SubstitutionFinder
from app.graphics import Graphic

def initializations():
    database_manager = DataBaseManager()
    substitution_finder = SubstitutionFinder(database_manager)
    graphic = Graphic(substitution_finder)
    return graphic

def main():
    graphic = initializations()
    graphic.main_loop()


if __name__ == "__main__":
    main()