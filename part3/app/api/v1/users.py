from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
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
@jwt_required(optional=True)
def create_user():
    claims = {}
    try:
        verify_jwt_in_request(optional=True)
        from flask_jwt_extended import get_jwt
        claims = get_jwt()
    except Exception:
        pass

    is_admin = claims.get('is_admin', False)

    data = request.get_json(silent=True) or {}

    # Non-admin cannot set is_admin=True
    if not is_admin:
        data.pop('is_admin', None)

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
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    if not is_admin and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized action'}), 403

    data = request.get_json(silent=True) or {}

    if not is_admin:
        if 'email' in data or 'password' in data:
            return jsonify({'error': 'You cannot modify email or password'}), 400
        data.pop('is_admin', None)

    try:
        user = facade.update_user(user_id, data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200
