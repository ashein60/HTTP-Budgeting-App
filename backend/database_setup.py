import sqlite3

from backend.metadata.enums import Misc_enums


def init_all_dbs():
    init_transactions_db()


def init_transactions_db():
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        date TEXT NOT NULL,
                        account TEXT NOT NULL,
                        description TEXT NOT NULL,
                        category TEXT NOT NULL,
                        debit TEXT NOT NULL,
                        credit TEXT NOT NULL
                    )
                """

        connection.execute(query)
