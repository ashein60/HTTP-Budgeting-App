from enum import Enum


class TransactionFields(Enum):
    ID = "id"
    DATE = "date"
    ACCOUNT = "account"
    DESCRIPTION = "description"
    CATEGORY = "category"
    DEBIT = "debit"
    CREDIT = "credit"


class CapOneCheckingAndSavingsFields(Enum):
    """CSV Table Headers from Capital One for Checking and Savings Accounts"""

    ACCOUNT_NUMBER = "Account Number"
    TRANSACTION_DESCRIPTION = "Transaction Description"
    TRANSACTION_DATE = "Transaction Date"
    TRANSACTION_TYPE = "Transaction Type"
    TRANSACTION_AMOUNT = "Transaction Amount"


class CapOneCreditCardFields(Enum):
    """CSV Table Headers from Capital One for the Credit Card"""

    POSTED_DATE = "Posted Date"
    CARD_NUMBER = "Card No."
    DESCRIPTION = "Description"
    CATEGORY = "Category"
    DEBIT = "Debit"
    CREDIT = "Credit"


class CategoryGroupFields(Enum):
    NAME = "name"


class MiscEnums(Enum):
    DATABASE = "database.db"
