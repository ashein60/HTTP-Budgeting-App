from metadata.enums import Misc_enums 
from metadata import flask_setup

import sqlite3

# Required to access POST and GET requests
from transactions import transaction_controller

def init_database():
        with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    account TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    debit TEXT NOT NULL,
                    credit TEXT NOT NULL
                )
        """)

if __name__ == "__main__":
    init_database()
    flask_setup.app.run(host="127.0.0.1", port=5000, debug=True)