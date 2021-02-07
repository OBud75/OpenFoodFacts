# coding: utf-8
#! /usr/bin/env python3

"""Fichier utilisé pour lancer l'application
On gère l'argument avec l'import argv
Cet argument correspond au mode du database_manager
Mode create pour le premier lancement et normal pour les suivants
python launcher.py database pour la création (premier lancement)
python launcher.py pour les suivants
"""

# Standard library import
from sys import argv
from sys import exit

# Local application imports
from database.database_manager import DataBaseManager
from app.application_manager import ApplicationManager

def check_argv():
    """Nous récupérons un argument supplémentaire grâce au module argv

    Returns:
        Str: Mode normal ou create pour la création de la base de données
    """
    if len(argv) == 2 and argv[1] == "database":
        return "create"
    if len(argv) == 1:
        return "normal"
    exit("Create database: python launcher.py database\nUsage: python launcher.py")

def main():
    """Fonction pour lancer l'application
    Nous utilisons l'agrégation et créeons 2 instances principales
    Une pour gérer la base de données
    La seconde pour gérer l'application
    """
    mode = check_argv()
    database_manager = DataBaseManager(mode)

    if mode == "create":
        exit("Création de la base de données terminée avec succès")

    application_manager = ApplicationManager(database_manager)
    application_manager.run()


if __name__ == "__main__":
    main()
