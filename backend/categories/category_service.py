import sqlite3

from backend.categories.category import Category
from backend.metadata.enums import MiscEnums

# ==================== Public Methods ====================


def add_category(name: str):
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        query = "INSERT INTO categories (name) VALUES (?)"
        connection.execute(
            query,
            (name,),  # name, communicates it's a tuple as required
        )


def get_categories() -> list[Category]:
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format
        rows = connection.execute("SELECT * FROM categories").fetchall()

        return _convert_rows_to_categories(rows)


def delete_category_by_name(name: str) -> bool:
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
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
