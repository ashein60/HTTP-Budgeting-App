from metadata.enums import Misc_enums
from transactions.transaction import Transaction
from transactions import transaction_service_impl

import sqlite3

ACCOUNT_NUMBER = 'Account Number'

def import_transactions(reader):
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