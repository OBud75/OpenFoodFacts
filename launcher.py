# coding: utf-8
#! /usr/bin/env python3
"""File used to launch the app
"""

# Standard library import
from sys import argv
from sys import exit

# Third party import

# Local application imports
from app.views.database_manager import DataBaseManager
from app.substitution_finder import SubstitutionFinder
from app.graphics import Graphic

def check_argv():
    if len(argv) == 2 and argv[1] == "database":
        return "create"
    if len(argv) == 1:
        return "normal"
    exit("Create database: python launcher.py database\nUsage: python launcher.py")

def initializations():
    """Initializating instances

    Returns:
        Object: Grafical user interface
    """
    database_manager = DataBaseManager(mode=check_argv())
    substitution_finder = SubstitutionFinder(database_manager)
    graphic = Graphic(substitution_finder)
    return graphic

def main():
    graphic = initializations()
    graphic.main_loop()


if __name__ == "__main__":
    main()
