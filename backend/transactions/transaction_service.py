import sqlite3
from csv import DictReader
from datetime import datetime
from sqlite3 import Connection

from backend.metadata.enums import CapOneCheckingAndSavingsFields, MiscEnums
from backend.transactions.transaction import Transaction

# ==================== Public Methods ====================


def import_transactions(reader: DictReader[str]):
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        transactions = get_transactions()

        if CapOneCheckingAndSavingsFields.ACCOUNT_NUMBER.value in reader.fieldnames:
            transaction_factory = Transaction.from_checking_and_saving_account_csv_row
        else:
            transaction_factory = Transaction.from_credit_card_csv_row

        for row in reader:
            transaction = transaction_factory(row)
            if transaction not in transactions:
                _insert_transaction(connection, transaction)


def get_transactions() -> list[Transaction]:
    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format
        rows = connection.execute("SELECT * FROM transactions").fetchall()

        return _convert_rows_to_transactions(rows)


def get_transactions_by_period(period: datetime) -> list[Transaction]:
    start_date, end_date = _convert_to_month_range(period)

    with sqlite3.connect(MiscEnums.DATABASE.value) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format

        query = """
                    SELECT * FROM transactions
                    WHERE date >= ?
                    AND date < ?
                """

        rows = connection.execute(query, (start_date, end_date)).fetchall()

        return _convert_rows_to_transactions(rows)


# ==================== Private Methods ====================


def _insert_transaction(connection: Connection, transaction: Transaction):
    query = "INSERT INTO transactions (date, account, description, category, debit, credit) VALUES (?, ?, ?, ?, ?, ?)"
    connection.execute(query, transaction.params)


def _convert_rows_to_transactions(rows: list) -> list[Transaction]:
    transactions = []

    for row in rows:
        transaction = Transaction.from_sql_row(row)
        transactions.append(transaction)

    return transactions


def _convert_to_month_range(period: datetime) -> tuple[str, str]:
    """Converts YYYY_MM datetime to an inclusive start date and exclusive end date"""

    start_date = period.replace(day=1).strftime("%Y-%m-%d")

    if period.month == 12:
        end_date = period.replace(year=period.year + 1, month=1, day=1).strftime(
            "%Y-%m-%d"
        )
    else:
        end_date = period.replace(month=period.month + 1, day=1).strftime("%Y-%m-%d")

    return start_date, end_date
