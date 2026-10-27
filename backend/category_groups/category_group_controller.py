import sqlite3
from dataclasses import asdict

from flask import jsonify, request

from backend.category_groups import category_group_service
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
        return jsonify({"error": "Category Group already exists"}), 409

    return jsonify(
        {"success": f"The Category Group {name} has been successfully added"}
    ), 201


@app.route("/category_group", methods=["GET"])
def get_category_groups():
    category_groups = category_group_service.get_category_groups()
    print(f"Hello: {category_groups}")
    return jsonify([asdict(c) for c in category_groups]), 200


@app.route("/category_group/delete", methods=["POST"])
def delete_category_group_by_name():
    data = request.get_json()

    if (
        not data
        or not isinstance(data.get(CategoryGroupFields.NAME.value), str)
        or not str(data[CategoryGroupFields.NAME.value]).strip()
    ):
        return jsonify({"error": "A non-empty string 'name' is required"}), 400

    name = str(data[CategoryGroupFields.NAME.value]).strip().title()

    is_deleted = category_group_service.delete_category_group_by_name(name)

    if is_deleted:
        return jsonify(
            {"success": f"The Category Group {name} has been successfully deleted"}
        ), 200

    return jsonify({"error": f"The Category Group {name} was not found"}), 404
