"""Constants relatives to the DataBase
"""

# Standard library import
import os

# Third party import

# Local application imports

# MySQL configuration
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_CONFIG = {
            "user": "root",
            "password": MYSQL_PASSWORD,
            "host": "localhost",
            "auth_plugin": "mysql_native_password",
        }
