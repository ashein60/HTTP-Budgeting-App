from metadata.enums import Misc_enums
from transactions.transaction import Transaction

import sqlite3

# Enums for importing Checking and Savings account data
ACCOUNT_NUMBER = 'Account Number'
TRANSACTION_DESCRIPTION = 'Transaction Description'
TRANSACTION_DATE = 'Transaction Date'
TRANSACTION_TYPE = 'Transaction Type'
TRANSACTION_AMOUNT = 'Transaction Amount'

# Enums for importing Credit Card account data
POSTED_DATE = 'Posted Date'
CARD_NUMBER = 'Card No.'
DESCRIPTION = 'Description'
CATEGORY = 'Category'
DEBIT = 'Debit'
CREDIT = 'Credit' 

def import_transactions(reader):
    with sqlite3.connect(Misc_enums.DATABASE.value) as connection:
        if 'Account Number' in reader.fieldnames:
            import_checking_saving_account(reader, connection)
        else:
            import_credit_card_account(reader, connection)
            

def import_checking_saving_account(reader, connection):
    for row in reader:
        transaction_type = row[TRANSACTION_TYPE]
        
        transaction = Transaction(
            date = row[TRANSACTION_DATE],
            account = row[ACCOUNT_NUMBER],
            description = row[TRANSACTION_DESCRIPTION],
            category = str(row[TRANSACTION_DESCRIPTION]).split()[0],
            debit = float(row[TRANSACTION_AMOUNT] or 0) if transaction_type == DEBIT else 0,
            credit = float(row[TRANSACTION_AMOUNT] or 0) if transaction_type == CREDIT else 0
        )

        execute_connection(connection, transaction)

def import_credit_card_account(reader, connection):
    for row in reader:
        transaction = Transaction(
            date = row[POSTED_DATE],
            account = row[CARD_NUMBER],
            description = row[DESCRIPTION],
            category = row[CATEGORY],
            debit = row[DEBIT],
            credit = row[CREDIT]
        )

        execute_connection(connection, transaction)

def execute_connection(connection, transaction):
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