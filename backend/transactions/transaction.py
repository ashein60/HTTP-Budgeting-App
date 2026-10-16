from metadata.enums import Transaction_Enums
from dataclasses import dataclass
from datetime import date as datetime

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

@dataclass
class Transaction:
    id: int
    date: datetime
    account: str
    description: str
    category: str
    debit: str
    credit: str

    @classmethod
    def from_sql_row(cls, row):
        return cls(
            id = row[Transaction_Enums.ID.value],
            date =  row[Transaction_Enums.DATE.value],
            account = row[Transaction_Enums.ACCOUNT.value],
            description = row[Transaction_Enums.DESCRIPTION.value],
            category = row[Transaction_Enums.CATEGORY.value],
            debit = row[Transaction_Enums.DEBIT.value],
            credit = row[Transaction_Enums.CREDIT.value]
        )

    @classmethod
    def from_checking_and_saving_account_csv_row(cls, row):
        transaction_type = row[TRANSACTION_TYPE]

        return cls(
            id = None,
            date = row[TRANSACTION_DATE],
            account = row[ACCOUNT_NUMBER],
            description = row[TRANSACTION_DESCRIPTION],
            category = str(row[TRANSACTION_DESCRIPTION]).split()[0],
            debit = float(row[TRANSACTION_AMOUNT] or 0) if transaction_type == DEBIT else 0,
            credit = float(row[TRANSACTION_AMOUNT] or 0) if transaction_type == CREDIT else 0
        )

    @classmethod
    def from_credit_card_csv_row(cls, row):
        return cls(
            id = None,
            date = row[POSTED_DATE],
            account = row[CARD_NUMBER],
            description = row[DESCRIPTION],
            category = row[CATEGORY],
            debit = row[DEBIT],
            credit = row[CREDIT]
        )