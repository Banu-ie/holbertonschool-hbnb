from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

places_bp = Blueprint('places', __name__)

@places_bp.route('/', methods=['GET'])
def get_places():
    return jsonify([p.to_dict() for p in facade.get_all_places()]), 200

@places_bp.route('/<place_id>', methods=['GET'])
def get_place(place_id):
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(place.to_dict()), 200

@places_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    current_user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    data['owner_id'] = current_user_id
    required = ('title', 'price', 'latitude', 'longitude')
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    try:
        place = facade.create_place(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(place.to_dict()), 201

@places_bp.route('/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    if not is_admin and place.owner_id != current_user_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    data = request.get_json(silent=True) or {}
    place = facade.update_place(place_id, data)
    return jsonify(place.to_dict()), 200

@places_bp.route('/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    if not is_admin and place.owner_id != current_user_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    facade.delete_place(place_id)
    return jsonify({'message': 'Place deleted'}), 200
