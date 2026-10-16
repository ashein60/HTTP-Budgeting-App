from flask import request, jsonify
from io import TextIOWrapper
from metadata import flask_setup
from transactions import transaction_service
from dataclasses import asdict


import csv

@flask_setup.app.route('/import-transactions', methods=['POST'])
def import_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    reader = csv.DictReader(
        TextIOWrapper(file.stream, encoding='utf-8-sig')
    )   

    transaction_service.import_transactions(reader)

    return jsonify({"success": "Transactions were imported successfully"}), 201

@flask_setup.app.route('/get-all-transactions', methods=['GET'])
def get_all_transactions():
    transactions = transaction_service.get_all_transactions()

    if transactions is None:
        return jsonify(None)

    return jsonify([asdict(t) for t in transactions])