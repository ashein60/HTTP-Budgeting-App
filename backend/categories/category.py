from dataclasses import dataclass

from backend.metadata.enums import CategoryFields


@dataclass
class Category:
    name: str

    @classmethod
    def from_sql_row(cls, row):
        return cls(name=row[CategoryFields.NAME.value])
