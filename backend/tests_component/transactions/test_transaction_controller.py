import json
import sqlite3
from io import BytesIO

from backend.database_setup import init_transactions_db
from backend.flask_setup import app

# Required to access POST and GET requests
from backend.transactions import transaction_controller  # noqa

DATA_PATH = "backend/tests_component/transactions/data"
IMPORT_API = "/transactions/import"
TRANSACTIONS_API = "/transactions"
DATABASE = "database.db"


def test_import_no_file(tmp_path):
    init_db(tmp_path)

    response = app.test_client().post(IMPORT_API, data={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No file provided"}


def test_import_no_file_selected(tmp_path):
    init_db(tmp_path)

    response = app.test_client().post(
        IMPORT_API,
        data={"file": (BytesIO(b""), "")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "No file selected"}


def test_import_credit_card(tmp_path):
    init_db(tmp_path)

    with open(f"{DATA_PATH}/transactions.csv", "rb") as file:
        response = app.test_client().post(IMPORT_API, data={"file": file})

    assert response.status_code == 201
    assert response.get_json() == {"success": "Transactions were imported successfully"}


def test_transactions_empty(tmp_path):
    init_db(tmp_path)

    print("Map: ", app.url_map)

    response = app.test_client().get(TRANSACTIONS_API, data={})
    assert response.status_code == 200
    assert response.get_json() == []


def test_transactions_with_data(tmp_path):
    init_db(tmp_path)

    with open(f"{DATA_PATH}/transactions.csv", "rb") as file:
        app.test_client().post(IMPORT_API, data={"file": file})

    response = app.test_client().get(TRANSACTIONS_API, data={})

    with open(f"{DATA_PATH}/transactions.json", "r", encoding="utf-8") as file:
        transactions = json.load(file)

    assert response.status_code == 200
    assert response.get_json() == transactions


def init_db(tmp_path):
    tmp_path / DATABASE
    init_transactions_db()

    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DELETE FROM transactions")
