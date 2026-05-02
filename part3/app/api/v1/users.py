from flask import Blueprint, request, jsonify
from app.services.facade import facade

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify([u.to_dict() for u in facade.get_all_users()]), 200

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = facade.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json(silent=True) or {}
    required = ('first_name', 'last_name', 'email', 'password')
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    try:
        user = facade.create_user(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    return jsonify(user.to_dict()), 201

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    try:
        user = facade.update_user(user_id, data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200
