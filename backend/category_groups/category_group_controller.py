import sqlite3

from flask import request

from backend.category_groups import category_group_service
from backend.flask_handler import app
from backend.message_catalog import MessageCatalog
from backend.metadata.enums import CategoryGroupFields, MessageFields

CATEGORY_GROUP = "Category Group"
CATEGORY_GROUPS = "Category Groups"

messages = MessageCatalog()


@app.route("/category_group", methods=["POST"])
def add_category_group():
    data = request.get_json()

    if (
        not data
        or not isinstance(data.get(CategoryGroupFields.NAME.value), str)
        or not str(data[CategoryGroupFields.NAME.value]).strip()
    ):
        return messages.get(MessageFields.INVALID_CATEGORY.value)

    name = str(data[CategoryGroupFields.NAME.value]).strip().title()

    try:
        category_group_service.add_category_group(name)
    except sqlite3.IntegrityError:
        return messages.get(MessageFields.ALREADY_EXISTS.value, item=CATEGORY_GROUP)

    return messages.get(
        MessageFields.POST_SUCCESS.value, item=CATEGORY_GROUP, value=name
    )


@app.route("/category_group", methods=["GET"])
def get_category_groups():
    category_groups = category_group_service.get_category_groups()

    return messages.get(
        MessageFields.GET_SUCCESS.value, category_groups, items=CATEGORY_GROUPS
    )


@app.route("/category_group/delete", methods=["POST"])
def delete_category_group_by_name():
    data = request.get_json()

    if (
        not data
        or not isinstance(data.get(CategoryGroupFields.NAME.value), str)
        or not str(data[CategoryGroupFields.NAME.value]).strip()
    ):
        return messages.get(MessageFields.INVALID_CATEGORY.value)

    name = str(data[CategoryGroupFields.NAME.value]).strip().title()

    is_deleted = category_group_service.delete_category_group_by_name(name)

    if is_deleted:
        return messages.get(
            MessageFields.DELETE_SUCCESS.value, item=CATEGORY_GROUP, value=name
        )

    return messages.get(MessageFields.NOT_FOUND.value, item=CATEGORY_GROUP, value=name)
