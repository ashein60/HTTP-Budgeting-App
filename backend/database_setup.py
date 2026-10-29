import json
import os
import sqlite3

from backend import flask_handler

SEED_DATA_PATH = "backend/seed_data/"

# ==================== init_all_dbs ====================


def init_all_dbs():
    init_transactions_db()
    init_category_groups_db()
    init_categories_db()
    init_summary_db()


def init_transactions_db():
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
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


def init_category_groups_db():
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS category_groups (
                        name TEXT PRIMARY KEY
                    )
                """

        connection.execute(query)


def init_categories_db():
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS categories (
                        name TEXT PRIMARY KEY,
                        group_name TEXT NOT NULL,
                        FOREIGN KEY (group_name)
                            REFERENCES category_groups(name)
                    )
                """

        connection.execute(query)


def init_summary_db():
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS summary (
                        category TEXT PRIMARY KEY,
                        category_group TEXT NOT NULL,
                        expected TEXT NOT NULL,
                        actual TEXT NOT NULL
                    )
                """

        connection.execute(query)


# ==================== Seed Data ====================


def init_all_seed_data():
    init_category_groups_seed_data()
    init_categories_seed_data()


def init_category_groups_seed_data():
    file_path = f"{SEED_DATA_PATH}category_groups.json"
    data = get_data_from_file(file_path)

    if data is not None:
        with sqlite3.connect(flask_handler.get_database_path()) as connection:
            query = "INSERT OR IGNORE INTO category_groups (name) VALUES (?)"
            connection.executemany(
                query, [(row["name"],) for row in data["category_groups"]]
            )


def init_categories_seed_data():
    file_path = f"{SEED_DATA_PATH}categories.json"
    data = get_data_from_file(file_path)

    if data is not None:
        with sqlite3.connect(flask_handler.get_database_path()) as connection:
            query = "INSERT OR IGNORE INTO categories (name, group_name) VALUES (?, ?)"
            connection.executemany(
                query, [(row["name"], row["group_name"]) for row in data["categories"]]
            )


def get_data_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    return None
