from csv import DictReader
from sqlite3 import Connection

from backend.metadata.enums import Cap_One_Checking_Enums
from backend.transactions import transaction_service
from backend.transactions.transaction import Transaction


def import_account(reader: DictReader[str], connection: Connection):
    transactions = transaction_service.get_transactions() or []

    if Cap_One_Checking_Enums.ACCOUNT_NUMBER.value in reader.fieldnames:
        transaction_factory = Transaction.from_checking_and_saving_account_csv_row
    else:
        transaction_factory = Transaction.from_credit_card_csv_row

    for row in reader:
        transaction = transaction_factory(row)
        if transaction not in transactions:
            insert_transaction(connection, transaction)


def insert_transaction(connection: Connection, transaction: Transaction):
    query = "INSERT INTO transactions (date, account, description, category, debit, credit) VALUES (?, ?, ?, ?, ?, ?)"
    connection.execute(query, transaction.params)
