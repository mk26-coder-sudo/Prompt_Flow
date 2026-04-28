from unittest import result
from werkzeug.security import generate_password_hash
from flask import Blueprint, request, jsonify
from service.user_service import create_user, login_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    if not data:
        return {"error": "No data provided"}

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {"error": "Missing required fields"}

    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash(password)

    result = create_user(username, email, password_hash)

    return result
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    result = login_user(email, password)

    return result