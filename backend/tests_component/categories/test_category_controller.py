import sqlite3

from backend import flask_handler
from backend.database_setup import init_categories_db, init_category_groups_db
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import CategoryFields, MessageCatalogFields, MessageFields

# Required to access POST and GET requests
from backend.categories import category_controller  # noqa # isort: skip
from backend.category_groups import category_group_controller  # noqa # isort: skip

# Files & Paths
DATABASE = "database.db"

# APIs
CATEGORY_GROUP_API = "/category_group"
CATEGORY_API = "/category"
CATEGORY_DELETE_API = "/category/delete"

# Misc
CATEGORY = "Category"

messages = MessageCatalog()

# ==================== POST /category ====================


def test_add_category_empty_data(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(CATEGORY_API, json={})
    assert response.get_json() == messages.get(MessageFields.DATA_MISSING.value)


def test_add_category_invalid_name_key(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_API, json={"FooKey": "FooValue"}
    )

    assert response.get_json() == messages.get(
        MessageFields.INVALID_DATA.value, item=CategoryFields.NAME.value
    )


def test_add_category_empty_expected_value(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_API, json={CategoryFields.NAME.value: "Gas"}
    )

    assert response.get_json() == messages.get(
        MessageFields.INVALID_DATA.value, item=CategoryFields.EXPECTED.value
    )


def test_add_category_empty_group_name_value(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_API,
        json={CategoryFields.NAME.value: "Gas", CategoryFields.EXPECTED.value: "0"},
    )

    assert response.get_json() == messages.get(
        MessageFields.INVALID_DATA.value, item=CategoryFields.GROUP_NAME.value
    )


def test_add_category_already_exists(tmp_path):
    _init_db(tmp_path)

    flask_handler.app.test_client().post(
        CATEGORY_GROUP_API, json={CategoryFields.NAME.value: "Expense"}
    )

    flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "Gas",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        },
    )

    response = flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "Gas",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        },
    )

    assert response.get_json() == messages.get(
        MessageFields.ALREADY_EXISTS.value, item=CATEGORY
    )


def test_add_category_foreign_key_not_found(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "Gas",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        },
    )

    database_path = tmp_path / DATABASE
    with sqlite3.connect(database_path) as connection:
        enabled = connection.execute("PRAGMA foreign_keys").fetchone()[0]
        print(f"Enabled: {enabled}")

    assert response.get_json() == messages.get(
        MessageFields.FOREIGN_KEY_NOT_FOUND.value, item=CATEGORY
    )


def test_add_category_random_caps(tmp_path):
    _init_db(tmp_path)

    flask_handler.app.test_client().post(
        CATEGORY_GROUP_API, json={CategoryFields.NAME.value: "Expense"}
    )

    response = flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "gAs",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "eXpEnse",
        },
    )

    message = response.get_json().get(MessageCatalogFields.MESSAGE.value)
    assert "Gas" in message


def test_add_category_multiple_words(tmp_path):
    _init_db(tmp_path)

    flask_handler.app.test_client().post(
        CATEGORY_GROUP_API, json={CategoryFields.NAME.value: "Expense"}
    )

    response = flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "Gas Ratio",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        },
    )

    message = response.get_json().get(MessageCatalogFields.MESSAGE.value)

    assert "Gas Ratio" in message


# ==================== GET /category ====================


def test_get_category_empty(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().get(CATEGORY_API)
    assert response.get_json().get(MessageCatalogFields.DATA.value) == []


def test_get_category_with_data(tmp_path):
    _init_db(tmp_path)

    flask_handler.app.test_client().post(
        CATEGORY_GROUP_API, json={CategoryFields.NAME.value: "Expense"}
    )

    flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "Gas Ratio",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        },
    )

    response = flask_handler.app.test_client().get(CATEGORY_API)

    assert response.get_json().get(MessageCatalogFields.DATA.value) == [
        {
            CategoryFields.NAME.value: "Gas Ratio",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        }
    ]


# ==================== POST /category/delete ====================


def test_delete_category_by_name_empty_data(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(CATEGORY_DELETE_API, json={})

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_by_name_invalid_name_key(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_DELETE_API, json={"namedd": "Gas"}
    )

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_by_name_empty_name_value(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_DELETE_API, json={CategoryFields.NAME.value: "  "}
    )

    assert response.get_json() == messages.get(MessageFields.INVALID_CATEGORY.value)


def test_delete_category_by_name_not_found(tmp_path):
    _init_db(tmp_path)

    response = flask_handler.app.test_client().post(
        CATEGORY_DELETE_API, json={CategoryFields.NAME.value: "Gas"}
    )

    assert response.get_json() == messages.get(
        MessageFields.NOT_FOUND.value, item=CATEGORY, value="Gas"
    )


def test_delete_category_by_name_success(tmp_path):
    _init_db(tmp_path)

    flask_handler.app.test_client().post(
        CATEGORY_GROUP_API, json={CategoryFields.NAME.value: "Expense"}
    )

    flask_handler.app.test_client().post(
        CATEGORY_API,
        json={
            CategoryFields.NAME.value: "gAS",
            CategoryFields.EXPECTED.value: "0",
            CategoryFields.GROUP_NAME.value: "Expense",
        },
    )

    response = flask_handler.app.test_client().post(
        CATEGORY_DELETE_API, json={"name": "GaS"}
    )

    assert response.get_json() == messages.get(
        MessageFields.DELETE_SUCCESS.value, item=CATEGORY, value="Gas"
    )


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    flask_handler.set_database_path(tmp_path / DATABASE)
    init_category_groups_db()
    init_categories_db()

    with sqlite3.connect(flask_handler.get_database_path()) as connection:
        connection.execute("DELETE FROM category_groups")
        connection.execute("DELETE FROM categories")
