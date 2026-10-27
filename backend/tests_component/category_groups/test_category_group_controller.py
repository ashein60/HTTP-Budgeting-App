import sqlite3

from backend.database_setup import init_category_group_db
from backend.flask_setup import app

# Required to access POST and GET requests
from backend.category_groups import category_group_controller  # noqa # isort: skip

# Files & Paths
DATABASE = "database.db"

# APIs
CATEGORY_GROUP_API = "/category_group"

# ==================== POST /category_group ====================


def test_add_category_group_empty_data(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={})

    assert response.get_json() == {"error": "A non-empty string 'name' is required"}
    assert response.status_code == 400


def test_add_category_group_missing_name_key(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"FooKey": "FooValue"})

    assert response.get_json() == {"error": "A non-empty string 'name' is required"}
    assert response.status_code == 400


def test_add_category_group_empty_name_value(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "   "})

    assert response.get_json() == {"error": "A non-empty string 'name' is required"}
    assert response.status_code == 400


def test_add_category_group_already_exists(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income"})
    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income"})

    assert response.get_json() == {"error": "Category group already exists"}
    assert response.status_code == 409


def test_add_category_group_random_caps(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "inCOmE"})

    assert response.get_json() == {"name": "Income"}
    assert response.status_code == 201


def test_add_category_group_multiple_words(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income Ratio"})

    assert response.get_json() == {"name": "Income Ratio"}
    assert response.status_code == 201


# ==================== GET /category_group ====================


def test_get_category_group_empty(tmp_path):
    _init_db(tmp_path)

    response = app.test_client().get(CATEGORY_GROUP_API)

    assert response.get_json() == []
    assert response.status_code == 200


def test_get_category_group_with_data(tmp_path):
    _init_db(tmp_path)

    app.test_client().post(CATEGORY_GROUP_API, json={"name": "Income"})

    response = app.test_client().get(CATEGORY_GROUP_API)

    assert response.get_json() == [{"name": "Income"}]
    assert response.status_code == 200


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    tmp_path / DATABASE
    init_category_group_db()

    with sqlite3.connect(DATABASE) as connection:
        connection.execute("DELETE FROM category_groups")
