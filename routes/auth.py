import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import User
from extensions import db
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "error": "Username already taken"}), 400

    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True, "data": {"message": "Registered successfully", "user_id": user.id, "username": user.username}}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    if not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "error": "Invalid password"}), 401

    return jsonify({"success": True, "data": {"message": "Login successful", "user_id": user.id, "username": user.username}}), 200
