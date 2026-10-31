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


class CategoryFields(Enum):
    NAME = "name"
    EXPECTED = "expected"
    GROUP_NAME = "group_name"


class MessageFields(Enum):
    IMPORT_SUCCESS = "IMPORT_SUCCESS"
    IMPORT_FAIL = "IMPORT_FAIL"
    INVALID_PERIOD = "INVALID_PERIOD"
    GET_SUCCESS = "GET_SUCCESS"
    GET_BY_SUCCESS = "GET_BY_SUCCESS"
    INVALID_CATEGORY = "INVALID_CATEGORY"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    POST_SUCCESS = "POST_SUCCESS"
    NOT_FOUND = "NOT_FOUND"
    DELETE_SUCCESS = "DELETE_SUCCESS"
    DATA_MISSING = "DATA_MISSING"
    INVALID_DATA = "INVALID_DATA"
    FOREIGN_KEY_NOT_FOUND = "FOREIGN_KEY_NOT_FOUND"


class SqliteErrorFields(Enum):
    SQLITE_CONSTRAINT_PRIMARYKEY = "SQLITE_CONSTRAINT_PRIMARYKEY"
    SQLITE_CONSTRAINT_FOREIGNKEY = "SQLITE_CONSTRAINT_FOREIGNKEY"


class MessageCatalogFields(Enum):
    SUCCESS = "success"
    CODE = "code"
    MESSAGE = "message"
    DATA = "data"


class MiscEnums(Enum):
    DATABASE = "database.db"
