from backend.transactions.transaction import Transaction
from backend.transactions import transaction_service_impl
from backend.metadata.enums import Misc_enums
from csv import DictReader


import sqlite3

def import_transactions(reader: DictReader[str]):
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        transaction_service_impl.import_account(reader, connection)

def get_transactions() -> Transaction | None:
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        connection.row_factory = sqlite3.Row # Allows csv style row format
        rows = connection.execute(
            "SELECT * FROM transactions"
        ).fetchall()

        transactions = []

        for row in rows:
            transaction = Transaction.from_sql_row(row)
            transactions.append(transaction)

        return transactions if len(transactions) > 0 else None