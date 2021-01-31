# coding: utf-8
#! /usr/bin/env python3
"""File used to launch the app
"""

# Standard library import
from sys import argv
from sys import exit

# Third party import
from PySide6 import QtWidgets

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
    graphic = Graphic(database_manager)
    return graphic

def main():
    qt_widget_app = QtWidgets.QApplication()
    graphic = initializations()
    graphic.show()
    exit(qt_widget_app.exec_())

if __name__ == "__main__":
    main()
