from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    date: date
    account: str
    description: str
    category: str
    debit: str
    credit: str