# coding: utf-8
#! /usr/bin/env python3

"""File used to launch the application
We manage the argument with the argv import
This argument corresponds to the mode of the database_manager
Create mode for the first launch and normal for the following ones
python launcher.py database for creation (first launch)
python launcher.py for the following
"""

# Standard library import
from sys import argv
from sys import exit

# Local application imports
from database.database_manager import DataBaseManager
from app.application_manager import ApplicationManager

def check_argv():
    """We get an additional argument thanks to the argv module

    Returns:
        Str: Normal or create mode for the creation of the database
    """
    if len(argv) == 2 and argv[1] == "database":
        return "create"
    if len(argv) == 1:
        return "normal"
    exit("Create database: python launcher.py database\nUsage: python launcher.py")

def main():
    """Function to launch the application
    We use aggregation and create 2 main instances
    One to manage the database
    The second to manage the application
    """
    mode = check_argv()
    database_manager = DataBaseManager(mode)

    if mode == "create":
        exit("Création de la base de données terminée avec succès")

    application_manager = ApplicationManager(database_manager)
    application_manager.run()


if __name__ == "__main__":
    main()
