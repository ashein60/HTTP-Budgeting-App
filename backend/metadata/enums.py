from enum import Enum

class Transaction_Enums(Enum):
    ID = 'id'
    DATE = 'date'
    ACCOUNT = 'account'
    DESCRIPTION = 'description'
    CATEGORY = 'category'
    DEBIT = 'debit'
    CREDIT = 'credit'

class Misc_enums(Enum):
    DATABASE = "database.db"