from enum import Enum


class Transaction_Enums(Enum):
    ID = "id"
    DATE = "date"
    ACCOUNT = "account"
    DESCRIPTION = "description"
    CATEGORY = "category"
    DEBIT = "debit"
    CREDIT = "credit"


class Cap_One_Checking_Enums(Enum):
    """CSV Table Headers from Capital One for Checking and Savings Accounts"""

    ACCOUNT_NUMBER = "Account Number"
    TRANSACTION_DESCRIPTION = "Transaction Description"
    TRANSACTION_DATE = "Transaction Date"
    TRANSACTION_TYPE = "Transaction Type"
    TRANSACTION_AMOUNT = "Transaction Amount"


class Cap_One_CC_Enums(Enum):
    """CSV Table Headers from Capital One for the Credit Card"""

    POSTED_DATE = "Posted Date"
    CARD_NUMBER = "Card No."
    DESCRIPTION = "Description"
    CATEGORY = "Category"
    DEBIT = "Debit"
    CREDIT = "Credit"


class Misc_enums(Enum):
    DATABASE = "database.db"
