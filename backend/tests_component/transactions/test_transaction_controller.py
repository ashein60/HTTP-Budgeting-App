import sqlite3
from io import BytesIO

from werkzeug.test import TestResponse

from backend.database_setup import init_transactions_db
from backend.flask_setup import app

# Required to access POST and GET requests
from backend.transactions import transaction_controller  # noqa

DATA_PATH = "backend/tests_component/transactions/data/"
CHECKING_TRANSACTIONS = "checking_transactions.csv"
CREDIT_CARD_TRANSACTIONS = "credit_card_transactions.csv"
DATABASE = "database.db"

# APIs
IMPORT_API = "/transactions/import"
TRANSACTIONS_API = "/transactions"

# ==================== /transaction/import ====================


def test_import_no_file(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(IMPORT_API, data={})

    assert response.get_json() == {"error": "No file provided"}
    assert response.status_code == 400


def test_import_no_file_selected(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(
        IMPORT_API,
        data={"file": (BytesIO(b""), "")},
        content_type="multipart/form-data",
    )

    assert response.get_json() == {"error": "No file selected"}
    assert response.status_code == 400


def test_import_checking_account(tmp_path):
    _init_db(tmp_path)

    response = _import_transactions(CHECKING_TRANSACTIONS)

    assert response.get_json() == {"success": "Transactions were imported successfully"}
    assert response.status_code == 201


def test_import_credit_card(tmp_path):
    _init_db(tmp_path)

    response = _import_transactions(CREDIT_CARD_TRANSACTIONS)

    assert response.get_json() == {"success": "Transactions were imported successfully"}
    assert response.status_code == 201


def test_import_duplicates(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response1 = app.test_client().get(TRANSACTIONS_API, data={})
    count1 = len(response1.get_json())

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response2 = app.test_client().get(TRANSACTIONS_API, data={})
    count2 = len(response2.get_json())

    assert count1 == count2


# ==================== /transaction ====================


def test_transactions_empty(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().get(TRANSACTIONS_API, data={})

    assert response.get_json() == []
    assert response.status_code == 200


def test_checking_transactions_with_data(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CHECKING_TRANSACTIONS)

    response = app.test_client().get(TRANSACTIONS_API, data={})
    count = len(response.get_json())

    assert count > 0
    assert response.status_code == 200


def test_credit_card_transactions_with_data(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response = app.test_client().get(TRANSACTIONS_API, data={})
    count = len(response.get_json())

    assert count > 0
    assert response.status_code == 200


# ==================== /transaction/<string:period_str> ====================


def test_transactions_by_period_invalid(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().get(f"{TRANSACTIONS_API}/20166-10", data={})

    assert response.get_json() == {"error": "Invalid period. Use YYYY-MM format"}
    assert response.status_code == 400


def test_transactions_by_period_out_of_range(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CHECKING_TRANSACTIONS)

    response = app.test_client().get(f"{TRANSACTIONS_API}/2001-10", data={})
    count = len(response.get_json())

    assert count == 0
    assert response.status_code == 200


def test_checking_transactions_by_period_in_range(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CHECKING_TRANSACTIONS).get_json()

    response = app.test_client().get(f"{TRANSACTIONS_API}/2026-10", data={})
    count = len(response.get_json())

    assert count >= 2
    assert response.status_code == 200


def test_credit_card_transactions_by_period_in_range(tmp_path):
    _init_db(tmp_path)

    _import_transactions(CREDIT_CARD_TRANSACTIONS)

    response = app.test_client().get(f"{TRANSACTIONS_API}/2026-10", data={})
    count = len(response.get_json())

    assert count >= 2
    assert response.status_code == 200


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    tmp_path / DATABASE
    init_transactions_db()

    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DELETE FROM transactions")


def _import_transactions(file_name: str) -> TestResponse:
    with open(f"{DATA_PATH}{file_name}", "rb") as file:
        return app.test_client().post(IMPORT_API, data={"file": file})
