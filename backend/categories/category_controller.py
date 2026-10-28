import sqlite3

from flask import request

from backend.categories import category_service
from backend.flask_setup import app
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import CategoryFields, MessageFields

CATEGORY = "Category"
CATEGORIES = "Categories"

messages = MessageCatalog()


@app.route("/category", methods=["POST"])
def add_category():
    data = request.get_json()

    if (
        not data
        or not isinstance(data.get(CategoryFields.NAME.value), str)
        or not str(data[CategoryFields.NAME.value]).strip()
    ):
        return messages.get(MessageFields.INVALID_CATEGORY.value)

    name = str(data[CategoryFields.NAME.value]).strip().title()

    try:
        category_service.add_category(name)
    except sqlite3.IntegrityError:
        return messages.get(MessageFields.ALREADY_EXISTS.value, item=CATEGORY)

    return messages.get(MessageFields.POST_SUCCESS.value, item=CATEGORY, value=name)


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
