from dataclasses import dataclass
from datetime import date as datetime

from backend.metadata.enums import (
    CapOneCheckingAndSavingsFields,
    CapOneCreditCardFields,
    TransactionFields,
)


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
            id=row[TransactionFields.ID.value],
            date=row[TransactionFields.DATE.value],
            account=row[TransactionFields.ACCOUNT.value],
            description=row[TransactionFields.DESCRIPTION.value],
            category=row[TransactionFields.CATEGORY.value],
            debit=row[TransactionFields.DEBIT.value],
            credit=row[TransactionFields.CREDIT.value],
        )

    @classmethod
    def from_checking_and_saving_account_csv_row(cls, row):
        transaction_type = row[CapOneCheckingAndSavingsFields.TRANSACTION_TYPE.value]

        # Capital One Checking/Savings accounts format date like 10/12/26 and need to be 2026-10-12
        date_unformatted = row[CapOneCheckingAndSavingsFields.TRANSACTION_DATE.value]
        date_formated = datetime.strptime(date_unformatted, "%m/%d/%y").strftime(
            "%Y-%m-%d"
        )

        return cls(
            id=None,
            date=date_formated,
            account=row[CapOneCheckingAndSavingsFields.ACCOUNT_NUMBER.value],
            description=row[
                CapOneCheckingAndSavingsFields.TRANSACTION_DESCRIPTION.value
            ],
            category=str(
                row[CapOneCheckingAndSavingsFields.TRANSACTION_DESCRIPTION.value]
            ).split()[0],
            debit=row[CapOneCheckingAndSavingsFields.TRANSACTION_AMOUNT.value]
            if transaction_type == CapOneCreditCardFields.DEBIT.value
            else "",
            credit=row[CapOneCheckingAndSavingsFields.TRANSACTION_AMOUNT.value]
            if transaction_type == CapOneCreditCardFields.CREDIT.value
            else "",
        )

    @classmethod
    def from_credit_card_csv_row(cls, row):
        return cls(
            id=None,
            date=row[CapOneCreditCardFields.POSTED_DATE.value],
            account=row[CapOneCreditCardFields.CARD_NUMBER.value],
            description=row[CapOneCreditCardFields.DESCRIPTION.value],
            category=row[CapOneCreditCardFields.CATEGORY.value],
            debit=row[CapOneCreditCardFields.DEBIT.value],
            credit=row[CapOneCreditCardFields.CREDIT.value],
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
            self.credit,
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
