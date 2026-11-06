import os
import sqlite3
from flask import Blueprint, current_app, jsonify, request

accounts_bp = Blueprint("accounts", __name__)


def _connect():
    db_path = current_app.config["DATABASE_PATH"]
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_storage(db_path):
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            address TEXT DEFAULT '',
            phone_number TEXT DEFAULT ''
        )"""
    )
    connection.commit()
    connection.close()


def _serialize(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "address": row["address"],
        "phone_number": row["phone_number"],
    }


@accounts_bp.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json(silent=True) or {}
    required = ("name", "email")
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400
    try:
        connection = _connect()
        cursor = connection.execute(
            "INSERT INTO accounts (name, email, address, phone_number) VALUES (?, ?, ?, ?)",
            (data["name"], data["email"], data.get("address", ""), data.get("phone_number", "")),
        )
        connection.commit()
        row = connection.execute("SELECT * FROM accounts WHERE id = ?", (cursor.lastrowid,)).fetchone()
        connection.close()
        return jsonify(_serialize(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "An account with this email already exists"}), 409


@accounts_bp.route("/accounts", methods=["GET"])
def list_accounts():
    connection = _connect()
    rows = connection.execute("SELECT * FROM accounts ORDER BY id").fetchall()
    connection.close()
    return jsonify([_serialize(row) for row in rows]), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    connection = _connect()
    row = connection.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
    connection.close()
    if row is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(_serialize(row)), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    data = request.get_json(silent=True) or {}
    allowed = ("name", "email", "address", "phone_number")
    updates = {key: value for key, value in data.items() if key in allowed}
    if not updates:
        return jsonify({"error": "Provide at least one valid field to update"}), 400
    try:
        connection = _connect()
        existing = connection.execute("SELECT id FROM accounts WHERE id = ?", (account_id,)).fetchone()
        if existing is None:
            connection.close()
            return jsonify({"error": "Account not found"}), 404
        assignments = ", ".join(f"{key} = ?" for key in updates)
        values = list(updates.values()) + [account_id]
        connection.execute(f"UPDATE accounts SET {assignments} WHERE id = ?", values)
        connection.commit()
        row = connection.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
        connection.close()
        return jsonify(_serialize(row)), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "An account with this email already exists"}), 409


@accounts_bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    connection = _connect()
    cursor = connection.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
    connection.commit()
    connection.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": "Account deleted successfully", "id": account_id}), 200
