from metadata.enums import Transaction_Enums
from metadata.enums import Cap_One_Checking_Enums
from metadata.enums import Cap_One_CC_Enums

from dataclasses import dataclass
from datetime import date as datetime

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
        transaction_type = row[Cap_One_Checking_Enums.TRANSACTION_TYPE]

        return cls(
            id = None,
            date = row[Cap_One_Checking_Enums.TRANSACTION_DATE],
            account = row[Cap_One_Checking_Enums.ACCOUNT_NUMBER],
            description = row[Cap_One_Checking_Enums.TRANSACTION_DESCRIPTION],
            category = str(row[Cap_One_Checking_Enums.TRANSACTION_DESCRIPTION]).split()[0],
            debit = row[Cap_One_Checking_Enums.TRANSACTION_AMOUNT] if transaction_type == Cap_One_CC_Enums.DEBIT else '',
            credit = row[Cap_One_Checking_Enums.TRANSACTION_AMOUNT] if transaction_type == Cap_One_CC_Enums.CREDIT else ''
        )

    @classmethod
    def from_credit_card_csv_row(cls, row):
        return cls(
            id = None,
            date = row[Cap_One_CC_Enums.POSTED_DATE],
            account = row[Cap_One_CC_Enums.CARD_NUMBER],
            description = row[Cap_One_CC_Enums.DESCRIPTION],
            category = row[Cap_One_CC_Enums.CATEGORY],
            debit = row[Cap_One_CC_Enums.DEBIT],
            credit = row[Cap_One_CC_Enums.CREDIT]
        )

    @property
    def params(self):
        """Does not include id"""
        return (
            self.date,
            self.account,
            self.description,
            self.category,
            self.debit,
            self.credit
        )

    def __eq__(self, other):
        """Does not include id or category"""
        if not isinstance(other, Transaction):
            return NotImplemented

        return (
            self.date == other.date
            and self.account == other.account
            and self.description == other.description
            and self.debit == other.debit
            and self.credit == other.credit
        )