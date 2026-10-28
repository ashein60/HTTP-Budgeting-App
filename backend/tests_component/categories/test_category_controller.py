import sqlite3

from backend.database_setup import init_categories_db
from backend.flask_setup import app
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import (
    MessageCatalogFields,
    MessageFields,
)

# Required to access POST and GET requests
from backend.categories import category_controller  # noqa # isort: skip

# Files & Paths
DATABASE = "database.db"

# APIs
CATEGORY_API = "/category"
CATEGORY_DELETE_API = "/category/delete"

# Misc
CATEGORY = "Category"

messages = MessageCatalog()

# ==================== POST /category ====================


def test_add_category_empty_data(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_API, json={})
    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_add_category_invalid_name_key(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_API, json={"FooKey": "FooValue"})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_add_category_empty_name_value(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_API, json={"name": "   "})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_add_category_already_exists(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_API, json={"name": "Gas"})
    response = app.test_client().post(CATEGORY_API, json={"name": "Gas"})

    assert response.get_json() == messages.get(
        MessageFields.ALREADY_EXISTS.value, item=CATEGORY
    )


def test_add_category_random_caps(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_API, json={"name": "gAs"})

    message = response.get_json().get(MessageCatalogFields.MESSAGE.value)

    assert "Gas" in message


def test_add_category_multiple_words(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_API, json={"name": "Gas Ratio"})

    message = response.get_json().get(MessageCatalogFields.MESSAGE.value)

    assert "Gas Ratio" in message


# ==================== GET /category ====================


def test_get_category_empty(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().get(CATEGORY_API)
    assert response.get_json().get(MessageCatalogFields.DATA.value) == []


def test_get_category_with_data(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_API, json={"name": "Gas"})

    response = app.test_client().get(CATEGORY_API)

    assert response.get_json().get(MessageCatalogFields.DATA.value) == [{"name": "Gas"}]


# ==================== POST /category/delete ====================


def test_delete_category_by_name_empty_data(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_DELETE_API, json={})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_by_name_invalid_name_key(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_DELETE_API, json={"namedd": "Gas"})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_by_name_empty_name_value(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_DELETE_API, json={"name": "  "})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_by_name_not_found(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_DELETE_API, json={"name": "Gas"})

    assert response.get_json() == messages.get(
        MessageFields.NOT_FOUND.value, item=CATEGORY, value="Gas"
    )


def test_delete_category_by_name_success(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_API, json={"name": "gAS"})

    response = app.test_client().post(CATEGORY_DELETE_API, json={"name": "GaS"})

    assert response.get_json() == messages.get(
        MessageFields.DELETE_SUCCESS.value, item=CATEGORY, value="Gas"
    )


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    tmp_path / DATABASE
    init_categories_db()

    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DELETE FROM categories")
