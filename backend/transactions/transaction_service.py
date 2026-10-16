from metadata.enums import Misc_enums
from transactions.transaction import Transaction

import sqlite3

def import_transactions(reader):
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        if 'Account Number' in reader.fieldnames:
            import_checking_saving_account(reader, connection)
        else:
            import_credit_card_account(reader, connection)
            

def import_checking_saving_account(reader, connection):
    for row in reader:
        transaction = Transaction.from_checking_and_saving_account_csv_row(row)
        insert_transaction(connection, transaction)

def import_credit_card_account(reader, connection):
    for row in reader:
        transaction = Transaction.from_checking_and_saving_account_csv_row(row)
        insert_transaction(connection, transaction)

def insert_transaction(connection, transaction):
    connection.execute(
        "INSERT INTO transactions (date, account, description, category, debit, credit) VALUES (?, ?, ?, ?, ?, ?)",
        (
            transaction.date,
            transaction.account,
            transaction.description,
            transaction.category,
            transaction.debit,
            transaction.credit
        )
    )

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