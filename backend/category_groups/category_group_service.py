import sqlite3

from backend import flask_handler
from backend.category_groups.category_group import CategoryGroup

# ==================== Public Methods ====================


def add_category_group(name: str):
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        query = "INSERT INTO category_groups (name) VALUES (?)"
        connection.execute(
            query,
            (name,),  # name, communicates it's a tuple as required
        )


def get_category_groups() -> list[CategoryGroup]:
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format
        rows = connection.execute("SELECT * FROM category_groups").fetchall()

        return _convert_rows_to_category_groups(rows)


def delete_category_group_by_name(name: str) -> bool:
    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        query = "DELETE FROM category_groups WHERE name = ?"
        cursor = connection.execute(
            query,
            (name,),  # name, communicates it's a tuple as required
        )

        return cursor.rowcount > 0


# ==================== Private Methods ====================


def _convert_rows_to_category_groups(rows: list) -> list[CategoryGroup]:
    category_groups = []

    for row in rows:
        category_group = CategoryGroup.from_sql_row(row)
        category_groups.append(category_group)

    return category_groups
