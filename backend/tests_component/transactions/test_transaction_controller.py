import sqlite3
from io import BytesIO

from werkzeug.test import TestResponse

from backend import flask_handler
from backend.database_setup import init_transactions_db
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import MessageCatalogFields, MessageFields

# Required to access POST and GET requests
from backend.transactions import transaction_controller  # noqa # isort: skip

# Files & Paths
DATA_PATH = "backend/tests_component/transactions/data/"
CHECKING_TRANSACTIONS = "checking_transactions.csv"
CREDIT_CARD_TRANSACTIONS = "credit_card_transactions.csv"
DATABASE = "database.db"

# APIs
IMPORT_API = "/transactions/import"
TRANSACTIONS_API = "/transactions"
TRANSACTIONS_PERIOD_API = "/transactions/period"

# Misc
TRANSACTIONS = "Transactions"

messages = MessageCatalog()

# ==================== /transaction/import ====================


def test_import_no_file(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(IMPORT_API, data={})

    assert response.get_json() == messages.get(MessageFields.IMPORT_FAIL.value)


def test_import_no_file_selected(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        IMPORT_API,
        data={"file": (BytesIO(b""), "")},
        content_type="multipart/form-data",
    )

    assert response.get_json() == messages.get(MessageFields.IMPORT_FAIL.value)


def test_import_checking_account(tmp_path):
    _init_db(tmp_path)

    response = _import_transactions(CHECKING_TRANSACTIONS)

    assert response.get_json() == messages.get(
        MessageFields.IMPORT_SUCCESS.value, items=TRANSACTIONS
    )


def test_import_credit_card(tmp_path):
    _init_db(tmp_path)

    response = _import_transactions(CREDIT_CARD_TRANSACTIONS)

    assert response.get_json() == messages.get(
        MessageFields.IMPORT_SUCCESS.value, items=TRANSACTIONS
    )


def test_import_duplicates(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response1 = flask_handler.app.test_client().get(TRANSACTIONS_API)
    count1 = len(response1.get_json())

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response2 = flask_handler.app.test_client().get(TRANSACTIONS_API)
    count2 = len(response2.get_json())

    assert count1 == count2


# ==================== /transaction ====================


def test_get_transactions_empty(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().get(TRANSACTIONS_API)

    assert response.get_json() == messages.get(
        MessageFields.GET_SUCCESS.value, [], items=TRANSACTIONS
    )


def test_get_checking_transactions_with_data(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CHECKING_TRANSACTIONS)

    response = flask_handler.app.test_client().get(TRANSACTIONS_API)
    count = len(response.get_json().get(MessageCatalogFields.DATA.value))

    assert count > 0


def test_get_credit_card_transactions_with_data(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response = flask_handler.app.test_client().get(TRANSACTIONS_API)
    count = len(response.get_json().get(MessageCatalogFields.DATA.value))

    assert count > 0


# ==================== /transaction/<string:period_str> ====================


def test_transactions_by_period_invalid(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().get(
        f"{TRANSACTIONS_PERIOD_API}/20166-10"
    )

    assert response.get_json() == messages.get(MessageFields.INVALID_PERIOD.value)


def test_transactions_by_period_out_of_range(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CHECKING_TRANSACTIONS)

    response = flask_handler.app.test_client().get(f"{TRANSACTIONS_PERIOD_API}/2001-10")
    count = len(response.get_json().get(MessageCatalogFields.DATA.value))

    assert count == 0


def test_checking_transactions_by_period_in_range(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CHECKING_TRANSACTIONS).get_json()

    response = flask_handler.app.test_client().get(f"{TRANSACTIONS_PERIOD_API}/2026-10")
    count = len(response.get_json().get(MessageCatalogFields.DATA.value))

    assert count > 0


def test_credit_card_transactions_by_period_in_range(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response = flask_handler.app.test_client().get(f"{TRANSACTIONS_PERIOD_API}/2026-10")
    count = len(response.get_json().get(MessageCatalogFields.DATA.value))

    assert count > 0


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    flask_handler.set_database_path(tmp_path / DATABASE)

    init_transactions_db()

    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        connection.execute("DELETE FROM transactions")


def _import_transactions(file_name: str) -> TestResponse:
    with open(f"{DATA_PATH}{file_name}", "rb") as file:
        return flask_handler.app.test_client().post(IMPORT_API, data={"file": file})
