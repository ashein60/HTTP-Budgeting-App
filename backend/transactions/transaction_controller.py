import csv
from datetime import datetime
from io import TextIOWrapper

from flask import request

from backend.flask_handler import app
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import MessageFields
from backend.transactions import transaction_service

messages = MessageCatalog()

TRANSACTIONS = "Transactions"


@app.route("/transactions/import", methods=["POST"])
def import_transactions():
    """Import CSVs from Capital One Checking and Savings Accounts and Credit Cards"""

    if "file" not in request.files:
        return messages.get(MessageFields.IMPORT_FAIL.value)

    file = request.files["file"]

    if file.filename == "":
        return messages.get(MessageFields.IMPORT_FAIL.value)

    reader = csv.DictReader(TextIOWrapper(file.stream, encoding="utf-8-sig"))

    transaction_service.import_transactions(reader)

    return messages.get(MessageFields.IMPORT_SUCCESS.value, items=TRANSACTIONS)


@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = transaction_service.get_transactions()

    return messages.get(
        MessageFields.GET_SUCCESS.value, transactions, items=TRANSACTIONS
    )


@app.route("/transactions/period/<string:period_str>", methods=["GET"])
def get_transactions_by_period(period_str):
    """Period format should be YYYY-MM"""
    try:
        period_datetime = datetime.strptime(period_str, "%Y-%m")
    except ValueError:
        return messages.get(MessageFields.INVALID_PERIOD.value)

    transactions = transaction_service.get_transactions_by_period(period_datetime)

    return messages.get(
        MessageFields.GET_BY_SUCCESS.value,
        transactions,
        items=TRANSACTIONS,
        by="period",
    )
