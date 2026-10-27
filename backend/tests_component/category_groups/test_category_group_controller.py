import sqlite3

from backend.database_setup import init_category_group_db
from backend.flask_setup import app
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import (
    MessageCatalogFields,
    MessageFields,
)

# Required to access POST and GET requests
from backend.category_groups import category_group_controller  # noqa # isort: skip

# Files & Paths
DATABASE = "database.db"

# APIs
CATEGORY_GROUP_API = "/category_group"
CATEGORY_GROUP_DELETE_API = "/category_group/delete"

# Misc
CATEGORY_GROUP = "Category Group"

messages = MessageCatalog()

# ==================== POST /category_group ====================


def test_add_category_group_empty_data(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={})
    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_add_category_group_invalid_name_key(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"FooKey": "FooValue"})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_add_category_group_empty_name_value(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "   "})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_add_category_group_already_exists(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income"})
    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income"})

    assert response.get_json() == messages.get(
        MessageFields.ALREADY_EXISTS.value, item=CATEGORY_GROUP
    )


def test_add_category_group_random_caps(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "inCOmE"})

    message = response.get_json().get(MessageCatalogFields.MESSAGE.value)

    assert "Income" in message


def test_add_category_group_multiple_words(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income Ratio"})

    message = response.get_json().get(MessageCatalogFields.MESSAGE.value)

    assert "Income Ratio" in message


# ==================== GET /category_group ====================


def test_get_category_group_empty(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().get(CATEGORY_GROUP_API)
    assert response.get_json().get(MessageCatalogFields.DATA.value) == []


def test_get_category_group_with_data(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income"})

    response = app.test_client().get(CATEGORY_GROUP_API)

    assert response.get_json().get(MessageCatalogFields.DATA.value) == [
        {"name": "Income"}
    ]


# ==================== POST /category_group/delete ====================


def test_delete_category_group_by_name_empty_data(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_DELETE_API, json={})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_group_by_name_invalid_name_key(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(
        CATEGORY_GROUP_DELETE_API, json={"namedd": "Income"}
    )

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_group_by_name_empty_name_value(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_DELETE_API, json={"name": "  "})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_group_by_name_not_found(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(
        CATEGORY_GROUP_DELETE_API, json={"name": "Income"}
    )

    assert response.get_json() == messages.get(
        MessageFields.NOT_FOUND.value, item=CATEGORY_GROUP, value="Income"
    )


def test_delete_category_group_by_name_success(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_GROUP_API, json={"name": "incOme"})

    response = app.test_client().post(
        CATEGORY_GROUP_DELETE_API, json={"name": "IncoMe"}
    )

    assert response.get_json() == messages.get(
        MessageFields.DELETE_SUCCESS.value, item=CATEGORY_GROUP, value="Income"
    )


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    tmp_path / DATABASE
    init_category_group_db()

    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DELETE FROM category_groups")
