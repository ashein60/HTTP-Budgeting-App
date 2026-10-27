import sqlite3

from backend.metadata.enums import MiscEnums


def add_category_group(name: str):
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        query = "INSERT INTO category_group (name) VALUES (?)"
        connection.execute(
            query,
            (name,),  # name, communicates it's a tuple as required
        )
