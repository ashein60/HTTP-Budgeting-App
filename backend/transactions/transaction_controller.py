import csv
from dataclasses import asdict
from datetime import datetime
from io import TextIOWrapper

from flask import jsonify, request

from backend.flask_setup import app
from backend.transactions import transaction_service


@app.route("/transactions/import", methods=["POST"])
def import_transactions():
    """Import CSVs from Capital One Checking and Savings Accounts and Credit Cards"""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    reader = csv.DictReader(TextIOWrapper(file.stream, encoding="utf-8-sig"))

    transaction_service.import_transactions(reader)

    return jsonify({"success": "Transactions were imported successfully"}), 201


@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = transaction_service.get_transactions()

    return jsonify([asdict(t) for t in transactions]), 200


@app.route("/transactions/period/<string:period_str>", methods=["GET"])
def get_transactions_by_period(period_str):
    """Period format should be YYYY-MM"""
    try:
        period_datetime = datetime.strptime(period_str, "%Y-%m")
    except ValueError:
        return jsonify({"error": "Invalid period. Use YYYY-MM format"}), 400

    transactions = transaction_service.get_transactions_by_period(period_datetime)

    return jsonify([asdict(t) for t in transactions]), 200
