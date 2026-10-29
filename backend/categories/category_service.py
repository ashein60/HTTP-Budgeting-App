import sqlite3

from backend import flask_handler
from backend.categories.category import Category

# ==================== Public Methods ====================


def add_category(category: Category):
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")

        query = "INSERT INTO categories (name, group_name) VALUES (?, ?)"
        connection.execute(query, category.params)


def get_categories() -> list[Category]:
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format
        rows = connection.execute("SELECT * FROM categories").fetchall()

        return _convert_rows_to_categories(rows)


def delete_category_by_name(name: str) -> bool:
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        query = "DELETE FROM categories WHERE name = ?"
        cursor = connection.execute(
            query,
            (name,),  # name, communicates it's a tuple as required
        )

        return cursor.rowcount > 0


# ==================== Private Methods ====================


def _convert_rows_to_categories(rows: list) -> list[Category]:
    categories = []

    for row in rows:
        category = Category.from_sql_row(row)
        categories.append(category)

    return categories
