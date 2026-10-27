import sqlite3

from flask import jsonify, request

from backend.category_group import category_group_service
from backend.flask_setup import app
from backend.metadata.enums import CategoryGroupFields


@app.route("/category_group", methods=["POST"])
def add_category_group():
    data = request.get_json()

    if (
        not data
        or not isinstance(data.get(CategoryGroupFields.NAME.value), str)
        or not str(data[CategoryGroupFields.NAME.value]).strip()
    ):
        return jsonify({"error": "A non-empty string 'name' is required"}), 400

    name = str(data[CategoryGroupFields.NAME.value]).strip().title()

    try:
        category_group_service.add_category_group(name)
    except sqlite3.IntegrityError:
        return jsonify({"error": "Category group already exists"}), 409

    return jsonify({CategoryGroupFields.NAME.value: name}), 201
