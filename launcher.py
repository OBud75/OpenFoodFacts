# coding: utf-8
#! /usr/bin/env python3
"""File used to launch the app
"""

# Standard library import
from sys import argv
from sys import exit

# Local application imports
from database.database_manager import DataBaseManager
from app.application_manager import ApplicationManager

def check_argv():
    if len(argv) == 2 and argv[1] == "database":
        return "create"
    if len(argv) == 1:
        return "normal"
    exit("Create database: python launcher.py database\nUsage: python launcher.py")

def main():
    database_manager = DataBaseManager(mode=check_argv())
    application_manager = ApplicationManager(database_manager)
    application_manager.run()

if __name__ == "__main__":
    main()
