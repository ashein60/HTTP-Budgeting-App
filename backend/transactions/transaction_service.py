from metadata.enums import Misc_enums
from transactions.transaction import Transaction

import transaction_service_impl

import sqlite3

def import_transactions(reader):
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        if 'Account Number' in reader.fieldnames:
            transaction_service_impl.import_checking_saving_account(reader, connection)
        else:
            transaction_service_impl.import_credit_card_account(reader, connection)

def get_all_transactions() -> Transaction | None:
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT * FROM transactions"
        ).fetchall()

        transactions = []

        for row in rows:
            transaction = Transaction.from_sql_row(row)
            transactions.append(transaction)

        return transactions if len(transactions) > 0 else None