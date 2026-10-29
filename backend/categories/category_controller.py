import sqlite3

from flask import request

from backend.categories import category_service
from backend.categories.category import Category
from backend.common import check_missing_fields_from_json_data
from backend.flask_setup import app
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import CategoryFields, MessageFields, SqliteErrorFields

CATEGORY = "Category"
CATEGORIES = "Categories"

messages = MessageCatalog()


@app.route("/category", methods=["POST"])
def add_category():
    data = request.get_json()

    if not data:
        return messages.get(MessageFields.DATA_MISSING.value)

    field = check_missing_fields_from_json_data(data, CategoryFields)

    if field is not None:
        return messages.get(MessageFields.INVALID_DATA.value, item=field.value)

    category = Category.from_sql_row(data)

    try:
        category_service.add_category(category)
    except sqlite3.IntegrityError as e:
        error_name = getattr(e, "sqlite_errorname", None)
        print(f"Okay then: {error_name}")

        if error_name == SqliteErrorFields.SQLITE_CONSTRAINT_PRIMARYKEY.value:
            return messages.get(MessageFields.ALREADY_EXISTS.value, item=CATEGORY)

        if error_name == SqliteErrorFields.SQLITE_CONSTRAINT_FOREIGNKEY.value:
            return messages.get(MessageFields.FOREIGN_KEY_NOT_FOUND.value)

    return messages.get(
        MessageFields.POST_SUCCESS.value, item=CATEGORY, value=category.name
    )


@app.route("/category", methods=["GET"])
def get_categories():
    categories = category_service.get_categories()

    return messages.get(MessageFields.GET_SUCCESS.value, categories, items=CATEGORIES)


@app.route("/category/delete", methods=["POST"])
def delete_category_by_name():
    data = request.get_json()

    if (
        not data
        or not isinstance(data.get(CategoryFields.NAME.value), str)
        or not str(data[CategoryFields.NAME.value]).strip()
    ):
        return messages.get(MessageFields.INVALID_CATEGORY.value)

    name = str(data[CategoryFields.NAME.value]).strip().title()

    is_deleted = category_service.delete_category_by_name(name)

    if is_deleted:
        return messages.get(
            MessageFields.DELETE_SUCCESS.value, item=CATEGORY, value=name
        )

    return messages.get(MessageFields.NOT_FOUND.value, item=CATEGORY, value=name)
