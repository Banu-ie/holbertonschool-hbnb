from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.facade import facade

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email    = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400

    user = facade.get_user_by_email(email)
    if not user or not user.verify_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={'is_admin': user.is_admin}
    )
    return jsonify({'access_token': access_token}), 200
