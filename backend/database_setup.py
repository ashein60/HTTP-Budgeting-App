import sqlite3

from backend.metadata.enums import MiscEnums


def init_all_dbs():
    init_transactions_db()
    init_category_group_db()
    init_summary_db()


def init_transactions_db():
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
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


def init_category_group_db():
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS category_group (
                        name TEXT PRIMARY KEY
                    )
                """

        connection.execute(query)


def init_summary_db():
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS summary (
                        category TEXT PRIMARY KEY,
                        category_group TEXT NOT NULL,
                        expected TEXT NOT NULL,
                        actual TEXT NOT NULL,
                        FOREIGN KEY (category_group)
                            REFERENCES category_group(name)
                    )
                """

        connection.execute(query)
