from dataclasses import dataclass

from backend.metadata.enums import CategoryFields


@dataclass
class Category:
    name: str
    expected: str
    group_name: str

    @classmethod
    def from_sql_row(cls, row):
        return cls(
            name=str(row[CategoryFields.NAME.value]).strip().title(),
            expected=str(row[CategoryFields.EXPECTED.value]).strip().title(),
            group_name=str(row[CategoryFields.GROUP_NAME.value]).strip().title(),
        )

    @property
    def params(self):
        return (self.name, self.expected, self.group_name)
